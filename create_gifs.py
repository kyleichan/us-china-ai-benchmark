"""
Create looping GIFs from HTML canvas animations using Playwright
"""
import os
import asyncio
import argparse
from pathlib import Path
from playwright.async_api import async_playwright
import imageio

# Configuration
DEFAULT_DURATION = 5  # seconds
DEFAULT_FPS = 15
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 670

async def capture_frames(html_path: str, duration: float, fps: int) -> list:
    """Capture frames from an HTML animation."""
    frames = []
    frame_count = int(duration * fps)
    frame_interval = 1000 / fps  # milliseconds between frames

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": CANVAS_WIDTH + 50, "height": CANVAS_HEIGHT + 50})

        # Load the HTML file
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        await page.goto(file_url)

        # Wait for animation to start
        await page.wait_for_timeout(500)

        print(f"  Capturing {frame_count} frames at {fps}fps...")

        for i in range(frame_count):
            # Take screenshot
            screenshot = await page.screenshot(type="png")
            frames.append(screenshot)

            # Wait for next frame
            await page.wait_for_timeout(frame_interval)

            # Progress indicator
            if (i + 1) % 15 == 0:
                print(f"    {i + 1}/{frame_count} frames captured")

        await browser.close()

    return frames

def create_gif(frames: list, output_path: str, fps: int):
    """Create a looping GIF from frames."""
    from PIL import Image
    import io

    # Convert PNG bytes to PIL Images
    images = []
    for frame_bytes in frames:
        img = Image.open(io.BytesIO(frame_bytes))
        # Convert to RGB if necessary (GIF doesn't support RGBA well)
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (0, 0, 0))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)

    # Save as GIF
    duration = 1000 / fps  # milliseconds per frame
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0  # 0 = infinite loop
    )

    # Get file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Saved: {output_path} ({size_mb:.2f} MB)")

async def process_html(html_path: str, output_dir: str, duration: float, fps: int):
    """Process a single HTML file into a GIF."""
    html_name = Path(html_path).stem
    output_path = os.path.join(output_dir, f"{html_name}.gif")

    print(f"\nProcessing: {html_name}")

    # Capture frames
    frames = await capture_frames(html_path, duration, fps)

    # Create GIF
    create_gif(frames, output_path, fps)

async def main():
    parser = argparse.ArgumentParser(
        description="Create looping GIFs from HTML animations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_gifs.py                              # All animations, 5s duration
  python create_gifs.py -p animation                 # Only animation prompt
  python create_gifs.py -m gpt                       # Only GPT outputs
  python create_gifs.py -p pendulum -m gemini        # Specific prompt and model
  python create_gifs.py -d 3 -f 10                   # 3 seconds at 10fps
        """
    )
    parser.add_argument("-p", "--prompts", nargs="+",
                        choices=["animation", "flow", "pendulum", "traffic"],
                        help="Prompts to process (default: all)")
    parser.add_argument("-m", "--models", nargs="+",
                        choices=["gpt", "gemini", "deepseek"],
                        help="Models to process (default: all)")
    parser.add_argument("-d", "--duration", type=float, default=DEFAULT_DURATION,
                        help=f"Duration in seconds (default: {DEFAULT_DURATION})")
    parser.add_argument("-f", "--fps", type=int, default=DEFAULT_FPS,
                        help=f"Frames per second (default: {DEFAULT_FPS})")
    parser.add_argument("-o", "--output", default=None,
                        help="Output directory (default: same as HTML files)")
    args = parser.parse_args()

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = args.output or script_dir

    # Default to all prompts and models
    prompts = args.prompts or ["animation", "flow", "pendulum", "traffic"]
    models = args.models or ["gpt", "gemini", "deepseek"]

    print(f"Creating GIFs: {args.duration}s duration, {args.fps}fps")
    print(f"Prompts: {', '.join(prompts)}")
    print(f"Models: {', '.join(models)}")

    # Process each combination
    for prompt in prompts:
        for model in models:
            html_file = os.path.join(script_dir, f"{prompt}_{model}.html")
            if os.path.exists(html_file):
                await process_html(html_file, output_dir, args.duration, args.fps)
            else:
                print(f"\nSkipping: {prompt}_{model}.html (not found)")

    print("\nDone!")

if __name__ == "__main__":
    asyncio.run(main())
