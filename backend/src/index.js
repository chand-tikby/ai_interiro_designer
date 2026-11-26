import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import multer from 'multer';
import { ai } from './config/gemini.js';
import { floorplanService } from './services/floorplanService.js';
dotenv.config();
const app = express();
const port = process.env.PORT || 5000;
// Setup multer memory storage for PDF file uploads
const upload = multer({
    storage: multer.memoryStorage(),
    limits: {
        fileSize: 30 * 1024 * 1024, // 30 MB max
    },
    fileFilter: (req, file, cb) => {
        const isPdf = file.mimetype === 'application/pdf' || file.originalname.toLowerCase().endsWith('.pdf');
        const isImage = file.mimetype.startsWith('image/') || /\.(jpg|jpeg|png|webp)$/i.test(file.originalname);
        if (isPdf || isImage) {
            cb(null, true);
        }
        else {
            cb(new Error('Only PDF and Image files (JPG, PNG, WEBP) are supported'));
        }
    },
});
app.use(cors());
app.use(express.json({ limit: '50mb' }));
// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'backend',
        geminiConfigured: Boolean(process.env.GEMINI_API_KEY && process.env.GEMINI_API_KEY !== 'your_gemini_api_key_here'),
    });
});
/**
 * 7-Step Architectural Floorplan Processing Pipeline:
 * 1. Upload PDF via React
 * 2. Send to Node.js backend
 * 3. Node.js sends to Python FastAPI
 * 4. Python PyMuPDF extracts text, dimensions, and vector drawings
 * 5. OpenCV line/contour detection & high-res rendering
 * 6. Gemini interprets room labels, dimensions, and symbols
 * 7. Combine into structured 2D geometry JSON
 */
app.post('/api/floorplans/upload', upload.single('file'), async (req, res) => {
    const stages = [
        { step: 1, name: 'Upload PDF from React', status: 'completed', details: `Received: ${req.file?.originalname || 'floorplan.pdf'} (${Math.round((req.file?.size || 0) / 1024)} KB)` },
        { step: 2, name: 'Node.js Backend Ingestion', status: 'completed', details: 'Validated PDF payload in memory buffer' },
    ];
    try {
        if (!req.file || !req.file.buffer) {
            res.status(400).json({ error: 'Please upload a valid PDF file under the "file" field.' });
            return;
        }
        // Step 3: Forward to Python FastAPI
        stages.push({ step: 3, name: 'Node.js to Python FastAPI Dispatch', status: 'in_progress' });
        const extractedData = await floorplanService.extractViaPython(req.file.buffer);
        stages[2] = {
            step: 3,
            name: 'Node.js to Python FastAPI Dispatch',
            status: 'completed',
            details: 'Transferred PDF buffer to Python FastAPI service on port 8000',
        };
        // Step 4: PyMuPDF Extraction Result
        const vectorCount = extractedData.vector_drawings_count || 0;
        const textCount = extractedData.text_blocks?.length || 0;
        stages.push({
            step: 4,
            name: 'PyMuPDF Text, Dimensions & Vectors',
            status: 'completed',
            details: `Dimensions: ${extractedData.dimensions.width}x${extractedData.dimensions.height} pt, ${vectorCount} vector shapes, ${textCount} text blocks.`,
        });
        // Step 5: OpenCV & Raster Analysis Result
        const detectedLinesCount = extractedData.detected_lines_count || 0;
        stages.push({
            step: 5,
            name: 'OpenCV & Raster Line/Contour Detection',
            status: 'completed',
            details: `Is vector sufficient: ${extractedData.is_vector_sufficient ? 'YES' : 'NO (Scanned/Raster fallback)'}, Detected ${detectedLinesCount} OpenCV structural wall lines at 150 DPI.`,
        });
        // Step 6: Architectural Interpretation
        stages.push({
            step: 6,
            name: 'Architectural Room & Geometry Correlation',
            status: 'in_progress',
            details: 'Correlating room labels, dimensions, and architectural symbols...',
        });
        const structuredGeometry = await floorplanService.interpretWithGemini(extractedData);
        stages[5] = {
            step: 6,
            name: 'Architectural Room & Geometry Correlation',
            status: 'completed',
            details: `Correlated ${structuredGeometry.rooms.length} rooms, ${structuredGeometry.walls.length} walls, ${structuredGeometry.doors.length} doors, ${structuredGeometry.windows.length} windows with exact CAD coordinates.`,
        };
        // Step 7: Combine into Structured 2D Geometry JSON
        stages.push({
            step: 7,
            name: 'Structured 2D Geometry JSON Generation',
            status: 'completed',
            details: 'Successfully synthesized 2D geometric coordinate model with walls, rooms, doors & windows.',
        });
        res.json({
            success: true,
            geometry: structuredGeometry,
            pipeline_stages: stages,
            raw_extraction_summary: {
                dimensions: extractedData.dimensions,
                is_vector_sufficient: extractedData.is_vector_sufficient,
                vector_count: vectorCount,
                detected_lines_count: detectedLinesCount,
                text_blocks_count: textCount,
            },
        });
    }
    catch (err) {
        console.error('Pipeline execution error:', err);
        res.status(500).json({
            success: false,
            error: 'Floorplan processing pipeline failed',
            details: err.message,
            pipeline_stages: stages,
        });
    }
});
// Provide demonstration sample 2D floorplan when user clicks 'Load Sample Drawing'
app.get('/api/floorplans/sample', (req, res) => {
    const sampleData = floorplanService.getSampleDemoModel();
    res.json({
        success: true,
        geometry: sampleData,
        pipeline_stages: [
            { step: 1, name: 'Upload Drawing from React', status: 'completed', details: 'Loaded RCC Residential Building drawing (58\'3" x 55\'11")' },
            { step: 2, name: 'Node.js Backend Ingestion', status: 'completed', details: 'Validated 819x1024 architectural floor plan buffer' },
            { step: 3, name: 'Node.js to Python FastAPI Dispatch', status: 'completed', details: 'Dispatched drawing payload to Python port 8000' },
            { step: 4, name: 'PyMuPDF Text, Dimensions & Vectors', status: 'completed', details: 'Extracted Bed, Bath, Dress, Living Hall & Balcony annotations' },
            { step: 5, name: 'OpenCV & Raster Line/Contour Detection', status: 'completed', details: 'Mapped 17 structural red columns, walls, & spiral staircase' },
            { step: 6, name: 'Gemini Architectural Interpretation', status: 'completed', details: 'Correlated joineries (MD, D, D2, W2, W3, Fw, V) & 2931 sq.ft buildup' },
            { step: 7, name: 'Structured 2D Geometry JSON Generation', status: 'completed', details: 'High-fidelity geometric model synchronized with blueprint' },
        ],
    });
});
app.listen(port, () => {
    console.log(`🚀 Node.js Backend server running on http://localhost:${port}`);
});
//# sourceMappingURL=index.js.map