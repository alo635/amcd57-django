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
    echo "  sudo npm install -g md-to-pdf"
    echo ""
    exit 1
fi

# Répertoire de sortie
OUTPUT_DIR="docs/pdf"
mkdir -p "$OUTPUT_DIR"

# Fonction pour générer un PDF
generate_pdf() {
    local input_file=$1
    local output_name=$2

    echo "📄 Génération de ${output_name}..."

    # md-to-pdf crée le PDF dans le même répertoire que le fichier source
    # On le génère puis on le déplace
    if md-to-pdf "$input_file" --launch-options '{"args": ["--no-sandbox"]}' 2>/dev/null; then
        # Récupérer le nom du PDF généré (même nom que .md mais avec .pdf)
        local generated_pdf="${input_file%.md}.pdf"

        # Déplacer vers le répertoire de sortie
        if [ -f "$generated_pdf" ]; then
            mv "$generated_pdf" "$OUTPUT_DIR/$output_name"
            echo "✅ $output_name créé"
        else
            echo "❌ Fichier PDF non trouvé: $generated_pdf"
        fi
    else
        echo "❌ Erreur lors de la création de $output_name"
    fi
    echo ""
}

# 1. Générer README.pdf
generate_pdf "readme.md" "README.pdf"

# 2. Générer GUIDE_ADMINISTRATEUR.pdf
generate_pdf "GUIDE_ADMINISTRATEUR.md" "GUIDE_ADMINISTRATEUR.pdf"

# 3. Générer PRODUCTION_CONFIG.pdf
generate_pdf "PRODUCTION_CONFIG.md" "PRODUCTION_CONFIG.pdf"

# 4. Générer DEPLOIEMENT.pdf
generate_pdf "DEPLOIEMENT.md" "DEPLOIEMENT.pdf"

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
