# 📘 Guide Administrateur AMCD57

Guide complet pour les membres du bureau qui administrent le site web du club AMCD57.

---

## 📋 Table des matières

1. [Accès à l'administration](#accès-à-ladministration)
2. [Gestion des articles de blog](#gestion-des-articles-de-blog)
3. [Gestion des événements](#gestion-des-événements)
4. [Gestion des membres](#gestion-des-membres)
5. [Gestion des liens utiles](#gestion-des-liens-utiles)
6. [Messages de contact](#messages-de-contact)
7. [Bonnes pratiques](#bonnes-pratiques)
8. [Résolution de problèmes](#résolution-de-problèmes)

---

## 🔐 Accès à l'administration

### Se connecter

1. Ouvrez votre navigateur et allez sur : **https://amcd.alodev.ovh/admin/**
2. Entrez votre **email** et votre **mot de passe**
3. Cliquez sur "Se connecter"

**Note** : Seuls les membres du bureau ont accès à l'interface d'administration.

### Première connexion

Si c'est votre première connexion, votre mot de passe vous a été communiqué par le responsable technique. Il est recommandé de le changer :

1. Cliquez sur votre nom (en haut à droite)
2. Cliquez sur "Modifier le mot de passe"
3. Entrez l'ancien mot de passe, puis le nouveau (2 fois)
4. Cliquez sur "Modifier mon mot de passe"

---

## 📝 Gestion des articles de blog

### Créer un nouvel article

1. Dans le menu de gauche, cliquez sur **"Blog" → "Articles"**
2. Cliquez sur **"AJOUTER ARTICLE"** (en haut à droite)
3. Remplissez les champs :

   **Champs obligatoires** :
   - **Titre** : Le titre de votre article (ex: "Sortie vol du 15 octobre")
   - **Contenu** : Le texte de l'article (éditeur riche avec formatage)
   - **Auteur** : Sélectionnez votre nom dans la liste
   - **Catégorie** : Choisissez la catégorie appropriée
     - **Club** : Vie du club, assemblées générales, actualités
     - **Technique** : Conseils techniques, tutoriels
     - **Convention** : Comptes-rendus de conventions, salons
     - **Divers** : Autres sujets

   **Champs optionnels** :
   - **Slug** : URL de l'article (se génère automatiquement depuis le titre)
   - **Extrait** : Résumé court (se génère automatiquement si vide)
   - **Image** : Photo à la une (formats acceptés : JPG, PNG, max 5 Mo)
   - **Tags** : Mots-clés pour faciliter la recherche (sélection multiple)
   - **Meta description** : Description pour Google (recommandé, 150-160 caractères)

4. **Statut** : Choisissez entre :
   - **Brouillon** : L'article n'est pas visible sur le site (vous pouvez continuer à travailler dessus)
   - **Publié** : L'article est visible par tous les visiteurs

5. Cliquez sur **"ENREGISTRER"** (en bas)

### Modifier un article existant

1. **"Blog" → "Articles"**
2. Trouvez l'article dans la liste
3. Cliquez sur le titre de l'article
4. Modifiez les champs souhaités
5. Cliquez sur **"ENREGISTRER"**

**Astuce** : Utilisez la recherche (en haut) pour trouver rapidement un article par son titre.

### Publier un brouillon

1. Ouvrez l'article en mode édition
2. Changez le **Statut** de "Brouillon" à "Publié"
3. Cliquez sur **"ENREGISTRER"**

L'article apparaît immédiatement sur le site dans la section Blog.

### Supprimer un article

1. **"Blog" → "Articles"**
2. Cochez la case à gauche de l'article à supprimer
3. Dans le menu déroulant "Action", sélectionnez **"Supprimer les articles sélectionnés"**
4. Cliquez sur **"Exécuter"**
5. Confirmez la suppression

**⚠️ Attention** : La suppression est définitive et supprime également tous les commentaires associés.

### Gérer les commentaires

1. **"Blog" → "Commentaires"**
2. Vous voyez la liste de tous les commentaires (approuvés et en attente)

**Approuver un commentaire** :
- Cochez le(s) commentaire(s) à approuver
- Action : "Approuver les commentaires sélectionnés"
- Cliquez sur "Exécuter"

**Supprimer un commentaire** :
- Cochez le(s) commentaire(s) à supprimer
- Action : "Supprimer les commentaires sélectionnés"
- Cliquez sur "Exécuter"

**Répondre à un commentaire** :
- Cliquez sur le commentaire
- Vous pouvez créer un nouveau commentaire en réponse
- N'oubliez pas de l'approuver

### Gérer les catégories

1. **"Blog" → "Catégories"**
2. **Ajouter** : Cliquez sur "AJOUTER CATÉGORIE"
3. **Modifier** : Cliquez sur une catégorie existante

**Champs** :
- **Nom** : Nom de la catégorie
- **Slug** : URL (auto-généré)
- **Description** : Courte description (optionnel)
- **Image** : Image représentative (optionnel)

### Gérer les tags

1. **"Blog" → "Tags"**
2. **Ajouter** : Cliquez sur "AJOUTER TAG"

**Champs** :
- **Nom** : Nom du tag (ex: "planeur", "débutant")
- **Slug** : URL (auto-généré)

---

## 📅 Gestion des événements

### Créer un nouvel événement

1. **"Events" → "Événements"**
2. Cliquez sur **"AJOUTER ÉVÉNEMENT"**

**Informations générales** :
- **Titre** : Nom de l'événement (ex: "Sortie vol mensuelle")
- **Description** : Détails de l'événement (contenu riche)
- **Type d'événement** : Réunion, Sortie terrain, Vol libre, Convention
- **Organisateur** : Votre nom

**Dates et horaires** :
- **Date de début** : Date et heure de début (cliquez sur le calendrier)
- **Date de fin** : Date et heure de fin
- **Toute la journée** : Cochez si l'événement dure toute la journée

**Lieu** :
- **Lieu** : Sélectionnez un lieu existant ou créez-en un nouveau
  - Pour créer un lieu : Cliquez sur le **+** vert à droite
  - Remplissez : Nom, Adresse, Ville, Code postal, Latitude, Longitude
  - Cliquez sur "ENREGISTRER"

**Inscriptions** :
- **Inscription requise** : Cochez si les membres doivent s'inscrire
- **Places limitées** : Cochez s'il y a un nombre maximum de participants
- **Nombre de places** : Si places limitées (ex: 20)
- **Date limite d'inscription** : Date avant laquelle s'inscrire

**Statut** :
- **Planifié** : Événement prévu mais pas confirmé
- **Confirmé** : Événement confirmé, visible sur le site
- **Annulé** : Événement annulé (reste visible mais marqué comme annulé)
- **Terminé** : Événement passé

3. Cliquez sur **"ENREGISTRER"**

### Gérer les inscriptions

1. **"Events" → "Inscriptions"**
2. Vous voyez toutes les inscriptions aux événements

**Colonnes importantes** :
- **Événement** : À quel événement
- **Participant** : Qui s'est inscrit
- **Statut** : En attente / Confirmé / Annulé
- **Accompagnants** : Nombre de personnes supplémentaires

**Confirmer une inscription** :
- Cliquez sur l'inscription
- Changez **Statut** de "En attente" à "Confirmé"
- Cliquez sur "ENREGISTRER"

**Marquer la présence** (après l'événement) :
- Cliquez sur l'inscription
- Cochez **"Présent"**
- Cliquez sur "ENREGISTRER"

**Voir les participants d'un événement** :
- Utilisez le filtre **"Événement"** en haut à droite
- Sélectionnez l'événement souhaité

### Gérer les types d'événements

1. **"Events" → "Types d'événements"**
2. **Modifier** : Cliquez sur un type existant

**Champs** :
- **Nom** : Nom du type (Réunion, Sortie, etc.)
- **Description** : Courte description
- **Couleur** : Code couleur hexadécimal (ex: #3B82F6 pour bleu)
- **Icône** : Emoji représentatif (ex: 🛩️, 📅, 🎪)

**⚠️ Attention** : Ne supprimez pas un type d'événement si des événements l'utilisent.

### Gérer les lieux

1. **"Events" → "Lieux"**
2. **Ajouter un nouveau lieu** :
   - Nom : Nom du lieu (ex: "Terrain AMCD Jarny")
   - Adresse, ville, code postal
   - Coordonnées GPS (latitude, longitude)
   - Capacité : Nombre maximum de personnes (optionnel)

**Astuce** : Pour trouver les coordonnées GPS :
1. Allez sur Google Maps
2. Faites un clic droit sur le lieu
3. Cliquez sur les coordonnées qui apparaissent en haut
4. Copiez-collez dans les champs Latitude et Longitude

---

## 👥 Gestion des membres

### Voir les membres

1. **"Members" → "Profils membres"**
2. Liste de tous les membres du club

**Colonnes** :
- **Nom complet** : Nom et prénom
- **Email** : Adresse email
- **Type de membre** : Bureau, Actif, Sympathisant
- **Adhésion valide** : Cotisation à jour ou non

### Créer un nouveau membre

**⚠️ Processus en 2 étapes** :

**Étape 1 : Créer l'utilisateur**
1. **"Authentification et autorisations" → "Utilisateurs"**
2. Cliquez sur **"AJOUTER UTILISATEUR"**
3. Remplissez :
   - **Email** : Adresse email du membre
   - **Mot de passe** : Mot de passe temporaire (à communiquer au membre)
4. Cliquez sur **"ENREGISTRER"**

**Étape 2 : Créer le profil membre**
1. **"Members" → "Profils membres"**
2. Cliquez sur **"AJOUTER PROFIL MEMBRE"**
3. Remplissez :
   - **Utilisateur** : Sélectionnez l'email créé à l'étape 1
   - **Nom** : Nom de famille
   - **Prénom** : Prénom
   - **Date de naissance** : JJ/MM/AAAA
   - **Téléphone** : Format 06XXXXXXXX ou 03XXXXXXXX
   - **Adresse, ville, code postal**
   - **Type de membre** : Bureau, Actif, ou Sympathisant
   - **Date d'adhésion** : Date d'inscription au club
   - **Cotisation valide jusqu'au** : Date de fin de cotisation (ex: 31/12/2025)
4. Cliquez sur **"ENREGISTRER"**

### Modifier un membre

1. **"Members" → "Profils membres"**
2. Cliquez sur le membre à modifier
3. Modifiez les informations
4. Cliquez sur **"ENREGISTRER"**

### Renouveler une cotisation

1. **"Members" → "Profils membres"**
2. Cliquez sur le membre
3. Modifiez **"Cotisation valide jusqu'au"** avec la nouvelle date de fin
4. Cliquez sur **"ENREGISTRER"**

Le champ **"Adhésion valide"** se met à jour automatiquement.

### Gérer les types de membres

1. **"Members" → "Types de membres"**

**Types existants** :
- **Bureau** : Membres du bureau (accès admin)
  - Peut voter ✓
  - Accès terrain ✓
  - Accès espace membre ✓

- **Actif** : Membres actifs cotisants
  - Peut voter ✓
  - Accès terrain ✓
  - Accès espace membre ✓

- **Sympathisant** : Non-cotisants
  - Peut voter ✗
  - Accès terrain ✗
  - Accès espace membre ✗

**⚠️ Attention** : Ne modifiez pas ces types sans consulter le bureau.

### Gérer les fonctions du bureau

1. **"Members" → "Fonctions bureau"**
2. Liste des postes au bureau

**Fonctions** :
- Président
- Vice-Président
- Trésorier
- Secrétaire

**Champs** :
- **Membre** : Qui occupe ce poste
- **Fonction** : Type de fonction
- **Date de début** : Début du mandat
- **Date de fin** : Fin du mandat (optionnel)
- **Fonction active** : Cochez si la personne occupe actuellement ce poste

---

## 🔗 Gestion des liens utiles

### Créer un lien

1. **"Weblinks" → "Liens"**
2. Cliquez sur **"AJOUTER LIEN"**

**Champs** :
- **Titre** : Nom du site (ex: "Fédération Française d'Aéromodélisme")
- **URL** : Adresse complète (ex: https://www.ffam.asso.fr)
- **Description** : Brève description du site
- **Catégorie** : Officiels, Clubs amis, Techniques, Boutiques
- **Tags** : Mots-clés (optionnel)
- **Logo** : Image du logo du site (optionnel)
- **Featured** : Cochez pour mettre en avant ce lien
- **Actif** : Cochez pour rendre le lien visible

3. Cliquez sur **"ENREGISTRER"**

### Gérer les catégories de liens

1. **"Weblinks" → "Catégories de liens"**
2. **Ajouter** : Cliquez sur "AJOUTER CATÉGORIE DE LIEN"

**Catégories recommandées** :
- **Officiels** : Fédérations, DGAC, etc.
- **Clubs amis** : Autres clubs de la région
- **Techniques** : Sites de conseils, tutoriels
- **Boutiques** : Magasins de modélisme

---

## 📧 Messages de contact

### Voir les messages

1. **"Core" → "Messages de contact"**
2. Liste de tous les messages reçus via le formulaire de contact

**Colonnes** :
- **Nom complet** : Qui a envoyé le message
- **Email** : Pour répondre
- **Sujet** : Type de demande
- **Statut** : Nouveau, En cours, Traité, Archivé
- **Lu** : Message lu ou non

### Traiter un message

1. Cliquez sur le message pour l'ouvrir
2. Lisez le **message** et les **informations de contact**
3. **Répondez par email** si nécessaire (utilisez l'email affiché)
4. Mettez à jour le **Statut** :
   - **Nouveau** → **En cours** : Quand vous commencez à traiter
   - **En cours** → **Traité** : Quand c'est terminé
   - **Traité** → **Archivé** : Pour ranger les anciens messages
5. Cochez **"Répondu"** si vous avez envoyé une réponse
6. Ajoutez des **Notes internes** si besoin (visibles seulement par les admins)
7. Cliquez sur **"ENREGISTRER"**

### Filtrer les messages

Utilisez les filtres à droite :
- **Par statut** : Voir uniquement les nouveaux, en cours, etc.
- **Par sujet** : Informations, Adhésion, Événement, etc.
- **Par lu/non lu**

### Supprimer des messages

1. Cochez les messages à supprimer
2. Action : "Supprimer les messages de contact sélectionnés"
3. Cliquez sur "Exécuter"

**💡 Conseil** : Archivez plutôt que de supprimer pour garder un historique.

---

## ✅ Bonnes pratiques

### Rédaction d'articles

**Titre** :
- Clair et descriptif
- 50-70 caractères idéal
- Exemple : "Sortie vol du 15 octobre à Commercy"

**Contenu** :
- Structurez avec des titres (Titre 2, Titre 3)
- Paragraphes courts et aérés
- Ajoutez des images (1-3 par article)
- Relisez avant de publier

**Images** :
- Taille recommandée : 1200x800 pixels
- Format : JPG (photos), PNG (logos/graphiques)
- Poids : < 500 Ko (compressez si nécessaire)
- Nommez vos fichiers clairement : `sortie-jarny-octobre-2025.jpg`

**SEO (référencement)** :
- Remplissez la "Meta description" (150-160 caractères)
- Utilisez des tags pertinents
- Choisissez la bonne catégorie

### Gestion des événements

**Anticipation** :
- Créez les événements **au moins 2 semaines à l'avance**
- Ouvrez les inscriptions suffisamment tôt
- Confirmez le statut rapidement

**Communication** :
- Statut "Confirmé" = l'événement aura bien lieu
- Statut "Annulé" = visible mais marqué comme annulé (avec raison dans la description)
- Passez en "Terminé" après l'événement

**Inscriptions** :
- Confirmez rapidement les inscriptions (notification par email)
- Surveillez le nombre de places restantes
- Marquez les présences après l'événement (statistiques)

### Gestion des membres

**Données personnelles** :
- Ne partagez jamais les informations personnelles
- Respectez le RGPD
- Seuls les membres du bureau ont accès

**Cotisations** :
- Vérifiez régulièrement les dates d'expiration
- Relancez les membres dont la cotisation expire bientôt
- Mettez à jour rapidement après paiement

**Sécurité** :
- Créez des mots de passe forts pour les nouveaux membres
- Demandez-leur de changer le mot de passe à la première connexion

---

## 🔧 Résolution de problèmes

### Je ne peux pas me connecter

**Vérifiez** :
1. Vous utilisez bien votre **email** (pas un nom d'utilisateur)
2. Le mot de passe est correct (majuscules/minuscules)
3. Vous êtes bien sur https://amcd.alodev.ovh/admin/

**Solution** :
- Utilisez "Mot de passe oublié ?" sur la page de connexion
- Ou contactez le responsable technique

### Je ne vois pas certaines sections

**Cause** : Vous n'avez pas les permissions nécessaires.

**Solution** : Contactez le responsable technique pour vérifier vos permissions.

### Une image ne s'upload pas

**Causes possibles** :
- Fichier trop lourd (> 5 Mo)
- Format non supporté (utiliser JPG ou PNG)
- Nom de fichier avec caractères spéciaux

**Solutions** :
1. Compressez l'image (avec TinyPNG, Compressor.io, etc.)
2. Convertissez au format JPG ou PNG
3. Renommez sans accents ni espaces (utiliser des tirets)

### Un article/événement n'apparaît pas sur le site

**Vérifiez** :
1. **Statut** : Doit être "Publié" (article) ou "Confirmé" (événement)
2. **Date** : La date de publication n'est pas dans le futur
3. **Cache** : Rafraîchissez la page (Ctrl+F5 ou Cmd+Shift+R)

### L'éditeur de texte ne fonctionne pas

**Solution** :
1. Essayez un autre navigateur (Chrome, Firefox recommandés)
2. Désactivez temporairement les bloqueurs de publicité
3. Videz le cache du navigateur

### Je ne peux pas supprimer une catégorie/un type

**Cause** : Des articles/événements utilisent encore cette catégorie/ce type.

**Solution** :
1. Trouvez les articles/événements concernés
2. Changez leur catégorie/type
3. Ensuite vous pourrez supprimer

---

## 📞 Support technique

### Besoin d'aide ?

**Responsable technique** :
- Email : [adresse email du responsable technique]
- Disponible : [horaires]

**Documentation** :
- Ce guide : [lien vers ce fichier]
- Documentation Django : https://docs.djangoproject.com/

### Signaler un bug

Si vous rencontrez un problème technique :
1. Notez ce que vous faisiez
2. Faites une capture d'écran si possible
3. Contactez le responsable technique avec ces informations

---

## 🎯 Checklist hebdomadaire

**À faire chaque semaine** :

- [ ] Vérifier les nouveaux messages de contact
- [ ] Approuver/modérer les commentaires en attente
- [ ] Vérifier les inscriptions aux événements à venir
- [ ] Publier au moins 1 article (actualités du club)
- [ ] Vérifier les cotisations qui expirent bientôt

**À faire chaque mois** :

- [ ] Créer les événements du mois suivant
- [ ] Vérifier les statistiques (nombre de vues des articles)
- [ ] Archiver les anciens messages de contact traités
- [ ] Marquer les événements passés comme "Terminé"

---

## 📊 Statistiques et rapports

### Voir les statistiques d'un article

1. **"Blog" → "Articles"**
2. Consultez la colonne **"Vues"** pour voir le nombre de lectures
3. Cliquez sur un article pour voir les détails

### Voir les participants à un événement

1. **"Events" → "Inscriptions"**
2. Filtrez par événement
3. Vous voyez la liste complète avec statut et présence

### Exporter des données

Pour exporter une liste (membres, événements, etc.) :
1. Allez dans la section concernée
2. Sélectionnez les éléments (ou tous avec la case en haut)
3. Action : "Exporter en CSV"
4. Ouvrez le fichier avec Excel ou LibreOffice

---

**Dernière mise à jour** : Octobre 2025
**Version** : 1.0
**Contact support** : [email technique]
