import express from 'express';
import multer from 'multer';
import FormData from 'form-data';
import axios from 'axios';
import logger from '../utils/logger.js';

const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

router.post('/', upload.single('image'), async (req, res) => {
  const imageFile = req.file;
  const fastapi_url = req.body.fastapi_url || req.query.fastapi_url;

  // Log incoming request details
  logger.info('POST /analyze request received');
  logger.info(`FastAPI URL from request: ${fastapi_url}`);
  logger.info(`File exists: ${!!imageFile}`);
  if (imageFile) {
    logger.info(`File details - name: ${imageFile.originalname}, size: ${imageFile.size} bytes, mimetype: ${imageFile.mimetype}`);
    logger.info(`File buffer exists: ${!!imageFile.buffer}, buffer length: ${imageFile.buffer?.length}`);
  }

  // Validate required fields
  if (!imageFile) {
    logger.warn('Image file is missing from request');
    return res.status(400).json({ error: 'Image file is required' });
  }

  if (!imageFile.buffer) {
    logger.warn('Image file buffer is missing or invalid');
    return res.status(400).json({ error: 'Image file buffer is invalid' });
  }

  if (!fastapi_url) {
    logger.warn('FastAPI URL is missing from request');
    return res.status(400).json({ error: 'FastAPI URL is required' });
  }

  logger.info(`Forwarding image analysis request to FastAPI: ${fastapi_url}/analyze`);

  // Create FormData to forward to FastAPI with correct field name 'image'
  const formData = new FormData();
  formData.append('image', imageFile.buffer, {
    filename: imageFile.originalname,
    contentType: imageFile.mimetype,
  });
  formData.append('file', imageFile.buffer, {
    filename: imageFile.originalname,
    contentType: imageFile.mimetype,
  });

  logger.info('FormData created successfully with file appended');

  // Forward request to FastAPI server with axios
  const response = await axios.post(
    `${fastapi_url}/analyze`,
    formData,
    {
      headers: formData.getHeaders(),
      timeout: 30000, // 30 second timeout
    }
  );

  logger.info(`FastAPI response status: ${response.status}`);
  logger.info(`FastAPI response data: ${JSON.stringify(response.data)}`);

  if (!response.status || response.status < 200 || response.status >= 300) {
    logger.error(`FastAPI returned non-success status: ${response.status}`);
    throw new Error(`FastAPI error: ${response.status} - ${JSON.stringify(response.data)}`);
  }

  logger.info('FastAPI analysis completed successfully');
  
  // Return the FastAPI response directly to frontend
  res.json(response.data);
});

export default router;