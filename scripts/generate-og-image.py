#!/usr/bin/env python3
"""
Generate Open Graph social media preview image for KJV Study.

Creates a 1200x630px image with Tufte-style design matching the site aesthetic.
Output: kjvstudy_org/static/og-image.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

# Image dimensions (standard Open Graph size)
WIDTH = 1200
HEIGHT = 630

# Colors matching Tufte CSS
BG_COLOR = (250, 250, 248)      # Off-white background
TEXT_COLOR = (17, 17, 17)       # Near black for title
ACCENT_COLOR = (102, 102, 102)  # Gray for subtitle

# Text content
TITLE = "KJV Study"
SUBTITLE = "Authorized King James Version Bible"

def generate_og_image():
    """Generate the Open Graph preview image."""

    # Create blank image
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Load fonts (Georgia serif to match site typography)
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 110)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 40)
    except OSError:
        # Fallback to default font if Georgia not available
        print("Warning: Georgia font not found, using default")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Calculate title position (centered)
    title_bbox = draw.textbbox((0, 0), TITLE, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_x = (WIDTH - title_width) // 2
    title_y = (HEIGHT - title_height) // 2 - 60

    # Draw title
    draw.text((title_x, title_y), TITLE, fill=TEXT_COLOR, font=title_font)

    # Calculate subtitle position (centered below title)
    subtitle_bbox = draw.textbbox((0, 0), SUBTITLE, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (WIDTH - subtitle_width) // 2
    subtitle_y = title_y + title_height + 40

    # Draw subtitle
    draw.text((subtitle_x, subtitle_y), SUBTITLE, fill=ACCENT_COLOR, font=subtitle_font)

    # Save to static directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_path = project_root / "kjvstudy_org" / "static" / "og-image.png"

    # Create directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save with optimization
    img.save(output_path, 'PNG', optimize=True)

    print(f"✓ Generated og-image.png")
    print(f"  Location: {output_path}")
    print(f"  Size: {WIDTH}x{HEIGHT}px")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    generate_og_image()
