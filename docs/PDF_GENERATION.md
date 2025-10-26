# 📄 Génération de PDFs depuis Markdown

Ce guide explique comment générer des versions PDF des fichiers Markdown de documentation.

## 🎯 Fichiers concernés

Les PDFs suivants peuvent être générés :
- **README.pdf** - Documentation complète du projet
- **GUIDE_ADMINISTRATEUR.pdf** - Guide pour les membres du bureau
- **PRODUCTION_CONFIG.pdf** - Configuration de production
- **DEPLOIEMENT.pdf** - Guide de déploiement

## 🔧 Prérequis

### ⭐ Option 1 : md-to-pdf (Recommandé - Supporte les emojis)

**La méthode la plus simple** pour générer des PDFs avec emojis :

```bash
# Installer via npm
sudo npm install -g md-to-pdf

# Utiliser le script simple
./scripts/generate_pdfs_simple.sh
```

**Avantages** :
- ✅ Support natif des emojis
- ✅ Installation simple (juste npm)
- ✅ Pas besoin de LaTeX
- ✅ Style moderne et propre

**Inconvénient** :
- Moins de contrôle sur le style que Pandoc

### Option 2 : Pandoc + LaTeX (Plus de contrôle, pas d'emojis)

**Sur macOS** :
```bash
# Installer Pandoc
brew install pandoc

# Installer BasicTeX (nécessaire pour générer les PDFs)
brew install --cask basictex

# Mettre à jour le PATH
eval "$(/usr/libexec/path_helper)"

# Installer les packages LaTeX requis
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
```

**Sur Linux (Ubuntu/Debian)** :
```bash
# Installer Pandoc et LaTeX
sudo apt update
sudo apt install pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

**Sur Windows** :
```powershell
# Avec Chocolatey
choco install pandoc miktex

# Ou télécharger manuellement :
# - Pandoc : https://pandoc.org/installing.html
# - MiKTeX : https://miktex.org/download
```

## 🚀 Génération avec le script automatique

### Script simple (md-to-pdf - Recommandé)

Le script `scripts/generate_pdfs_simple.sh` génère tous les PDFs **avec support des emojis** :

```bash
./scripts/generate_pdfs_simple.sh
```

### Script Pandoc (sans emojis)

Le script `scripts/generate_pdfs.sh` utilise Pandoc/LaTeX :

```bash
# Exécuter le script
./scripts/generate_pdfs.sh
```

Ce script va :
1. Créer le répertoire `docs/pdf/` s'il n'existe pas
2. Générer les 4 PDFs principaux
3. Ajouter table des matières, numérotation des sections
4. Appliquer un style professionnel
5. Ouvrir automatiquement le dossier de sortie (sur Mac)

**Sortie** :
```
docs/pdf/
├── README.pdf
├── GUIDE_ADMINISTRATEUR.pdf
├── PRODUCTION_CONFIG.pdf
└── DEPLOIEMENT.pdf
```

## 📝 Génération manuelle

Si vous voulez générer un seul fichier ou personnaliser les options :

### Exemple basique

```bash
# Générer un PDF simple
pandoc readme.md -o readme.pdf

# Générer avec options
pandoc GUIDE_ADMINISTRATEUR.md -o GUIDE_ADMINISTRATEUR.pdf \
  --pdf-engine=pdflatex \
  --toc \
  --number-sections \
  --metadata title="Guide Administrateur AMCD57"
```

### Exemple avec toutes les options

```bash
pandoc readme.md -o docs/pdf/README.pdf \
  --pdf-engine=pdflatex \
  --variable geometry:margin=2cm \
  --variable fontsize=11pt \
  --variable documentclass=article \
  --variable colorlinks=true \
  --variable linkcolor=blue \
  --variable urlcolor=blue \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --metadata title="AMCD57 - Documentation Projet" \
  --metadata author="AMCD57 - Club d'Aéromodélisme de Delme" \
  --metadata date="$(date +'%d %B %Y')"
```

### Options Pandoc expliquées

| Option | Description |
|--------|-------------|
| `--pdf-engine=pdflatex` | Moteur de génération PDF |
| `--toc` | Table des matières |
| `--toc-depth=3` | Profondeur de la table des matières |
| `--number-sections` | Numéroter les sections |
| `--variable geometry:margin=2cm` | Marges de la page |
| `--variable fontsize=11pt` | Taille de police |
| `--variable colorlinks=true` | Liens en couleur |
| `--metadata title="Titre"` | Titre du document |

## 🎨 Personnalisation avancée

### Ajouter une page de garde

Créez un fichier `cover.yaml` :

```yaml
---
title: "Guide Administrateur AMCD57"
subtitle: "Interface d'Administration Django"
author: "Club d'Aéromodélisme de Delme"
date: "Octobre 2025"
abstract: |
  Ce guide complet explique comment utiliser l'interface
  d'administration Django pour gérer le contenu du site AMCD57.
---
```

Puis générez avec :

```bash
pandoc cover.yaml GUIDE_ADMINISTRATEUR.md -o GUIDE_ADMINISTRATEUR.pdf \
  --pdf-engine=pdflatex \
  --toc \
  --number-sections
```

### Utiliser un template LaTeX personnalisé

```bash
pandoc readme.md -o readme.pdf \
  --template=custom-template.latex \
  --pdf-engine=pdflatex
```

## 🐛 Dépannage

### Erreur : "pdflatex not found"

**Cause** : LaTeX n'est pas installé.

**Solution** :
- macOS : `brew install --cask basictex`
- Linux : `sudo apt install texlive-latex-base`
- Windows : Installer MiKTeX

### Erreur : "! LaTeX Error: File `...sty' not found"

**Cause** : Package LaTeX manquant.

**Solution** :
```bash
# macOS/Linux
sudo tlmgr install <nom-du-package>

# Ou installer la collection complète
sudo tlmgr install collection-fontsrecommended
```

### PDF généré mais emojis manquants

**Cause** : LaTeX ne gère pas nativement les emojis.

**Solution** : Utiliser `md-to-pdf` (Node.js) à la place :
```bash
npm install -g md-to-pdf
md-to-pdf readme.md
```

### Erreur de mémoire lors de la génération

**Cause** : Document trop volumineux.

**Solution** : Augmenter la mémoire LaTeX ou diviser le document.

## 📚 Ressources

- [Documentation Pandoc](https://pandoc.org/MANUAL.html)
- [Pandoc PDF options](https://pandoc.org/MANUAL.html#creating-a-pdf)
- [md-to-pdf (alternative Node.js)](https://www.npmjs.com/package/md-to-pdf)
- [LaTeX Project](https://www.latex-project.org/)

## ✅ Checklist

Avant de distribuer les PDFs :

- [ ] Vérifier que tous les liens fonctionnent
- [ ] Vérifier la table des matières
- [ ] Vérifier que les images s'affichent correctement
- [ ] Vérifier la numérotation des sections
- [ ] Vérifier les métadonnées (titre, auteur, date)
- [ ] Tester l'ouverture sur différents lecteurs PDF
- [ ] Vérifier la taille du fichier (compression si > 10 MB)

---

**Note** : Les PDFs générés ne sont pas versionnés dans Git (ajoutés au `.gitignore`). Ils doivent être générés à la demande quand la documentation est mise à jour.
