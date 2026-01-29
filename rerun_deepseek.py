"""
Re-run DeepSeek prompts with higher token limit
"""
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

PROMPTS = {
    "animation": "Create an animation with three spinning hexagons that are nested one inside the next. Each hexagon is missing one side. There are little bouncy balls that start in the very center and bounce around until they fall out. Make the physics real with friction and bouncing. Don't use any external libraries. Make the final output fit in an 800x400 iframe.",
    "flow": "Create a deterministic animated flow-field visualization. Use a smooth noise-based vector field to drive at least 10,000 particles. Particles should leave fading trails and move continuously without jitter. The animation must be reproducible from a single integer seed and run smoothly for at least 30 seconds. Don't use any external libraries. Make the final output fit in an 800x400 iframe.",
    "pendulum": "Create an animation of a double pendulum using only your own physics implementation (no external physics engines). Simulate the system in continuous time, render the motion smoothly, and draw a trailing path for the second mass. Color the trail based on instantaneous angular velocity. The animation should clearly show chaotic behavior over time and remain numerically stable for at least 30 seconds. Don't use any external libraries. Make the final output fit in an 800x400 iframe.",
    "traffic": "Simulate and animate urban traffic in a small city from a top-down view. The city is a graph of intersections and roads with traffic lights; vehicles are autonomous agents with random origins and destinations that move continuously and follow only local rules (speed limits, following distance, red lights). Traffic congestion must emerge naturally, with queues and stop-and-go waves, not hard-coded behavior. Midway through the simulation, change one policy variable (e.g., signal timing or road capacity) and make the system-level effect clearly visible. Don't use any external libraries. Make the final output fit in an 800x400 iframe.",
}

def extract_html(response_text):
    """Extract HTML from markdown code blocks or return as-is."""
    # Try to find HTML in code blocks
    match = re.search(r'```html\s*(<!DOCTYPE html>.*?</html>)\s*```', response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r'```(?:html)?\s*(<!DOCTYPE html>.*?</html>)\s*```', response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    # If response starts with <!DOCTYPE or <html, return as-is
    if response_text.strip().lower().startswith('<!doctype') or response_text.strip().lower().startswith('<html'):
        return response_text.strip()
    # Last resort: find any HTML-like content
    match = re.search(r'(<!DOCTYPE html>.*?</html>)', response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return response_text

def call_deepseek(prompt: str) -> dict:
    """Call DeepSeek API with higher token limit."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 8192,  # Higher limit
        },
        timeout=180,
    )
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return {"content": extract_html(content), "usage": usage}

if __name__ == "__main__":
    app_dir = os.path.dirname(os.path.abspath(__file__))

    for prompt_name, prompt_text in PROMPTS.items():
        print(f"\n{'='*60}")
        print(f"Running DeepSeek: {prompt_name}")
        print(f"{'='*60}")

        print(f"[DeepSeek V3.2] Calling API with max_tokens=8192...")
        try:
            result = call_deepseek(prompt_text)
            filepath = os.path.join(app_dir, f"{prompt_name}_deepseek.html")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(result["content"])
            print(f"  Saved to {prompt_name}_deepseek.html")
            print(f"  Usage: {result['usage']}")
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\n{'='*60}")
    print("Done!")
    print(f"{'='*60}")
