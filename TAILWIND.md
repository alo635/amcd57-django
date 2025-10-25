# Tailwind CSS - Guide d'utilisation

## 📦 Installation effectuée

Tailwind CSS v3 est configuré et optimisé pour le projet AMCD57.

## 🚀 Utilisation en développement

### Option 1 : Build manuel (après modifications)
```bash
npm run build
```

### Option 2 : Watch mode (recommandé - recompile automatiquement)
```bash
npm run watch
```

Puis dans un autre terminal :
```bash
source venv/bin/activate
python manage.py runserver
```

## 📊 Optimisation obtenue

- **Avant** : CDN Tailwind = ~3.5 MB
- **Après** : CSS optimisé = ~43 KB
- **Gain** : 98.8% de réduction !

## 📁 Structure des fichiers

```
static/
├── css/
│   ├── src/
│   │   └── input.css          # Fichier source avec @tailwind directives
│   └── output.css             # Fichier CSS compilé (utilisé par Django)
```

## ⚙️ Configuration

### tailwind.config.js
Configure les chemins des templates à scanner pour détecter les classes utilisées :
```javascript
content: [
  './templates/**/*.html',
  './*/templates/**/*.html',
  './**/templates/**/*.html',
]
```

### Couleur personnalisée
La couleur `amcd-blue` est définie dans `tailwind.config.js` :
```javascript
colors: {
  'amcd-blue': '#1e40af',
}
```

## 🔧 Ajouter des styles personnalisés

### Dans les templates (recommandé)
Utilisez directement les classes Tailwind :
```html
<div class="bg-blue-500 text-white p-4 rounded-lg">
  Mon contenu
</div>
```

### CSS personnalisé (optionnel)
Ajoutez vos styles dans `static/css/src/input.css` :
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Vos styles personnalisés */
.ma-classe-custom {
  @apply bg-blue-500 text-white p-4;
}
```

## 📝 Workflow de développement

1. **Modifier les templates** avec les classes Tailwind
2. **Watch mode** détecte automatiquement les changements
3. **Rechargez la page** pour voir les modifications

## 🐛 En cas de problème

### Les classes ne sont pas appliquées
```bash
# Reconstruisez le CSS
npm run build
```

### Le fichier CSS n'est pas chargé
Vérifiez que Django collecte les static files :
```bash
python manage.py collectstatic
```

En développement avec `DEBUG=True`, c'est automatique.

## 🚀 Production

Avant le déploiement :
```bash
# Build final minifié
npm run build

# Collecte des fichiers statiques
python manage.py collectstatic --noinput
```

## 📚 Ressources

- [Documentation Tailwind CSS](https://tailwindcss.com/docs)
- [Tailwind Play (testeur en ligne)](https://play.tailwindcss.com/)
- [Tailwind Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)

---

**💡 Astuce** : Utilisez `npm run watch` en parallèle de `python manage.py runserver` pour un développement fluide !
