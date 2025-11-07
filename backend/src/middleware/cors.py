"""
CORS Middleware Configuration
Cross-Origin Resource Sharing setup for Banking App
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from typing import Callable
from ..config.settings import settings

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Custom logging middleware for request/response logging"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} | "
            f"Time: {process_time:.3f}s | "
            f"Path: {request.url.path}"
        )
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # API version header
        response.headers["X-API-Version"] = "1.0.0"
        
        return response


def add_cors_middleware(app: FastAPI) -> None:
    """Add CORS middleware with proper configuration"""
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language", 
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
        ],
        expose_headers=[
            "X-Process-Time",
            "X-API-Version",
        ],
    )


def add_security_middleware(app: FastAPI) -> None:
    """Add security-related middleware"""
    
    # Trusted host middleware
    if not settings.is_development:
        app.add_middleware(
            TrustedHostMiddleware, 
            allowed_hosts=settings.security.allowed_hosts
        )
    
    # Security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)


def add_performance_middleware(app: FastAPI) -> None:
    """Add performance-related middleware"""
    # GZip compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Request logging middleware
    app.add_middleware(LoggingMiddleware)


def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware in correct order"""
    # Order matters: last added is executed first
    
    # 1. Performance middleware (innermost)
    add_performance_middleware(app)
    
    # 2. Security middleware
    add_security_middleware(app)
    
    # 3. CORS middleware (outermost)
    add_cors_middleware(app)