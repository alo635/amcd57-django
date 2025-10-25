#!/usr/bin/env python3
"""
Script pour générer un favicon à partir du logo AMCD57
"""
from PIL import Image
import os

# Chemins
logo_path = 'static/images/logoamcd.png'
favicon_path = 'static/images/favicon.ico'
favicon_png_path = 'static/images/favicon.png'

print("🎨 Génération du favicon à partir du logo AMCD57...")

# Ouvrir le logo
logo = Image.open(logo_path)
print(f"✅ Logo chargé : {logo.size[0]}x{logo.size[1]} pixels")

# Créer le favicon PNG (32x32)
favicon_png = logo.copy()
favicon_png.thumbnail((32, 32), Image.Resampling.LANCZOS)
favicon_png.save(favicon_png_path, 'PNG')
print(f"✅ Favicon PNG créé : {favicon_png_path}")

# Créer le favicon ICO (16x16 et 32x32)
icon_sizes = [(16, 16), (32, 32)]
favicon_ico = logo.copy()
favicon_ico.save(
    favicon_path,
    format='ICO',
    sizes=icon_sizes
)
print(f"✅ Favicon ICO créé : {favicon_path}")

print("\n🎉 Favicon généré avec succès !")
print(f"   - {favicon_png_path} (PNG 32x32)")
print(f"   - {favicon_path} (ICO 16x16 + 32x32)")
