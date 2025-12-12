"""Dynamic OG image generator for social sharing."""

import hashlib
import os
import textwrap
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Image dimensions (standard OG image size)
WIDTH = 1200
HEIGHT = 630

# Colors matching the site design
BG_COLOR = (255, 255, 248)  # #fffff8 - cream/off-white
TITLE_COLOR = (34, 34, 34)  # #222 - dark gray/black
SUBTITLE_COLOR = (102, 102, 102)  # #666 - medium gray
VERSE_COLOR = (68, 68, 68)  # #444 - slightly lighter for verse text
ACCENT_COLOR = (74, 124, 89)  # #4a7c59 - green accent

# Cache directory
CACHE_DIR = Path(__file__).parent / "static" / "og-cache"


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Get a font, falling back to default if custom font not available."""
    # Try to use system fonts that look like et-book/Georgia
    font_paths = [
        "/System/Library/Fonts/Supplemental/Georgia.ttf",  # macOS
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",  # macOS bold
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",  # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",  # Linux bold
        "C:\\Windows\\Fonts\\georgia.ttf",  # Windows
        "C:\\Windows\\Fonts\\georgiab.ttf",  # Windows bold
    ]

    # Filter for bold/regular
    if bold:
        font_paths = [p for p in font_paths if "Bold" in p or "bold" in p or "georgiab" in p]
    else:
        font_paths = [p for p in font_paths if "Bold" not in p and "bold" not in p and "georgiab" not in p]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    # Fallback to default
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = font.getbbox(test_line)
        if bbox[2] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return lines


def generate_og_image(
    title: str,
    subtitle: str | None = None,
    verse_text: str | None = None,
    page_type: str = "default"
) -> bytes:
    """
    Generate an OG image with the given content.

    Args:
        title: Main title text (e.g., "Genesis 1:1", "Faith", "The Creation")
        subtitle: Optional subtitle (e.g., "Authorized King James Version")
        verse_text: Optional verse text to display
        page_type: Type of page for styling variations

    Returns:
        PNG image as bytes
    """
    # Create image
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Load fonts
    title_font = get_font(72, bold=True)
    subtitle_font = get_font(36)
    verse_font = get_font(32)
    brand_font = get_font(28)

    # Calculate vertical positioning
    y_cursor = HEIGHT // 2 - 100  # Start above center

    # Draw title
    title_lines = wrap_text(title, title_font, WIDTH - 160)
    for line in title_lines[:2]:  # Max 2 lines for title
        bbox = title_font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, y_cursor), line, font=title_font, fill=TITLE_COLOR)
        y_cursor += bbox[3] - bbox[1] + 10

    y_cursor += 20  # Space after title

    # Draw subtitle if provided
    if subtitle:
        bbox = subtitle_font.getbbox(subtitle)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, y_cursor), subtitle, font=subtitle_font, fill=SUBTITLE_COLOR)
        y_cursor += bbox[3] - bbox[1] + 30

    # Draw verse text if provided (truncated with ellipsis)
    if verse_text:
        # Truncate verse text if too long
        if len(verse_text) > 200:
            verse_text = verse_text[:197] + "..."

        verse_lines = wrap_text(f'"{verse_text}"', verse_font, WIDTH - 200)
        for line in verse_lines[:3]:  # Max 3 lines
            bbox = verse_font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            x = (WIDTH - text_width) // 2
            draw.text((x, y_cursor), line, font=verse_font, fill=VERSE_COLOR)
            y_cursor += bbox[3] - bbox[1] + 8

    # Draw brand at bottom
    brand_text = "kjvstudy.org"
    bbox = brand_font.getbbox(brand_text)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, HEIGHT - 60), brand_text, font=brand_font, fill=ACCENT_COLOR)

    # Add subtle accent line
    line_width = 100
    line_y = HEIGHT - 90
    draw.line(
        [(WIDTH // 2 - line_width // 2, line_y), (WIDTH // 2 + line_width // 2, line_y)],
        fill=ACCENT_COLOR,
        width=2
    )

    # Convert to bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def get_cache_path(cache_key: str) -> Path:
    """Get the cache file path for a given key."""
    # Create cache directory if it doesn't exist
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Hash the key for a safe filename
    key_hash = hashlib.md5(cache_key.encode()).hexdigest()
    return CACHE_DIR / f"{key_hash}.png"


def get_cached_or_generate(
    cache_key: str,
    title: str,
    subtitle: str | None = None,
    verse_text: str | None = None,
    page_type: str = "default"
) -> bytes:
    """
    Get a cached OG image or generate a new one.

    Args:
        cache_key: Unique key for caching (e.g., "verse:Genesis:1:1")
        title: Main title text
        subtitle: Optional subtitle
        verse_text: Optional verse text
        page_type: Type of page

    Returns:
        PNG image as bytes
    """
    cache_path = get_cache_path(cache_key)

    # Check cache
    if cache_path.exists():
        return cache_path.read_bytes()

    # Generate new image
    image_bytes = generate_og_image(title, subtitle, verse_text, page_type)

    # Cache it
    try:
        cache_path.write_bytes(image_bytes)
    except Exception:
        # Don't fail if caching fails (e.g., read-only filesystem)
        pass

    return image_bytes
