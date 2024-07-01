mkdir models

echo "Downloading Whisper models"
bash scripts/download_whisper_models.sh small
bash scripts/download_grounding_dino.sh