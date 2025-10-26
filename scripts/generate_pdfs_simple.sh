#!/bin/bash
# Script de génération de PDFs depuis les fichiers Markdown
# Utilise md-to-pdf (npm) - Support complet des emojis ✅

echo "🔄 Génération des PDFs avec md-to-pdf..."
echo ""

# Vérifier que md-to-pdf est installé
if ! command -v md-to-pdf &> /dev/null; then
    echo "❌ md-to-pdf n'est pas installé."
    echo ""
    echo "Pour l'installer :"
    echo "  npm install -g md-to-pdf"
    echo ""
    exit 1
fi

# Répertoire de sortie
OUTPUT_DIR="docs/pdf"
mkdir -p "$OUTPUT_DIR"

# 1. Générer README.pdf
echo "📄 Génération de README.pdf..."
if md-to-pdf readme.md --dest "$OUTPUT_DIR/README.pdf" --launch-options '{"args": ["--no-sandbox"]}'; then
  echo "✅ README.pdf créé"
else
  echo "❌ Erreur lors de la création de README.pdf"
fi
echo ""

# 2. Générer GUIDE_ADMINISTRATEUR.pdf
echo "📄 Génération de GUIDE_ADMINISTRATEUR.pdf..."
if md-to-pdf GUIDE_ADMINISTRATEUR.md --dest "$OUTPUT_DIR/GUIDE_ADMINISTRATEUR.pdf" --launch-options '{"args": ["--no-sandbox"]}'; then
  echo "✅ GUIDE_ADMINISTRATEUR.pdf créé"
else
  echo "❌ Erreur lors de la création de GUIDE_ADMINISTRATEUR.pdf"
fi
echo ""

# 3. Générer PRODUCTION_CONFIG.pdf
echo "📄 Génération de PRODUCTION_CONFIG.pdf..."
if md-to-pdf PRODUCTION_CONFIG.md --dest "$OUTPUT_DIR/PRODUCTION_CONFIG.pdf" --launch-options '{"args": ["--no-sandbox"]}'; then
  echo "✅ PRODUCTION_CONFIG.pdf créé"
else
  echo "❌ Erreur lors de la création de PRODUCTION_CONFIG.pdf"
fi
echo ""

# 4. Générer DEPLOIEMENT.pdf
echo "📄 Génération de DEPLOIEMENT.pdf..."
if md-to-pdf DEPLOIEMENT.md --dest "$OUTPUT_DIR/DEPLOIEMENT.pdf" --launch-options '{"args": ["--no-sandbox"]}'; then
  echo "✅ DEPLOIEMENT.pdf créé"
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
