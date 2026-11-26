import { GoogleGenAI } from '@google/genai';
import dotenv from 'dotenv';
dotenv.config();
const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey || apiKey === 'your_gemini_api_key_here') {
    console.warn('⚠️  Warning: GEMINI_API_KEY is not set in backend/.env');
}
export const ai = new GoogleGenAI({
    apiKey: apiKey || '',
});
//# sourceMappingURL=gemini.js.map