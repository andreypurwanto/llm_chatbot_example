import requests
from typing import List
from web_app.logs import LOG
from web_app.base.request_api import RequestAPI
from streamlit_app.constant import WEB_URL, WEB_AUTH
import json

class WebAPI(RequestAPI):
    def __init__(self, url: str = WEB_URL):
        super().__init__(
            url=url,
            timeout=30,
            retry_count=1,
            notify=False
        )
    
    def fetch_models(self) -> List[str]:
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = self.get(self.url, endpoint='/v1/model', headers=headers)
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                return [model["name"] for model in data.get("data", [])]
        except requests.RequestException as e:
            LOG.error(f"Failed to fetch models: {e}")
        
        return []  # Default fallback to None (empty list)

    def fetch_prediction(self, model_name, query, conv_ext_id) -> str:
        endpoint = f"/v1/model/{model_name}/prediction_result"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': WEB_AUTH
        }
        payload = json.dumps({"query": query, "conv_ext_id": conv_ext_id})
        
        try:
            response = self.post(self.url, endpoint=endpoint, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                return data["data"].get("result", "Maaf terjadi kendala di Sistem Kami, Mohon Tunggu beberapa saat.")
        except requests.RequestException as e:
            LOG.error(f"Failed to fetch prediction: {e}")
        
        return "Maaf terjadi kendala di Sistem Kami, Mohon Tunggu beberapa saat."
    
    def send_review(self, rating, feedback, conv_ext_id) -> None:
        endpoint = "/v1/review"
        payload = json.dumps({
            "star": 1 if rating == "Like" else 0,
            "feedback": feedback if feedback else "",
            "conv_ext_id": conv_ext_id
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': WEB_AUTH
        }

        response = self.post(self.url, endpoint=endpoint, headers=headers, data=payload)

        try:
            response = requests.post(self.url, headers=headers, data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            LOG.error(f"Failed to send review: {e}")
