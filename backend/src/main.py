"""
Banking App Backend - Transaction History Feature
FastAPI application main module
"""

import logging
import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .api import transaction_router, account_router
from .middleware.cors import setup_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application instance
app = FastAPI(
    title="Banking App API",
    description="Transaction History API for Banking App Prototype",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True  # Enable debug mode for detailed error messages
)

# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions with detailed logging"""
    logger.error(f"Unhandled exception occurred: {str(exc)}")
    logger.error(f"Exception type: {type(exc).__name__}")
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error": str(exc),
            "type": type(exc).__name__,
            "path": str(request.url.path),
            "method": request.method,
            "traceback": traceback.format_exc() if app.debug else None
        }
    )

# HTTP exception handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with detailed logging"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    logger.warning(f"Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path),
            "method": request.method
        }
    )

# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed logging"""
    logger.warning(f"Validation error: {exc.errors()}")
    logger.warning(f"Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation Error",
            "errors": exc.errors(),
            "path": str(request.url.path),
            "method": request.method
        }
    )

# Setup middleware (includes CORS and other middleware)
setup_middleware(app)

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and perform startup tasks"""
    logger.info("Application starting up...")
    try:
        from .database.connection import create_tables
        from .database.sample_data import create_sample_data
        
        logger.info("Initializing database tables...")
        create_tables()
        logger.info("Database initialization completed successfully")
        
        logger.info("Creating sample data if needed...")
        create_sample_data()
        logger.info("Sample data initialization completed")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Don't raise here to allow app to start even with DB issues for debugging
        
# Include API routers
app.include_router(transaction_router, prefix="/api", tags=["transactions"])
app.include_router(account_router, prefix="/api", tags=["accounts"])

@app.get("/")
async def root():
    """Root endpoint for API health check"""
    return {"message": "Banking App API is running", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "banking-app-backend"}

@app.get("/api/health")
async def api_health_check():
    """API health check endpoint"""
    return {"status": "healthy", "api": "banking-transactions", "version": "0.1.0"}