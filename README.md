# Amogus Chatbot (Flutter + Flask)

Base minimale pour un chatbot Amogus avec une UI Flutter et un backend Flask qui génère des réponses humoristiques et permet d'ajouter vos propres répliques.

## Backend (Python + Flask)
1) Créer l'environnement et installer les dépendances :
```
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
2) Lancer l'API :
```
python app.py
```
- Endpoint chat : `POST http://localhost:5000/chat` body JSON `{ "message": "..." }`
- Endpoint train : `POST http://localhost:5000/train` body JSON `{ "example": "nouvelle punchline" }`
- Santé : `GET http://localhost:5000/health`

Les répliques sont stockées dans `backend/data/corpus.json`. Vous pouvez y ajouter des lignes ou passer par `/train`.

## Frontend (Flutter)
1) Installer les dépendances :
```
cd frontend
flutter pub get
```
2) Lancer l'app (web ou mobile) :
```
flutter run
```
L'app appelle le backend sur `http://localhost:5000/chat`. Adaptez l'URL dans `lib/main.dart` si besoin (ex. déploiement distant).

### Structure
- `frontend/lib/main.dart` : page de chat avec bulles, avatar Amogus (asset `src/assets/Amogus.png`) et appel HTTP.
- `backend/app.py` : endpoints `/chat`, `/train`, stockage simple dans `data/corpus.json`.

### Entraîner votre IA maison
- Ajoutez des blagues ou punchlines via `/train` ou directement dans `corpus.json`.
- L'algorithme actuel est volontairement simple (sélection + mini-templates). Vous pouvez le remplacer par votre propre modèle ou pipeline tout en gardant les mêmes endpoints.
