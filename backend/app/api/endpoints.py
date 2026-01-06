from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
import time

# Import the Prometheus client
from app.prometheus.client import prometheus_client

router = APIRouter(prefix="/api", tags=["API"])

@router.get("/health")
async def health_check():
    """Check backend and Prometheus health"""
    prometheus_healthy = prometheus_client.test_connection()
    
    return {
        "backend": "healthy",
        "prometheus": "healthy" if prometheus_healthy else "unhealthy",
        "timestamp": time.time()
    }

@router.get("/test-prometheus")
async def test_prometheus():
    """Test Prometheus connection and get sample data"""
    is_connected = prometheus_client.test_connection()
    metrics = []
    
    if is_connected:
        metrics = prometheus_client.get_available_metrics()[:5]
    
    return {
        "prometheus_connected": is_connected,
        "available_metrics_sample": metrics,
        "message": "Prometheus is connected" if is_connected else "Cannot connect to Prometheus"
    }

@router.post("/translate")
async def translate_query(query_data: Dict[str, Any]):
    """Translate natural language to PromQL"""
    user_query = query_data.get("query", "").lower()
    
    # Simple hardcoded translations for Day 2
    if "cpu" in user_query:
        promql = 'container_cpu_usage_seconds_total'
    elif "memory" in user_query:
        promql = 'container_memory_usage_bytes'
    elif "http" in user_query:
        promql = 'http_requests_total'
    else:
        promql = 'up'  # Default Prometheus metric
    
    return {
        "status": "success",
        "original_query": user_query,
        "promql": promql,
        "explanation": f"Translated to {promql}",
        "confidence": 0.8
    }

@router.get("/execute")
async def execute_query(
    promql: str = Query(..., description="PromQL query to execute"),
    start: Optional[str] = None,
    end: Optional[str] = None,
    step: Optional[str] = "15s"
):
    """Execute a PromQL query"""
    if not promql:
        raise HTTPException(status_code=400, detail="No query provided")
    
    try:
        if start and end:
            result = prometheus_client.query_range(promql, start, end, step)
        else:
            result = prometheus_client.query(promql)
        
        return {
            "status": "success",
            "query": promql,
            "result": result,
            "executed_at": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@router.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "API is working",
        "timestamp": time.time(),
        "endpoints": [
            "/api/health",
            "/api/test-prometheus",
            "/api/translate (POST)",
            "/api/execute"
        ]
    }