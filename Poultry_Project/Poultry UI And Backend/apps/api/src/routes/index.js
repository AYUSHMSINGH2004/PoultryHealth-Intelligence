import { Router } from 'express';
import healthCheck from './health-check.js';
import analyzeRouter from './analyze.js';

const router = Router();

export default () => {
    router.get('/health', healthCheck);
    router.use('/analyze', analyzeRouter);

    return router;
};