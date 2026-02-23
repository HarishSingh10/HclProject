import requests
import streamlit as st
from typing import Optional, Dict, Any
import json

BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8000")

class APIClient:
    
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url.rstrip("/")
    
    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            if response.status_code == 401:
                raise Exception("Unauthorized. Please log in again.")
            elif response.status_code == 403:
                raise Exception("Access denied. Insufficient permissions.")
            elif response.status_code == 404:
                raise Exception("Resource not found.")
            elif response.status_code >= 500:
                raise Exception("Server error. Please try again later.")
            elif response.status_code >= 400:
                error_data = response.json()
                raise Exception(error_data.get("detail", "Request failed"))
            
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception("Invalid response from server")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to backend at {self.base_url}")
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"email": email, "password": password},
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Login failed: {str(e)}")
    
    def create_ticket(self, description: str, category: str, priority: str, token: str) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/tickets",
                json={
                    "description": description,
                    "category": category,
                    "priority": priority
                },
                headers=self._get_headers(token),
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create ticket: {str(e)}")
    
    def get_recommendations(self, ticket_id: str, token: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/recommend/{ticket_id}",
                headers=self._get_headers(token),
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch recommendations: {str(e)}")
    
    def get_user_tickets(self, token: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/my-tickets",
                headers=self._get_headers(token),
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch tickets: {str(e)}")
    
    def update_ticket_status(self, ticket_id: str, status: str, token: str) -> Dict[str, Any]:
        try:
            response = requests.patch(
                f"{self.base_url}/tickets/{ticket_id}",
                json={"status": status},
                headers=self._get_headers(token),
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update ticket: {str(e)}")
    
    def get_admin_stats(self, token: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/admin/stats",
                headers=self._get_headers(token),
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch admin stats: {str(e)}")
    
    def get_admin_tickets(self, token: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/admin/tickets",
                headers=self._get_headers(token),
                timeout=10
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch admin tickets: {str(e)}")


api_client = APIClient()
