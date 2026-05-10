---

## 👤 User Stories

### Définition d une User Story

Une User Story suit le format :
> **En tant que** [type d utilisateur], **je veux** [action], **afin de** [bénéfice]

### Démarche de développement d une User Story

- [ ] Rédaction de la User Story avec critères d acceptation
- [ ] Découpage en tâches techniques
- [ ] Création d une branche `feature/nom-fonctionnalite`
- [ ] Développement du back-end (modèle, serializer, vue, URL)
- [ ] Développement du front-end (composant React, CSS)
- [ ] Tests unitaires
- [ ] Code review
- [ ] Merge sur `develop`
- [ ] Mise à jour du statut → **Done**

---

### US-01 — Consultation des véhicules ✅ DONE

**En tant que** visiteur, **je veux** consulter la liste des véhicules disponibles, **afin de** trouver un véhicule qui correspond à mes besoins.

**Critères d acceptation :**
- Les véhicules s affichent sans connexion
- Chaque véhicule affiche : photo, marque, modèle, année, kilométrage, carburant, prix
- Un filtre permet de trier par Achat / Location / Tous
- Une barre de recherche permet de chercher par marque ou modèle

**Tâches techniques :**
- Modèle `Vehicle` avec tous les champs nécessaires
- API `GET /api/vehicles/` accessible sans authentification
- Page `VehicleList.jsx` avec grille responsive
- Filtres et recherche côté React

**Statut : ✅ DONE**

---

### US-02 — Détail d un véhicule ✅ DONE

**En tant que** visiteur, **je veux** voir le détail complet d un véhicule, **afin d** avoir toutes les informations avant de faire une demande.

**Critères d acceptation :**
- Page dédiée accessible en cliquant sur un véhicule
- Affichage : photo, caractéristiques complètes, description, prix
- Si non connecté : message invitant à s inscrire
- Si connecté : boutons Acheter / Louer visibles

**Tâches techniques :**
- API `GET /api/vehicles/:id/`
- Page `VehicleDetail.jsx` avec grille de caractéristiques
- Gestion de l état connecté/non connecté

**Statut : ✅ DONE**

---

### US-03 — Inscription ✅ DONE

**En tant que** visiteur, **je veux** créer un compte, **afin de** pouvoir déposer un dossier d achat ou de location.

**Critères d acceptation :**
- Formulaire avec : prénom, nom, username, email, téléphone, mot de passe
- Redirection vers la page connexion après inscription
- Message d erreur si le username existe déjà

**Tâches techniques :**
- Modèle `CustomUser` étendant `AbstractUser`
- API `POST /api/register/`
- Page `Register.jsx`

**Statut : ✅ DONE**

---

### US-04 — Connexion ✅ DONE

**En tant que** client inscrit, **je veux** me connecter à mon espace, **afin d** accéder à mes dossiers et mon profil.

**Critères d acceptation :**
- Connexion avec username et mot de passe
- Token JWT stocké localement
- Navbar mise à jour après connexion
- Message d erreur si identifiants incorrects

**Tâches techniques :**
- API `POST /api/auth/login/` avec JWT
- Contexte `AuthContext.jsx`
- Page `Login.jsx`
- Intercepteur Axios pour token automatique

**Statut : ✅ DONE**

---

### US-05 — Dépôt de dossier ✅ DONE

**En tant que** client connecté, **je veux** déposer un dossier d achat ou de location, **afin de** soumettre ma demande à l équipe AutoDeal.

**Critères d acceptation :**
- Accessible uniquement après connexion
- Formulaire avec : date de début, date de fin (location), notes
- Calcul automatique du montant total
- Confirmation après soumission

**Tâches techniques :**
- Modèle `Contract` avec statuts multiples
- API `POST /api/contracts/`
- Page `NewDossier.jsx`

**Statut : ✅ DONE**

---

### US-06 — Suivi des dossiers ✅ DONE

**En tant que** client connecté, **je veux** suivre l avancement de mes dossiers, **afin de** savoir où en est ma demande.

**Critères d acceptation :**
- Liste de tous mes dossiers avec statut coloré
- Timeline visuelle : Déposé → Documents reçus → En vérification → Approuvé
- Possibilité d annuler un dossier en attente
- Clic sur un dossier pour voir le détail

**Tâches techniques :**
- API `GET /api/contracts/` filtrée par utilisateur
- Pages `Dossiers.jsx` et `DossierDetail.jsx`
- Timeline CSS animée

**Statut : ✅ DONE**

---

### US-07 — Documents dématérialisés ✅ DONE

**En tant que** client connecté, **je veux** télécharger les documents requis et uploader mes justificatifs, **afin de** constituer mon dossier 100% en ligne.

**Critères d acceptation :**
- Téléchargement du formulaire de dossier
- Téléchargement de la liste des documents requis
- Upload de la CNI, justificatif de domicile et fiche de paie
- Statut de vérification visible pour chaque document
- Statut du dossier mis à jour automatiquement quand tous les documents sont reçus

**Tâches techniques :**
- Modèle `ClientDocument` lié au contrat
- API `POST /api/contracts/:id/upload_document/`
- Page `DossierDetail.jsx` avec section upload
- Génération de documents téléchargeables

**Statut : ✅ DONE**

---

### US-08 — Profil utilisateur ✅ DONE

**En tant que** client connecté, **je veux** consulter et modifier mon profil, **afin de** garder mes informations à jour.

**Critères d acceptation :**
- Affichage des informations personnelles
- Modification du prénom, nom, email, téléphone, ville, adresse
- Statistiques : nombre de dossiers, achats, locations
- Déconnexion depuis le profil

**Tâches techniques :**
- API `GET /api/profile/` et `PATCH /api/profile/update/`
- Page `Profile.jsx` avec mode édition
- Serializer `UserSerializer` avec champs partiels

**Statut : ✅ DONE**

---

## 🏗️ Architecture du projet
---

## 🚀 Installation et lancement

### Prérequis
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+

### Back-end
```bash
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Front-end
```bash
cd frontend
npm install
npm run dev
```

### Variables d environnement
Créer un fichier `.env` dans `backend/` :