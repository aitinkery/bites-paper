#!/usr/bin/env python3
"""Download fonts for Bites Paper"""
import urllib.request
import os

fonts_dir = "fonts"
os.makedirs(fonts_dir, exist_ok=True)

fonts = {
    "Fraunces-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/fraunces/static/Fraunces_144pt-Regular.ttf",
    "Fraunces-SemiBold.ttf": "https://github.com/google/fonts/raw/main/ofl/fraunces/static/Fraunces_144pt-SemiBold.ttf",
    "Fraunces-Black.ttf": "https://github.com/google/fonts/raw/main/ofl/fraunces/static/Fraunces_144pt-Black.ttf",
    "Inter-Regular.ttf": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.ttf",
    "Inter-Medium.ttf": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Medium.ttf",
    "Inter-Bold.ttf": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.ttf",
}

for filename, url in fonts.items():
    filepath = os.path.join(fonts_dir, filename)
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"  ✓ Saved to {filepath}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

print("\nDone!")
