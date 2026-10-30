"""
Generate branding logo.png for AI Resume Analyzer
"""
from PIL import Image, ImageDraw, ImageFont
import os

assets_dir = os.path.dirname(__file__)
logo_path = os.path.join(assets_dir, "logo.png")

img = Image.new('RGBA', (300, 300), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Outer circle accent
draw.ellipse((20, 20, 280, 280), fill=(108, 92, 231, 255), outline=(162, 155, 254, 255), width=6)

# Inner document / AI icon shape
draw.rectangle((90, 80, 210, 220), fill=(255, 255, 255, 255))
draw.line((110, 110, 190, 110), fill=(108, 92, 231, 255), width=6)
draw.line((110, 140, 190, 140), fill=(108, 92, 231, 255), width=6)
draw.line((110, 170, 170, 170), fill=(108, 92, 231, 255), width=6)

# Star / AI Sparkle accent
draw.polygon([(210, 60), (220, 80), (240, 90), (220, 100), (210, 120), (200, 100), (180, 90), (200, 80)], fill=(255, 234, 167, 255))

img.save(logo_path)
print("Logo generated at logo.png")
