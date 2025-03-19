import requests
import os
import asyncio
from .file_service import load_prompt_from_file
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("AZURE_GPT_API_KEY")
api_endpoint = os.getenv("AZURE_GPT_API_ENDPOINT")

def create_prompt(description, image_base64=None, image_url=None):
    if image_base64 or image_url:
        prompt = load_prompt_from_file(r'C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\backend\src\templates\image_prompt.txt')
    else:
        prompt = load_prompt_from_file(r'C:\Users\GT0730-1\Documents\GitHub\Ads-Gen\backend\src\templates\text_prompt.txt')

    prompt += "\n\nDescription:\n" + description
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
        "model": "gpt-4o-mini",
        "api-version": "2024-02-01",
    }

    messages = [
        {"role": "system", "content": "You are a creative assistant."},
        {"role": "user", "content": [{"type": "text", "text": prompt}]},
    ]
    
    if image_url:
        messages[1]["content"].append(
                {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}}
            )
    elif image_base64:
        messages[1]["content"].append(
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            )
        
    data = {
        "temperature": 0.8,
        "top_p": 0.6,
        "max_tokens": 4000,
        "messages": messages,
    }
    response = requests.post(api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        generated_content = response_data['choices'][0]['message']['content']
        return {generated_content}
    else:
        raise Exception(f"Failed to generate prompt: {response.text}")
    