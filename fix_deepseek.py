"""Fix DeepSeek HTML files that have markdown wrapping"""
import os
import re

APP_DIR = os.path.dirname(os.path.abspath(__file__))

files_to_fix = [
    "flow_deepseek.html",
    "pendulum_deepseek.html",
    "traffic_deepseek.html",
    "animation_deepseek.html"
]

def extract_html(text):
    """Extract HTML from markdown code blocks."""
    # Try to find HTML in code blocks
    match = re.search(r'```html\s*(<!DOCTYPE html>.*?</html>)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    # Try without DOCTYPE
    match = re.search(r'```html\s*(<html.*?</html>)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    # If response starts with <!DOCTYPE or <html, return as-is
    if text.strip().lower().startswith('<!doctype') or text.strip().lower().startswith('<html'):
        return text.strip()
    return text

for filename in files_to_fix:
    filepath = os.path.join(APP_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if it needs fixing
        if not content.strip().lower().startswith('<!doctype') and not content.strip().lower().startswith('<html'):
            print(f"Fixing {filename}...")
            fixed_content = extract_html(content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"  Fixed!")
        else:
            print(f"{filename} is already valid HTML")
    else:
        print(f"{filename} not found")

print("\nDone!")
