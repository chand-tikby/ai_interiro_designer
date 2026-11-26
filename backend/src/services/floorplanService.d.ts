export interface Point2D {
    x: number;
    y: number;
}
export interface WallSegment {
    id: string;
    start: Point2D;
    end: Point2D;
    thickness: number;
    type?: 'exterior' | 'interior';
}
export interface RoomGeometry {
    id: string;
    name: string;
    dimensions?: string;
    label_position: Point2D;
    boundary: Point2D[];
}
export interface DoorSymbol {
    id: string;
    label?: string;
    position: Point2D;
    width: number;
    swing?: 'inward_left' | 'inward_right' | 'outward_left' | 'outward_right' | 'sliding';
}
export interface WindowSymbol {
    id: string;
    label?: string;
    position: Point2D;
    width: number;
}
export interface ColumnSymbol {
    id: string;
    position: Point2D;
    width: number;
    height: number;
}
export interface StaircaseSymbol {
    id: string;
    type: 'spiral' | 'straight';
    position: Point2D;
    radius?: number;
    steps?: number;
}
export interface DimensionCallout {
    id: string;
    label: string;
    start: Point2D;
    end: Point2D;
    textPos: Point2D;
}
export interface Structured2DGeometry {
    metadata: {
        title?: string;
        area_sqft?: string;
        page_dimensions: {
            width: number;
            height: number;
        };
        scale: string;
        unit: string;
        rooms_count: number;
        walls_count: number;
        doors_count: number;
        windows_count: number;
        columns_count?: number;
    };
    rooms: RoomGeometry[];
    walls: WallSegment[];
    doors: DoorSymbol[];
    windows: WindowSymbol[];
    columns?: ColumnSymbol[];
    stairs?: StaircaseSymbol[];
    dimensions_callouts?: DimensionCallout[];
    pergola_slots?: Array<{
        x: number;
        y: number;
        width: number;
        height: number;
    }>;
    overlay_image_url?: string;
}
export declare class FloorplanService {
    private pythonServiceUrl;
    constructor();
    extractViaPython(fileBuffer: Buffer): Promise<any>;
    /**
     * Purely Dynamic Fallback:
     * Synthesizes 2D geometry directly from OpenCV computer vision extraction
     * of the ACTUAL uploaded image/PDF (no hardcoded rooms, no hardcoded coordinates).
     */
    synthesizeDynamicGeometry(extractedData: any, overlayImageUrl: string): Structured2DGeometry;
    /**
     * Step 6: Gemini Multimodal Vision / Dynamic Architectural Parsing.
     */
    interpretWithGemini(extractedData: any): Promise<Structured2DGeometry>;
    /**
     * Only called when the user clicks "Load Sample Drawing" on demand.
     */
    getSampleDemoModel(): Structured2DGeometry;
}
export declare const floorplanService: FloorplanService;
//# sourceMappingURL=floorplanService.d.ts.map