import os
import json
import httpx
from termcolor import cprint
import asyncio

# Constants
API_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "deepseek/deepseek-r1"
API_KEY = os.getenv("OPENROUTER_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

async def call_deepseek(prompt: str):
    """
    Calls the DeepSeek API with streaming for both content and reasoning.
    """
    try:
        cprint("\n[1/2] 📡 Calling DeepSeek API... (Streaming)", "cyan")
        async with httpx.AsyncClient() as client:
            payload = {
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
                "include_reasoning": True
            }
            async with client.stream("POST", f"{API_BASE_URL}/chat/completions", headers=HEADERS, json=payload) as response:
                response.raise_for_status()
                content_stream = ""
                reasoning_stream = ""
                has_started_content = False
                
                # Print a nice header
                print("\n" + "="*50)
                cprint("🤖 DeepSeek Response", "blue", attrs=['bold'])
                print("="*50)
                
                # Print reasoning section header first
                print("\n" + "-"*30)
                cprint("🤔 Reasoning Process:", "yellow", attrs=['bold'])
                print("-"*30 + "\n")
                
                async for chunk in response.aiter_lines():
                    if chunk:
                        try:
                            if chunk.startswith("data: "):
                                chunk = chunk[6:]
                            
                            chunk_stripped = chunk.strip()
                            if not chunk_stripped.startswith('{'):
                                if "DONE" not in chunk and chunk_stripped != ": OPENROUTER PROCESSING":
                                    cprint(f"\nℹ️  Skipping non-JSON chunk: {chunk_stripped}", "yellow")
                                continue

                            json_chunk = json.loads(chunk)
                            if 'choices' in json_chunk and json_chunk['choices']:
                                delta = json_chunk['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                reasoning = delta.get('reasoning', '')

                                if content:
                                    # Print content header if this is the first content chunk
                                    if not has_started_content:
                                        print("\n\n" + "-"*30)
                                        cprint("💭 Final Answer:", "cyan", attrs=['bold'])
                                        print("-"*30 + "\n")
                                        has_started_content = True
                                    
                                    # Stream content in cyan
                                    cprint(content, 'cyan', end="", flush=True)
                                    content_stream += content
                                if reasoning:
                                    # Stream reasoning in yellow
                                    cprint(reasoning, 'yellow', end="", flush=True)
                                    reasoning_stream += reasoning
                        except json.JSONDecodeError as e:
                            continue

                # Print a nice footer
                print("\n" + "="*50)
                cprint("[2/2] ✅ Response Complete!", "green", attrs=['bold'])
                print("="*50 + "\n")
                
                return {
                    "content": content_stream.strip(),
                    "reasoning": reasoning_stream.strip()
                }
    except httpx.HTTPError as e:
        cprint(f"\n⚠️ HTTPError: {e}", "red")
        return None
    except Exception as e:
        cprint(f"\n⚠️ Error: {str(e)}", "red")
        return None

if __name__ == "__main__":

    asyncio.run(call_deepseek("What is 2+2?"))
