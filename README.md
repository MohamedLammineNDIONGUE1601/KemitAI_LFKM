# KemitAI_LFKM
# 🎓 Chatbot Pédagogique — Série S | Lycée Fadel KANE de Matam

Assistant IA pour les élèves de Terminale Série S du Sénégal.

## Installation locale (VS Code)

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# → Ouvrir .env et coller ta clé GEMINI_API_KEY

# 4. Lancer l'application
python app.py
# → Ouvrir http://localhost:5000
```

## Obtenir une clé API Gemini
1. Aller sur https://aistudio.google.com/app/apikey
2. Créer une clé API Google AI Studio
3. Copier la clé dans le fichier .env

## Mise en ligne gratuite sur Render.com

1. Créer un compte sur https://render.com
2. New → Web Service → connecter ton repo GitHub
3. Dans "Environment Variables", ajouter :
   - `GEMINI_API_KEY` = ta clé API
4. Render détecte automatiquement `render.yaml`
5. Deploy → URL publique disponible en ~2 minutes

# KemitAI_LFKM

# 🎓 Chatbot Pédagogique — Série S | Lycée Fadel KANE de Matam

Assistant IA pour les élèves de Terminale Série S du Sénégal.

## Installation locale (VS Code)

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# → Ouvrir .env et coller ta clé GEMINI_API_KEY

# 4. Lancer l'application
python app.py
# → Ouvrir http://localhost:5000
```

## Obtenir une clé API Gemini
1. Aller sur https://aistudio.google.com/app/apikey
2. Créer une clé API Google AI Studio
3. Copier la clé dans le fichier .env

## Mise en ligne gratuite sur Render.com

1. Créer un compte sur https://render.com
2. New → Web Service → connecter ton repo GitHub
3. Dans "Environment Variables", ajouter :
   - `GEMINI_API_KEY` = ta clé API
4. Render détecte automatiquement `render.yaml`
5. Deploy → URL publique disponible en ~2 minutes

## Structure du projet
```
chatbot_serie_s/
├── app.py              ← Backend Flask + API Gemini
├── templates/
│   └── index.html      ← Interface web complète
├── requirements.txt    ← Dépendances Python
├── render.yaml         ← Configuration déploiement
├── .env.example        ← Template variables d'environnement
├── .gitignore
└── README.md
```

## Matières couvertes
- 📐 Mathématiques (coefficient 7)
- ⚗️ Physique-Chimie (coefficient 6)
- 🌱 SVT (coefficient 5)
- ⚙️ Sciences de l'Ingénieur (coefficient 4)
- 💭 Philosophie (coefficient 2)
- 📖 Français (coefficient 2)
