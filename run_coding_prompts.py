"""
Run coding prompts 3-6 against GPT-5.2, Gemini 3 Pro, and DeepSeek V3.2
"""
import os
import re
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Prompts - minimal output, no extra UI
SUFFIX = " Don't use external libraries. Output only the code. Don't include any additional text or comments. Don't have any sliders or user interface. Make the whole output fit within a 250x400px frame."

PROMPTS = {
    "hexagon": "Create an animation with three spinning hexagons that are nested one inside the next. Each hexagon is missing one side. There are little bouncy balls that start in the very center and bounce around until they fall out. Make the physics real with friction and bouncing. Add new balls continuously." + SUFFIX,
    "flow": "Create a deterministic animated flow-field visualization. Use a smooth noise-based vector field to drive around 2,000 particles. Particles should leave fading trails and move continuously without jitter. Use curl noise to ensure particles don't converge into sinks. Normalize the velocity vectors so all particles move at constant speed. The animation must be reproducible from a single integer seed and run continuously. Introduce a small time-varying or curl component to the vector field so particle motion remains circulating rather than collapsing into sinks." + SUFFIX,
    "pendulum": "Create an animation of a double pendulum swinging freely with normal gravity and inertia using only your own physics implementation (no external physics engines). Simulate the system in continuous time, render the motion smoothly, and draw a trailing path for the second mass. Color the trail based on instantaneous angular velocity. Start the pendulum near the top. Use real-world parameters and have the animation run at real-world speed (no slow-motion). Give the pendulum a hard push every 10 seconds." + SUFFIX,
    "traffic": "Create an animation of simualted urban traffic from a top-down view. The city is a 10x10 street grid with traffic lights. Vehicles are autonomous agents with random origins and destinations that move continuously and follow only local rules (speed limits, following distance, red lights). Traffic congestion must emerge naturally, with queues and stop-and-go waves, not hard-coded behavior." + SUFFIX,
    "blocks": "Create an HTML-only game where there are 10 blocks of different shapes and sizes scattered on the ground. You have to move the blocks and stack them into a tower without it falling over. Every few seconds, there's a mild earthquake. Use normal friction and gravity. Don't use external libraries. Output only the code. Make the whole output fit within a 200x300px frame.",
    "minesweeper": "Create a fully playable Minesweeper game. Include a grid of cells that can be clicked to reveal what's underneath. Some cells contain mines, others show numbers indicating adjacent mines. Right-click to flag potential mines. Include win/lose conditions and a reset button." + SUFFIX,
}

def extract_html(response_text):
    """Extract HTML from markdown code blocks or return as-is."""
    text = response_text.strip()

    # Try to find complete HTML document in code blocks
    match = re.search(r'```(?:html)?\s*(<!DOCTYPE html>.*?</html>)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Try without DOCTYPE
    match = re.search(r'```(?:html)?\s*(<html.*?</html>)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Strip leading ```html or ``` markers
    text = re.sub(r'^```(?:html)?\s*', '', text, flags=re.IGNORECASE)
    # Strip trailing ``` markers
    text = re.sub(r'\s*```\s*$', '', text)
    text = text.strip()

    # If it now starts with <!DOCTYPE or <html, return it
    if text.lower().startswith('<!doctype') or text.lower().startswith('<html'):
        return text

    # Find any complete HTML document
    match = re.search(r'(<!DOCTYPE html>.*?</html>)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Try to find partial HTML (canvas + script) and wrap it
    match = re.search(r'(<canvas.*?</script>)', text, re.DOTALL | re.IGNORECASE)
    if match:
        partial = match.group(1)
        return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>* {{ margin: 0; padding: 0; }} body {{ background: #0a0a14; overflow: hidden; }} canvas {{ display: block; }}</style>
</head>
<body>
{partial}
</body>
</html>'''
    return text

def call_openai(prompt: str) -> dict:
    """Call OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-5.2",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=300,
    )
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return {"content": extract_html(content), "usage": usage}

def call_gemini(prompt: str) -> dict:
    """Call Google Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent?key={api_key}",
        json={
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        },
        timeout=300,
    )
    data = response.json()
    content = data["candidates"][0]["content"]["parts"][0]["text"]
    usage = data.get("usageMetadata", {})
    return {"content": extract_html(content), "usage": usage}

def call_deepseek(prompt: str) -> dict:
    """Call DeepSeek API."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek-reasoner",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=300,
    )
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return {"content": extract_html(content), "usage": usage}

def call_kimi(prompt: str) -> dict:
    """Call Kimi (Moonshot) API."""
    api_key = os.getenv("KIMI_API_KEY")
    response = requests.post(
        "https://api.moonshot.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "kimi-k2.5",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=300,
    )
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return {"content": extract_html(content), "usage": usage}

def call_qwen(prompt: str) -> dict:
    """Call Qwen API (US-Virginia endpoint) - uses coder model for coding prompts."""
    api_key = os.getenv("QWEN_API_KEY")
    response = requests.post(
        "https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "qwen3-coder-plus",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=300,
    )
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return {"content": extract_html(content), "usage": usage}

MODELS = {
    "gpt": ("GPT-5.2", call_openai),
    "gemini": ("Gemini 3 Pro", call_gemini),
    "deepseek": ("DeepSeek V3.2", call_deepseek),
    "kimi": ("Kimi K2.5", call_kimi),
    "qwen": ("Qwen3-Coder-Plus", call_qwen),
}

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Run coding prompts against AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_coding_prompts.py                           # Run all prompts, all models
  python run_coding_prompts.py -p animation flow         # Run only animation and flow prompts
  python run_coding_prompts.py -m gpt deepseek           # Run only GPT and DeepSeek
  python run_coding_prompts.py -p traffic -m gemini      # Run traffic prompt on Gemini only
  python run_coding_prompts.py --list                    # Show available prompts and models
        """
    )
    parser.add_argument("-p", "--prompts", nargs="+", choices=list(PROMPTS.keys()),
                        help="Prompts to run (default: all)")
    parser.add_argument("-m", "--models", nargs="+", choices=list(MODELS.keys()),
                        help="Models to test (default: all)")
    parser.add_argument("--list", action="store_true",
                        help="List available prompts and models")
    args = parser.parse_args()

    if args.list:
        print("Available prompts:", ", ".join(PROMPTS.keys()))
        print("Available models:", ", ".join(MODELS.keys()))
        sys.exit(0)

    selected_prompts = args.prompts or list(PROMPTS.keys())
    selected_models = args.models or list(MODELS.keys())

    app_dir = os.path.dirname(os.path.abspath(__file__))
    stats_file = os.path.join(app_dir, "stats.json")

    # Load existing stats or create new
    if os.path.exists(stats_file):
        with open(stats_file, "r") as f:
            all_stats = json.load(f)
    else:
        all_stats = {}

    print(f"Running prompts: {', '.join(selected_prompts)}")
    print(f"Testing models: {', '.join(selected_models)}")

    total_prompts = len(selected_prompts)
    for i, prompt_name in enumerate(selected_prompts, 1):
        prompt_text = PROMPTS[prompt_name]
        print(f"\n{'='*60}")
        print(f"[{i}/{total_prompts}] Running: {prompt_name}")
        print(f"{'='*60}")
        sys.stdout.flush()

        if prompt_name not in all_stats:
            all_stats[prompt_name] = {}

        for model_key in selected_models:
            model_name, model_func = MODELS[model_key]
            print(f"\n[{model_name}] Starting API call...", end=" ", flush=True)
            try:
                start_time = time.time()
                result = model_func(prompt_text)
                elapsed = time.time() - start_time

                filepath = os.path.join(app_dir, f"{prompt_name}_{model_key}.html")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(result["content"])
                print(f"Done! ({elapsed:.1f}s)")
                print(f"  Saved to {prompt_name}_{model_key}.html")
                print(f"  Usage: {result['usage']}")

                # Save stats
                all_stats[prompt_name][model_key] = {
                    "usage": result["usage"],
                    "time_seconds": round(elapsed, 1)
                }
            except Exception as e:
                print(f"ERROR!")
                print(f"  {e}")
            sys.stdout.flush()

    # Save stats to JSON
    with open(stats_file, "w") as f:
        json.dump(all_stats, f, indent=2)
    print(f"\nStats saved to stats.json")

    print(f"\n{'='*60}")
    print("Done! All selected prompts processed.")
    print(f"{'='*60}")
