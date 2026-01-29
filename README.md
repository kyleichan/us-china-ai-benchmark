# US-China AI Scorecard

A Streamlit dashboard comparing the capabilities of leading US and Chinese AI models across various benchmarks.

## Models Compared

**US Models:**
- GPT-5.2 (OpenAI)
- Gemini 3 Pro (Google)

**Chinese Models:**
- DeepSeek V3.2
- Qwen3-Max (Alibaba)
- Kimi K2.5 (Moonshot AI)

## Benchmarks

The scorecard evaluates models on:

1. **Basic reasoning** - Simple letter counting tasks
2. **Knowledge & censorship** - Questions about political leaders (reveals content filtering differences)
3. **Coding challenges** - Complex single-prompt coding tasks:
   - Nested spinning hexagons with bouncing balls (physics simulation)
   - Flow-field particle visualization (curl noise, 2000 particles)
   - Double pendulum simulation (custom physics, velocity-colored trails)
   - Urban traffic simulation (10x10 grid, autonomous agents, emergent congestion)

## Metrics Tracked

- Token usage (input/output)
- Response time
- Cost per query
- Content filtering/censorship

## Setup

1. Install dependencies:
   ```bash
   pip install streamlit
   ```

2. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   DEEPSEEK_API_KEY=your_key
   KIMI_API_KEY=your_key
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
├── app.py                 # Main Streamlit dashboard
├── run_coding_prompts.py  # Script to generate coding benchmark outputs
├── benchmark.py           # Benchmark runner utilities
├── stats.json             # Token usage and timing data
├── *_gpt.html            # GPT-5.2 coding outputs
├── *_gemini.html         # Gemini 3 Pro coding outputs
├── *_deepseek.html       # DeepSeek V3.2 coding outputs
├── *_kimi.html           # Kimi K2.5 coding outputs
└── .env                   # API keys (not tracked)
```

## Author

Created by Kyle Chan
