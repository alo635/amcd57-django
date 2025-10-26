#!/bin/bash
# Script de génération de PDFs depuis les fichiers Markdown
# Nécessite : pandoc et LaTeX (basictex)

echo "🔄 Génération des PDFs depuis les fichiers Markdown..."
echo ""

# Répertoire de sortie
OUTPUT_DIR="docs/pdf"
mkdir -p "$OUTPUT_DIR"

# Configuration Pandoc commune
PANDOC_OPTIONS="--pdf-engine=pdflatex \
  --variable geometry:margin=2cm \
  --variable fontsize=11pt \
  --variable documentclass=article \
  --variable colorlinks=true \
  --variable linkcolor=blue \
  --variable urlcolor=blue \
  --toc \
  --toc-depth=3 \
  --number-sections"

# 1. Générer README.pdf
echo "📄 Génération de README.pdf..."
if pandoc readme.md -o "$OUTPUT_DIR/README.pdf" $PANDOC_OPTIONS \
  --metadata title="AMCD57 - Documentation Projet" \
  --metadata author="AMCD57 - Club d'Aéromodélisme de Delme" \
  --metadata date="$(date +'%d %B %Y')"; then
  echo "✅ README.pdf créé : $OUTPUT_DIR/README.pdf"
else
  echo "❌ Erreur lors de la création de README.pdf"
fi
echo ""

# 2. Générer GUIDE_ADMINISTRATEUR.pdf
echo "📄 Génération de GUIDE_ADMINISTRATEUR.pdf..."
if pandoc GUIDE_ADMINISTRATEUR.md -o "$OUTPUT_DIR/GUIDE_ADMINISTRATEUR.pdf" $PANDOC_OPTIONS \
  --metadata title="Guide Administrateur AMCD57" \
  --metadata author="AMCD57 - Interface d'Administration Django" \
  --metadata date="$(date +'%d %B %Y')"; then
  echo "✅ GUIDE_ADMINISTRATEUR.pdf créé : $OUTPUT_DIR/GUIDE_ADMINISTRATEUR.pdf"
else
  echo "❌ Erreur lors de la création de GUIDE_ADMINISTRATEUR.pdf"
fi
echo ""

# 3. Générer PRODUCTION_CONFIG.pdf (bonus)
echo "📄 Génération de PRODUCTION_CONFIG.pdf..."
if pandoc PRODUCTION_CONFIG.md -o "$OUTPUT_DIR/PRODUCTION_CONFIG.pdf" $PANDOC_OPTIONS \
  --metadata title="Configuration Production AMCD57" \
  --metadata author="AMCD57 - Documentation Technique" \
  --metadata date="$(date +'%d %B %Y')"; then
  echo "✅ PRODUCTION_CONFIG.pdf créé : $OUTPUT_DIR/PRODUCTION_CONFIG.pdf"
else
  echo "❌ Erreur lors de la création de PRODUCTION_CONFIG.pdf"
fi
echo ""

# 4. Générer DEPLOIEMENT.pdf (bonus)
echo "📄 Génération de DEPLOIEMENT.pdf..."
if pandoc DEPLOIEMENT.md -o "$OUTPUT_DIR/DEPLOIEMENT.pdf" $PANDOC_OPTIONS \
  --metadata title="Guide de Déploiement AMCD57" \
  --metadata author="AMCD57 - Guide Technique" \
  --metadata date="$(date +'%d %B %Y')"; then
  echo "✅ DEPLOIEMENT.pdf créé : $OUTPUT_DIR/DEPLOIEMENT.pdf"
else
  echo "❌ Erreur lors de la création de DEPLOIEMENT.pdf"
fi
echo ""

# Résumé
echo "=========================================="
echo "📊 Résumé de la génération"
echo "=========================================="
ls -lh "$OUTPUT_DIR"/*.pdf 2>/dev/null || echo "Aucun PDF généré"
echo ""
echo "📁 PDFs disponibles dans : $OUTPUT_DIR/"
echo ""

# Ouvrir le répertoire (Mac uniquement)
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "📂 Ouverture du dossier de sortie..."
  open "$OUTPUT_DIR"
fi
