import requests
import asyncio

#Placeholder values for now
async def invoke_gpt_async(prompt: str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, invoke_llm, prompt)

def invoke_llm(prompt: str):
    response = requests.post("LLM_API_ENDPOINT", json={"prompt": prompt})
    if response.status_code == 200:
        return response.json().get("response")
    else:
        raise Exception("Failed to get response from LLM")

def construct_llm_prompt(template: str, category: str):
    # Construct a prompt using csv file
    return template.replace("{category}", category)