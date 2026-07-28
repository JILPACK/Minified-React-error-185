# Worker Mini — Ministral 3.3B

Worker IA intégrant le modèle [Ministral-3-3B-Instruct-2512](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512) (Mistral AI) comme backend d'inférence locale.

## Prérequis

```
pip install -r requirements.txt
```

Nécessite ~4GB de RAM/VRAM. GPU CUDA recommandé mais CPU fonctionne.

## Utilisation

```bash
# Serveur API (port 8742)
python model_worker.py

# Client CLI interactif
python chat_client.py

# Mode CLI
python model_worker.py --cli

# One-shot
python model_worker.py --text "Bonjour, qui es-tu?"
```

## API

| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/v1/chat/completions` | Chat (compatible OpenAI) |
| GET | `/v1/models` | Liste des modèles |
| GET | `/health` | Health check |

## Intégration GUI

L'onglet "Worker IA" dans `flux-gui.py` permet de lancer/arrêter le worker
et de chatter directement depuis l'interface.
