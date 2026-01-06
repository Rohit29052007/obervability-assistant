import requests
import json
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class PrometheusClient:
    """Simple Prometheus API client for Day 2"""
    
    def __init__(self, base_url: str = "http://localhost:9090"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 10
        
    def test_connection(self) -> bool:
        """Test if Prometheus is reachable"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/label/__name__/values",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Prometheus connection failed: {e}")
            return False
    
    def query(self, promql: str) -> Dict[str, Any]:
        """Execute a PromQL query"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/query",
                params={'query': promql}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Prometheus query failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": {"result": []}
            }
    
    def query_range(self, promql: str, start: str, end: str, step: str = "15s") -> Dict[str, Any]:
        """Execute range query for graphs"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/query_range",
                params={
                    'query': promql,
                    'start': start,
                    'end': end,
                    'step': step
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Prometheus range query failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": {"result": []}
            }
    
    def get_available_metrics(self) -> List[str]:
        """Get list of all metric names"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/label/__name__/values")
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return []
    
    def get_label_values(self, label_name: str) -> List[str]:
        """Get values for a specific label"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/label/{label_name}/values")
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            logger.error(f"Failed to get label values: {e}")
            return []

# Create a global instance
prometheus_client = PrometheusClient()