import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Upload, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  RefreshCw, 
  Sparkles, 
  LayoutDashboard, 
  Code2, 
  FileCheck,
  Box,
  Armchair,
  Trash2,
  X
} from 'lucide-react';
import { PipelineTracker } from './components/PipelineTracker';
import { FloorplanViewer2D } from './components/FloorplanViewer2D';
import { FloorplanViewer3D } from './components/FloorplanViewer3D';
import { FurniturePlanner } from './components/FurniturePlanner';
import { GeometryJsonViewer } from './components/GeometryJsonViewer';
import type { Structured2DGeometry, PipelineStage } from './types/floorplan';

const API_BASE = 'http://localhost:5000';

const DEFAULT_STAGES: PipelineStage[] = [
  { step: 1, name: 'PDF Upload', status: 'pending', details: 'Waiting for architectural floorplan PDF' },
  { step: 2, name: 'Node.js Ingestion', status: 'pending', details: 'Multer memory buffer validation' },
  { step: 3, name: 'FastAPI Dispatch', status: 'pending', details: 'Forward payload to Python port 8000' },
  { step: 4, name: 'PyMuPDF Vectors', status: 'pending', details: 'Extract text blocks & vector commands' },
  { step: 5, name: 'OpenCV Analysis', status: 'pending', details: '150 DPI render & structural line detection' },
  { step: 6, name: 'Gemini Interpretation', status: 'pending', details: 'Vision model room & symbol labeling' },
  { step: 7, name: '2D Geometry JSON', status: 'pending', details: 'Final structured coordinate synthesis' },
];

export function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [stages, setStages] = useState<PipelineStage[]>(DEFAULT_STAGES);
  const [geometry, setGeometry] = useState<Structured2DGeometry | null>(null);
  const [activeTab, setActiveTab] = useState<'blueprint' | '3d' | 'json' | 'furniture'>('3d');
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Check backend health only on mount (do not auto-load sample data)
  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const res = await axios.get(`${API_BASE}/health`, { timeout: 3000 });
      setBackendOnline(res.data.status === 'healthy');
    } catch {
      setBackendOnline(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setGeometry(null); // Clear previous conversion results
      setStages(DEFAULT_STAGES); // Reset pipeline status
      setErrorMessage(null);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      const isPdf = droppedFile.type === 'application/pdf' || droppedFile.name.endsWith('.pdf');
      const isImg = droppedFile.type.startsWith('image/') || /\.(jpg|jpeg|png|webp)$/i.test(droppedFile.name);
      if (isPdf || isImg) {
        setFile(droppedFile);
        setGeometry(null); // Clear previous conversion results
        setStages(DEFAULT_STAGES); // Reset pipeline status
        setErrorMessage(null);
      } else {
        setErrorMessage('Only PDF and Image files (JPG, PNG, WEBP) are supported.');
      }
    }
  };

  const handleClearAll = () => {
    setFile(null);
    setGeometry(null);
    setStages(DEFAULT_STAGES);
    setErrorMessage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setErrorMessage(null);

    // Initial stages
    setStages([
      { step: 1, name: 'PDF Upload', status: 'in_progress', details: `Uploading ${file.name}...` },
      { step: 2, name: 'Node.js Ingestion', status: 'pending' },
      { step: 3, name: 'FastAPI Dispatch', status: 'pending' },
      { step: 4, name: 'PyMuPDF Vectors', status: 'pending' },
      { step: 5, name: 'OpenCV Analysis', status: 'pending' },
      { step: 6, name: 'Gemini Interpretation', status: 'pending' },
      { step: 7, name: '2D Geometry JSON', status: 'pending' },
    ]);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_BASE}/api/floorplans/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (res.data.success) {
        setGeometry(res.data.geometry);
        setStages(res.data.pipeline_stages || []);
      } else {
        throw new Error(res.data.error || 'Pipeline processing failed.');
      }
    } catch (err: any) {
      console.error(err);
      const msg = err.response?.data?.details || err.response?.data?.error || err.message;
      setErrorMessage(msg);
      if (err.response?.data?.pipeline_stages) {
        setStages(err.response.data.pipeline_stages);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLoadSample = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      const res = await axios.get(`${API_BASE}/api/floorplans/sample`);
      if (res.data.success) {
        setGeometry(res.data.geometry);
        setStages(res.data.pipeline_stages || []);
      }
    } catch (err: any) {
      setErrorMessage('Could not load sample floorplan. Ensure Node.js server is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Top Navigation Bar */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-600/20 border border-indigo-500/30 rounded-xl text-indigo-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base font-bold tracking-tight text-white m-0">
                AI Interior Designer
              </h1>
              <p className="text-xs text-slate-400 m-0">
                Architectural 2D Geometry Parser
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Status indicator */}
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border bg-slate-800/80 border-slate-700">
              <span
                className={`w-2 h-2 rounded-full ${
                  backendOnline === true
                    ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]'
                    : backendOnline === false
                    ? 'bg-rose-400'
                    : 'bg-amber-400'
                }`}
              />
              <span className="text-slate-300">
                {backendOnline === true
                  ? 'Node & Python Services Ready'
                  : backendOnline === false
                  ? 'Backend Offline (Port 5000)'
                  : 'Checking status...'}
              </span>
            </div>

            {(geometry || file) && (
              <button
                onClick={handleClearAll}
                className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800/80 hover:bg-rose-950/40 hover:border-rose-700/50 text-slate-300 hover:text-rose-300 transition-colors flex items-center gap-1.5"
                title="Clear current drawing and reset pipeline"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Reset Plan</span>
              </button>
            )}

            <a
              href="/walkthrough.html"
              target="_blank"
              rel="noreferrer"
              className="text-xs font-bold px-3 py-1.5 rounded-lg border border-amber-500/40 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 transition-all flex items-center gap-1.5 shadow-md shadow-amber-500/20"
              title="Open full interactive 3D architectural walkthrough of the 4,537 sq ft floor plan"
            >
              <Sparkles className="w-3.5 h-3.5 text-slate-950" />
              <span>3D Walkthrough (New Tab)</span>
            </a>

            <button
              onClick={handleLoadSample}
              disabled={loading}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors flex items-center gap-1.5"
            >
              <FileCheck className="w-3.5 h-3.5 text-indigo-400" />
              Load Sample Drawing
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 flex flex-col gap-6 w-full">
        {/* Error Alert */}
        {errorMessage && (
          <div className="p-4 bg-rose-950/40 border border-rose-500/40 rounded-xl text-rose-300 text-sm flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <span className="font-semibold">Pipeline Error: </span>
              {errorMessage}
            </div>
          </div>
        )}

        {/* 1. PDF UPLOAD SECTION */}
        <section className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <div className="flex flex-col md:flex-row items-center gap-5">
            {/* Dropzone */}
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className="flex-1 w-full border-2 border-dashed border-slate-700 hover:border-indigo-500/60 rounded-xl p-6 text-center cursor-pointer transition-all bg-slate-950/40 hover:bg-slate-900/60 flex flex-col items-center justify-center gap-2 group"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,image/png,image/jpeg,image/webp"
                className="hidden"
                onChange={handleFileChange}
              />
              <div className="p-3 rounded-full bg-slate-800 group-hover:bg-indigo-600/20 text-slate-400 group-hover:text-indigo-400 transition-all">
                <Upload className="w-6 h-6" />
              </div>
              <div className="text-sm font-medium text-slate-200">
                {file ? (
                  <span className="text-indigo-300 font-semibold">{file.name}</span>
                ) : (
                  <span>Click to browse or drag & drop architectural PDF or Image (JPG, PNG)</span>
                )}
              </div>
              <p className="text-xs text-slate-500">
                {file ? `${(file.size / (1024 * 1024)).toFixed(2)} MB • Ready for processing` : 'Architectural drawings, CAD sheets, and floorplan blueprints'}
              </p>
            </div>

            {/* Action buttons */}
            <div className="flex flex-col sm:flex-row md:flex-col gap-3 w-full md:w-auto">
              <button
                onClick={handleUpload}
                disabled={!file || loading}
                className={`px-5 py-3 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 shadow-lg transition-all ${
                  !file || loading
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                    : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-500/25 cursor-pointer'
                }`}
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Processing Pipeline...</span>
                  </>
                ) : (
                  <>
                    <FileText className="w-4 h-4" />
                    <span>Run 7-Step Extraction</span>
                  </>
                )}
              </button>

              {file && !loading && (
                <button
                  onClick={handleClearAll}
                  className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-700/60 flex items-center justify-center gap-1.5 transition-colors"
                >
                  <X className="w-3.5 h-3.5" />
                  <span>Remove Selected File</span>
                </button>
              )}
            </div>
          </div>
        </section>

        {/* 2. PIPELINE PROGRESS TRACKER */}
        <section>
          <PipelineTracker stages={stages} />
        </section>

        {/* 3. GROUND FLOOR ARCHITECTURAL 3D WALKTHROUGH (4,537 Sq Ft) — Full-Bleed Width so Sidebars use Outer Margins */}
        <section className="w-screen relative left-1/2 -translate-x-1/2 px-4 sm:px-6 flex flex-col gap-3">
          <div className="max-w-7xl mx-auto w-full flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-1.5 text-xs font-bold px-3 py-1 bg-amber-500 text-slate-950 rounded-lg shadow-sm">
                <Sparkles className="w-3.5 h-3.5" />
                Ground Floor 3D Walkthrough (4,537 Sq Ft)
              </span>
              <span className="text-xs text-slate-400 hidden sm:inline">
                Traced from 2D Ground Floor Plan CAD Blueprint • Three.js r128 Walkthrough
              </span>
            </div>
            <a
              href="/walkthrough.html"
              target="_blank"
              rel="noreferrer"
              className="text-xs text-sky-400 hover:text-sky-300 font-semibold flex items-center gap-1"
            >
              <span>Open in Full Window ↗</span>
            </a>
          </div>

          <div className="w-full h-[760px] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl bg-[#090d16]">
            <iframe
              src="/walkthrough.html"
              title="Architectural 3D Walkthrough"
              className="w-full h-full border-0"
            />
          </div>
        </section>

        {/* 4. VISUALIZATION & OUTPUT TABS */}
        {geometry && (
          <section className="flex flex-col gap-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveTab('3d')}
                  className={`text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all ${
                    activeTab === '3d'
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                  }`}
                >
                  <Box className="w-3.5 h-3.5 text-indigo-300" />
                  3D Walkthrough Space
                </button>
                <button
                  onClick={() => setActiveTab('furniture')}
                  className={`text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all ${
                    activeTab === 'furniture'
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                  }`}
                >
                  <Armchair className="w-3.5 h-3.5 text-indigo-300" />
                  Furniture Planner
                </button>
                <button
                  onClick={() => setActiveTab('blueprint')}
                  className={`text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all ${
                    activeTab === 'blueprint'
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                  }`}
                >
                  <LayoutDashboard className="w-3.5 h-3.5" />
                  2D CAD Blueprint
                </button>
                <button
                  onClick={() => setActiveTab('json')}
                  className={`text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all ${
                    activeTab === 'json'
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                  }`}
                >
                  <Code2 className="w-3.5 h-3.5" />
                  Structured 2D Geometry JSON
                </button>
              </div>

              <span className="text-xs text-slate-400 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                Geometry Ready
              </span>
            </div>

            {/* Content view */}
            {activeTab === '3d' ? (
              <FloorplanViewer3D geometry={geometry} />
            ) : activeTab === 'furniture' ? (
              <FurniturePlanner geometry={geometry} />
            ) : activeTab === 'blueprint' ? (
              <FloorplanViewer2D geometry={geometry} />
            ) : (
              <GeometryJsonViewer geometry={geometry} />
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
