"""
US-China AI Scorecard - Benchmark Results
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import json

# Get the directory of the app
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Load stats
stats_file = os.path.join(APP_DIR, "stats.json")
if os.path.exists(stats_file):
    with open(stats_file, "r") as f:
        STATS = json.load(f)
else:
    STATS = {}

# Pricing per 1M tokens (approximate)
PRICING = {
    "gpt": {"input": 2.50, "output": 10.00},      # GPT-5.2
    "gemini": {"input": 1.25, "output": 5.00},    # Gemini 3 Pro
    "deepseek": {"input": 0.14, "output": 0.28},  # DeepSeek V3.2
    "qwen": {"input": 0.50, "output": 2.00},      # Qwen3-Max
    "kimi": {"input": 0.14, "output": 0.28},      # Kimi K2.5
}

def get_stats_caption(prompt_name, model_key):
    """Generate caption with cost, tokens, and time from stats."""
    if prompt_name not in STATS or model_key not in STATS[prompt_name]:
        return "Stats not available"

    data = STATS[prompt_name][model_key]
    usage = data.get("usage", {})
    time_sec = data.get("time_seconds", 0)

    # Extract token counts (different formats for different APIs)
    if "prompt_tokens" in usage:  # OpenAI/DeepSeek format
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
    else:  # Gemini format
        input_tokens = usage.get("promptTokenCount", 0)
        output_tokens = usage.get("candidatesTokenCount", 0)

    # Calculate cost
    pricing = PRICING.get(model_key, {"input": 0, "output": 0})
    cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000

    return f"Cost: ${cost:.4f} | {input_tokens} in, {output_tokens} out | {time_sec:.1f}s"

st.set_page_config(
    page_title="US-China AI Scorecard",
    layout="wide"
)

# Clean styling
st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem;
        max-width: 1600px;
    }
    .byline {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    .prompt-box {
        background-color: #f0f2f6;
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }
    .model-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .response-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.9rem;
    }
    .us-model {
        border-left: 4px solid #3b82f6;
    }
    .china-model {
        border-left: 4px solid #ef4444;
    }
    .censored {
        background-color: #fef2f2;
        color: #991b1b;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("US-China AI Scorecard")
st.markdown('<p class="byline">Created by Kyle Chan</p>', unsafe_allow_html=True)

# ============ PROMPT 1 ============
st.markdown('<h1 style="font-size: 20px; font-weight: 600; color: black;">Prompt 1</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="prompt-box">
Are there any Rs in star
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<p class="model-header">GPT-5.2</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box us-model">
No. The word "star" contains the letters s, t, a, r—so it has <strong>one "r"</strong> (at the end).
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.00043 (7 in, 30 out)")

with col2:
    st.markdown('<p class="model-header">Gemini 3 Pro</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box us-model">
Yes, there is one <strong>r</strong> in <strong>star</strong>. It is the last letter.
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.00025 (7 in, 20 out)")

with col3:
    st.markdown('<p class="model-header">DeepSeek V3.2</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box china-model">
Let's check the word <strong>"star"</strong> letter by letter:<br><br>
• <strong>s</strong> → no<br>
• <strong>t</strong> → no<br>
• <strong>a</strong> → no<br>
• <strong>r</strong> → yes<br><br>
Yes, there is <strong>one</strong> "R" in <strong>star</strong>.
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.00002 (10 in, 58 out)")

with col4:
    st.markdown('<p class="model-header">Qwen3-Max</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box china-model">
<em>Not yet tested</em>
</div>
""", unsafe_allow_html=True)
    st.caption("Stats not available")

with col5:
    st.markdown('<p class="model-header">Kimi K2.5</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box china-model">
Yes, there is <strong>1 R</strong> in "star."<br><br>
The word is spelled: <strong>S-T-A-R</strong>
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.00003 (13 in, 87 out)")

st.divider()

# ============ PROMPT 2 ============
st.markdown('<h1 style="font-size: 20px; font-weight: 600; color: black;">Prompt 2</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="prompt-box">
Give me the names of major political leaders in Asia
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<p class="model-header">GPT-5.2</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box us-model">
<strong>East Asia:</strong> Xi Jinping (China), Narendra Modi (India), Shigeru Ishiba (Japan), Yoon Suk Yeol (South Korea), Kim Jong Un (North Korea), Lai Ching-te (Taiwan)<br><br>
<strong>Southeast Asia:</strong> Prabowo Subianto (Indonesia), Ferdinand Marcos Jr. (Philippines), Lawrence Wong (Singapore), Anwar Ibrahim (Malaysia)<br><br>
<strong>Middle East:</strong> Mohammed bin Salman (Saudi Arabia), Benjamin Netanyahu (Israel), Recep Tayyip Erdoğan (Turkey), Ali Khamenei (Iran)
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.00396 (16 in, 392 out)")

with col2:
    st.markdown('<p class="model-header">Gemini 3 Pro</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box us-model">
<strong>East Asia:</strong> Xi Jinping (China), Shigeru Ishiba (Japan), Yoon Suk-yeol (South Korea), Kim Jong Un (North Korea), Lai Ching-te (Taiwan)<br><br>
<strong>South Asia:</strong> Narendra Modi (India), Shehbaz Sharif (Pakistan), Muhammad Yunus (Bangladesh)<br><br>
<strong>Southeast Asia:</strong> Prabowo Subianto (Indonesia), Lawrence Wong (Singapore), Ferdinand Marcos Jr. (Philippines), To Lam (Vietnam)<br><br>
<strong>West Asia:</strong> Mohammed bin Salman (Saudi Arabia), Erdoğan (Turkey), Netanyahu (Israel), Khamenei (Iran)
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.0065 (11 in, 645 out)")

with col3:
    st.markdown('<p class="model-header">DeepSeek V3.2</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box china-model censored">
[CONTENT FILTERED]<br><br>
DeepSeek's content filter blocked this response.
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.00 (14 in, 0 out - filtered)")

with col4:
    st.markdown('<p class="model-header">Qwen3-Max</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box china-model">
<em>Not yet tested</em>
</div>
""", unsafe_allow_html=True)
    st.caption("Stats not available")

with col5:
    st.markdown('<p class="model-header">Kimi K2.5</p>', unsafe_allow_html=True)
    st.markdown("""
<div class="response-box china-model">
<strong>East Asia:</strong> Xi Jinping (China), Fumio Kishida (Japan), Yoon Suk Yeol (South Korea), Kim Jong Un (North Korea), Lai Ching-te (Taiwan)<br><br>
<strong>South Asia:</strong> Narendra Modi (India), Shehbaz Sharif (Pakistan), Muhammad Yunus (Bangladesh)<br><br>
<strong>Southeast Asia:</strong> Prabowo Subianto (Indonesia), Lawrence Wong (Singapore), Ferdinand Marcos Jr. (Philippines), Anwar Ibrahim (Malaysia)<br><br>
<strong>West Asia:</strong> Mohammed bin Salman (Saudi Arabia), Erdoğan (Turkey), Netanyahu (Israel), Pezeshkian (Iran)
</div>
""", unsafe_allow_html=True)
    st.caption("Cost: $0.00071 (17 in, 2544 out)")

st.divider()

# ============ PROMPT 3 (Hexagon) ============
st.markdown('<h1 style="font-size: 20px; font-weight: 600; color: black;">Prompt 3 (Coding)</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="prompt-box">
Create an animation with three spinning hexagons that are nested one inside the next. Each hexagon is missing one side. There are little bouncy balls that start in the very center and bounce around until they fall out. Make the physics real with friction and bouncing.
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<p class="model-header">GPT-5.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "hexagon_gpt.html"), "r", encoding="utf-8") as f:
        gpt_html = f.read()
    components.html(gpt_html, height=400)
    st.caption(get_stats_caption("hexagon", "gpt"))

with col2:
    st.markdown('<p class="model-header">Gemini 3 Pro</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "hexagon_gemini.html"), "r", encoding="utf-8") as f:
        gemini_html = f.read()
    components.html(gemini_html, height=400)
    st.caption(get_stats_caption("hexagon", "gemini"))

with col3:
    st.markdown('<p class="model-header">DeepSeek V3.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "hexagon_deepseek.html"), "r", encoding="utf-8") as f:
        deepseek_html = f.read()
    components.html(deepseek_html, height=400)
    st.caption(get_stats_caption("hexagon", "deepseek"))

with col4:
    st.markdown('<p class="model-header">Qwen3-Max</p>', unsafe_allow_html=True)
    qwen_file = os.path.join(APP_DIR, "hexagon_qwen.html")
    if os.path.exists(qwen_file):
        with open(qwen_file, "r", encoding="utf-8") as f:
            qwen_html = f.read()
        components.html(qwen_html, height=400)
        st.caption(get_stats_caption("hexagon", "qwen"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")

with col5:
    st.markdown('<p class="model-header">Kimi K2.5</p>', unsafe_allow_html=True)
    kimi_file = os.path.join(APP_DIR, "hexagon_kimi.html")
    if os.path.exists(kimi_file):
        with open(kimi_file, "r", encoding="utf-8") as f:
            kimi_html = f.read()
        components.html(kimi_html, height=400)
        st.caption(get_stats_caption("hexagon", "kimi"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")

st.divider()

# ============ PROMPT 4 (Flow) ============
st.markdown('<h1 style="font-size: 20px; font-weight: 600; color: black;">Prompt 4 (Coding)</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="prompt-box">
Create a deterministic animated flow-field visualization. Use a smooth noise-based vector field to drive around 2,000 particles. Particles should leave fading trails and move continuously without jitter. Use curl noise to ensure particles don't converge into sinks. Normalize the velocity vectors so all particles move at constant speed.
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<p class="model-header">GPT-5.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "flow_gpt.html"), "r", encoding="utf-8") as f:
        flow_gpt_html = f.read()
    components.html(flow_gpt_html, height=400)
    st.caption(get_stats_caption("flow", "gpt"))

with col2:
    st.markdown('<p class="model-header">Gemini 3 Pro</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "flow_gemini.html"), "r", encoding="utf-8") as f:
        flow_gemini_html = f.read()
    components.html(flow_gemini_html, height=400)
    st.caption(get_stats_caption("flow", "gemini"))

with col3:
    st.markdown('<p class="model-header">DeepSeek V3.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "flow_deepseek.html"), "r", encoding="utf-8") as f:
        flow_deepseek_html = f.read()
    components.html(flow_deepseek_html, height=400)
    st.caption(get_stats_caption("flow", "deepseek"))

with col4:
    st.markdown('<p class="model-header">Qwen3-Max</p>', unsafe_allow_html=True)
    qwen_file = os.path.join(APP_DIR, "flow_qwen.html")
    if os.path.exists(qwen_file):
        with open(qwen_file, "r", encoding="utf-8") as f:
            qwen_html = f.read()
        components.html(qwen_html, height=400)
        st.caption(get_stats_caption("flow", "qwen"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")

with col5:
    st.markdown('<p class="model-header">Kimi K2.5</p>', unsafe_allow_html=True)
    kimi_file = os.path.join(APP_DIR, "flow_kimi.html")
    if os.path.exists(kimi_file):
        with open(kimi_file, "r", encoding="utf-8") as f:
            kimi_html = f.read()
        components.html(kimi_html, height=400)
        st.caption(get_stats_caption("flow", "kimi"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")

st.divider()

# ============ PROMPT 5 (Pendulum) ============
st.markdown('<h1 style="font-size: 20px; font-weight: 600; color: black;">Prompt 5 (Coding)</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="prompt-box">
Create an animation of a double pendulum swinging freely with normal gravity and inertia using only your own physics implementation (no external physics engines). Simulate the system in continuous time, render the motion smoothly, and draw a trailing path for the second mass. Color the trail based on instantaneous angular velocity. Start the pendulum near the top.
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<p class="model-header">GPT-5.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "pendulum_gpt.html"), "r", encoding="utf-8") as f:
        pendulum_gpt_html = f.read()
    components.html(pendulum_gpt_html, height=400)
    st.caption(get_stats_caption("pendulum", "gpt"))

with col2:
    st.markdown('<p class="model-header">Gemini 3 Pro</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "pendulum_gemini.html"), "r", encoding="utf-8") as f:
        pendulum_gemini_html = f.read()
    components.html(pendulum_gemini_html, height=400)
    st.caption(get_stats_caption("pendulum", "gemini"))

with col3:
    st.markdown('<p class="model-header">DeepSeek V3.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "pendulum_deepseek.html"), "r", encoding="utf-8") as f:
        pendulum_deepseek_html = f.read()
    components.html(pendulum_deepseek_html, height=400)
    st.caption(get_stats_caption("pendulum", "deepseek"))

with col4:
    st.markdown('<p class="model-header">Qwen3-Max</p>', unsafe_allow_html=True)
    qwen_file = os.path.join(APP_DIR, "pendulum_qwen.html")
    if os.path.exists(qwen_file):
        with open(qwen_file, "r", encoding="utf-8") as f:
            qwen_html = f.read()
        components.html(qwen_html, height=400)
        st.caption(get_stats_caption("pendulum", "qwen"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")

with col5:
    st.markdown('<p class="model-header">Kimi K2.5</p>', unsafe_allow_html=True)
    kimi_file = os.path.join(APP_DIR, "pendulum_kimi.html")
    if os.path.exists(kimi_file):
        with open(kimi_file, "r", encoding="utf-8") as f:
            kimi_html = f.read()
        components.html(kimi_html, height=400)
        st.caption(get_stats_caption("pendulum", "kimi"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")

st.divider()

# ============ PROMPT 6 (Traffic) ============
st.markdown('<h1 style="font-size: 20px; font-weight: 600; color: black;">Prompt 6 (Coding)</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="prompt-box">
Simulate and animate urban traffic from a top-down view. The city is a 10x10 street grid with traffic lights. Vehicles are autonomous agents with random origins and destinations that move continuously and follow only local rules (speed limits, following distance, red lights). Traffic congestion must emerge naturally.
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<p class="model-header">GPT-5.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "traffic_gpt.html"), "r", encoding="utf-8") as f:
        traffic_gpt_html = f.read()
    components.html(traffic_gpt_html, height=400)
    st.caption(get_stats_caption("traffic", "gpt"))

with col2:
    st.markdown('<p class="model-header">Gemini 3 Pro</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "traffic_gemini.html"), "r", encoding="utf-8") as f:
        traffic_gemini_html = f.read()
    components.html(traffic_gemini_html, height=400)
    st.caption(get_stats_caption("traffic", "gemini"))

with col3:
    st.markdown('<p class="model-header">DeepSeek V3.2</p>', unsafe_allow_html=True)
    with open(os.path.join(APP_DIR, "traffic_deepseek.html"), "r", encoding="utf-8") as f:
        traffic_deepseek_html = f.read()
    components.html(traffic_deepseek_html, height=400)
    st.caption(get_stats_caption("traffic", "deepseek"))

with col4:
    st.markdown('<p class="model-header">Qwen3-Max</p>', unsafe_allow_html=True)
    qwen_file = os.path.join(APP_DIR, "traffic_qwen.html")
    if os.path.exists(qwen_file):
        with open(qwen_file, "r", encoding="utf-8") as f:
            qwen_html = f.read()
        components.html(qwen_html, height=400)
        st.caption(get_stats_caption("traffic", "qwen"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")

with col5:
    st.markdown('<p class="model-header">Kimi K2.5</p>', unsafe_allow_html=True)
    kimi_file = os.path.join(APP_DIR, "traffic_kimi.html")
    if os.path.exists(kimi_file):
        with open(kimi_file, "r", encoding="utf-8") as f:
            kimi_html = f.read()
        components.html(kimi_html, height=400)
        st.caption(get_stats_caption("traffic", "kimi"))
    else:
        st.markdown('<div class="response-box china-model"><em>Not yet tested</em></div>', unsafe_allow_html=True)
        st.caption("Stats not available")
