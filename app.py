# ─── app.py — Chatbot pédagogique Série S — Lycée Fadel KANE de Matam ──────
import os
from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from dotenv import load_dotenv
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cle_secrete_a_changer")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

# Configuration de Google Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ════════════════════════════════════════════════════════════════════════════
#  SYSTEM PROMPT — Programme Série S Sénégal (INSPÉ / CRFPE)
# ════════════════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """
Tu es un assistant pédagogique expert conçu spécifiquement pour les élèves
de la Série Scientifique (Série S) du Lycée Fadel KANE de Matam, au Sénégal.

## Ton rôle
Tu aides les élèves à comprendre les cours, résoudre des exercices et préparer
le Baccalauréat selon le programme officiel sénégalais de la Série S (INSPÉ / CRFPE).

## Matières couvertes (programme officiel Série S Sénégal)

### Mathématiques (coefficient 7)
- Analyse : fonctions, limites, dérivées, intégrales, équations différentielles
- Algèbre : suites numériques, dénombrement, probabilités, arithmétique, nombres complexes
- Géométrie : trigonométrie, géométrie dans l'espace, vecteurs, transformations
- Statistiques et probabilités

### Sciences Physiques — Physique-Chimie (coeff. 6)
**Physique :**
- Mécanique : cinématique, dynamique, énergie, gravitation universelle
- Électricité : dipôles, circuits RC/RL/RLC, régimes transitoires et sinusoïdaux
- Optique : optique géométrique, ondes lumineuses, diffraction
- Ondes mécaniques et acoustique

**Chimie :**
- Structure de la matière, liaisons chimiques
- Cinétique chimique, équilibres, pH, acides/bases
- Électrochimie : piles, électrolyse, oxydoréduction
- Chimie organique : fonctions organiques, réactions

### Sciences de la Vie et de la Terre — SVT (coeff. 5)
- Biologie cellulaire et moléculaire : ADN, génétique, héritage
- Physiologie : digestion, nutrition, respiration, circulation, reproduction
- Géologie : tectonique des plaques, roches, gisements, histoire de la Terre
- Écologie et environnement

### Sciences de l'Ingénieur (coeff. 4)
- Analyse fonctionnelle et structurelle des systèmes
- Mécanique des solides, transmission de puissance
- Automatique et asservissement
- Électrotechnique appliquée

### Philosophie (coeff. 2)
- Notions du programme : le sujet, la culture, la raison, la connaissance
- La morale et la politique
- Méthodologie : dissertation, explication de texte

### Français (coeff. 2)
- Littérature et textes du programme
- Commentaire composé, dissertation littéraire
- Grammaire et expression écrite

## Tes règles de conduite

1. **Langue** : Réponds toujours en français clair et accessible.
2. **Pédagogie** : Explique étape par étape. Utilise des exemples concrets
   tirés de la vie quotidienne au Sénégal quand c'est pertinent.
3. **Rigueur** : Donne des réponses exactes et conformes au programme officiel.
   Ne confonds pas avec d'autres systèmes éducatifs (français, américain, etc.).
4. **Encouragement** : Reste bienveillant et motivant. Les élèves peuvent avoir
   des lacunes — aide-les à progresser sans les décourager.
5. **Exercices** : Quand un élève te soumet un exercice, guide-le plutôt que
   de donner directement la réponse. Pose des questions socratiques.
6. **BAC** : Si la question porte sur le Baccalauréat sénégalais, rappelle les
   attentes officielles (présentation, notation, structure des copies).
7. **Limites** : Si une question sort du programme Série S, précise-le
   gentiment et recentre sur le programme.
8. **Format** : Utilise des formules LaTeX pour les maths avec la notation
   $...$ pour l'inline et $$...$$ pour les blocs. Structure tes réponses
   avec des titres clairs quand c'est utile.

## Exemple d'introduction
Quand tu te présentes, dis :
"Bonjour ! Je suis ton assistant pédagogique pour la Série S au Lycée Fadel KANE.
Je peux t'aider en Maths, Physique-Chimie, SVT, Sciences de l'Ingénieur,
Philosophie et Français. Quelle matière veux-tu travailler aujourd'hui ?"
"""

# Initialisation du modèle avec les instructions système
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)


def build_fallback_response(user_message):
    message = user_message.lower()

    if any(word in message for word in ["limite", "fonction", "dérivée", "derivee", "intégrale", "integrale"]):
        return (
            "Je ne peux pas joindre Gemini pour le moment, mais voici un point de départ sur les fonctions :\n\n"
            "- Vérifie d’abord le domaine de définition.\n"
            "- Cherche la formule principale: dérivée, limite ou intégrale selon la question.\n"
            "- Fais un exemple simple avec une fonction comme f(x)=x² ou f(x)=1/x.\n\n"
            "Si tu veux, écris exactement l’exercice et je te guiderai pas à pas."
        )

    if any(word in message for word in ["mitose", "svt", "cellule", "adn", "génétique", "genetique"]):
        return (
            "Je ne peux pas joindre Gemini pour le moment, mais voici un point de départ sur la biologie cellulaire :\n\n"
            "- Commence par définir le mot clé: cellule, ADN, mitose ou génétique.\n"
            "- Relie la notion à son rôle dans le vivant.\n"
            "- Ajoute un schéma ou une étape du processus si c’est demandé.\n\n"
            "Si tu veux, envoie la phrase exacte de ton cours ou de ton exercice."
        )

    if any(word in message for word in ["philo", "dissertation", "argument", "thèse", "these", "texte"]):
        return (
            "Je ne peux pas joindre Gemini pour le moment, mais voici un point de départ pour la philosophie :\n\n"
            "- Identifie le sujet exact et les notions qu’il contient.\n"
            "- Formule une problématique claire.\n"
            "- Construis un plan simple: thèse, antithèse, dépassement.\n\n"
            "Si tu veux, donne-moi le sujet et je t’aide à bâtir le plan."
        )

    if any(word in message for word in ["rc", "circuit", "physique", "électricité", "electricite", "courant"]):
        return (
            "Je ne peux pas joindre Gemini pour le moment, mais voici un point de départ sur les circuits électriques :\n\n"
            "- Repère les grandeurs: tension, courant, résistance, capacité.\n"
            "- Utilise la loi d’Ohm si le circuit est simple.\n"
            "- Si c’est un circuit RC, pense à la charge et à la décharge du condensateur.\n\n"
            "Si tu veux, envoie le schéma du circuit ou l’énoncé exact."
        )

    return (
        "Je ne peux pas joindre Gemini pour le moment, mais je peux quand même t’aider à avancer :\n\n"
        "- Reformule la question en une phrase simple.\n"
        "- Repère la matière concernée et les mots-clés.\n"
        "- Donne-moi l’énoncé exact, et je te propose une méthode de résolution.\n\n"
        "Si tu veux, renvoie le message plus tard pour obtenir une réponse complète."
    )

# ════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    if "conversation_id" not in session:
        session["conversation_id"] = str(uuid.uuid4())
    if "messages" not in session:
        session["messages"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    # Debug: log raw request body and headers to help diagnose bad requests
    raw_req = request.get_data(as_text=True)
    print("DEBUG RAW REQUEST:", repr(raw_req))
    try:
        print("DEBUG HEADERS:", dict(request.headers))
    except Exception:
        pass

    data = request.get_json(silent=True)
    if not data:
        print("DEBUG: request.get_json returned None or invalid JSON")
        return jsonify({"error": "Corps JSON invalide ou en-tête manquant"}), 400

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message vide"}), 400

    if not GEMINI_API_KEY:
        return jsonify({
            "error": "GEMINI_API_KEY manquante. Ajoute une clé Google Gemini valide dans .env ou dans les variables d'environnement de Render."
        }), 500

    if "messages" not in session:
        session["messages"] = []

    messages = session["messages"]
    
    # Limiter l'historique à 40 messages pour éviter d'alourdir la session Flask
    if len(messages) >= 40:
        messages = messages[-38:] # Conserve un nombre pair pour garder la cohérence Alternance User/Model

    try:
        # Traduction de l'historique Flask vers le format attendu par l'API Gemini
        # Gemini utilise 'model' au lieu d' 'assistant'
        gemini_history = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [m["content"]]})

        # Initialisation du chat avec l'historique des messages précédents
        chat_session = model.start_chat(history=gemini_history)
        
        # Envoi du nouveau message de l'élève
        response = chat_session.send_message(user_message)
        assistant_message = response.text

        # Sauvegarde de l'échange actuel (au format d'origine pour votre front-end si nécessaire)
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": assistant_message})
        
        session["messages"] = messages
        session.modified = True

        # Note : L'API Gemini standard ne renvoie pas l'usage exact des tokens de la même manière
        # dans la réponse textuelle directe, nous omettons donc "tokens_used" pour éviter les erreurs.
        return jsonify({
            "response": assistant_message
        })

    except Exception as e:
        error_text = str(e).lower()
        if "quota" in error_text or "rate limit" in error_text or "429" in error_text or "resource exhausted" in error_text:
            fallback_message = build_fallback_response(user_message)
            messages.append({"role": "user", "content": user_message})
            messages.append({"role": "assistant", "content": fallback_message})
            session["messages"] = messages
            session.modified = True
            return jsonify({"response": fallback_message, "fallback": True}), 200
        if "invalid x-api-key" in error_text or "api key not valid" in error_text or "unauthenticated" in error_text:
            return jsonify({
                "error": "Clé Gemini invalide. Remplace GEMINI_API_KEY par une clé Google AI Studio valide, puis redémarre l'application."
            }), 401
        return jsonify({"error": f"Erreur API Gemini : {str(e)}"}), 500


@app.route("/reset", methods=["POST"])
def reset():
    session["messages"] = []
    session.modified = True
    return jsonify({"status": "ok", "message": "Conversation réinitialisée."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)