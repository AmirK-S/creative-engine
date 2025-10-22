import os
import requests

class StabilityAIClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Stability AI API key is required.")
        self.api_key = api_key
        self.api_host = "https://api.stability.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

    def generate_image(self, prompt: str, negative_prompt: str = "", width: int = 1024, height: int = 1024) -> bytes | None:
        endpoint = "/v2beta/stable-image/generate/core"
        url = f"{self.api_host}{endpoint}"

        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "output_format": "png"
        }
        
        print(f"Generating image for prompt: '{prompt[:70]}...'")
        try:
            response = requests.post(url, headers=self.headers, data=data, timeout=180)
            response.raise_for_status()
            
            if response.headers.get("finish-reason") == 'SUCCESS':
                return response.content
            else:
                print(f"Warning: Generation failed with reason: {response.headers.get('finish-reason')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error during image generation: {e}")
            return None