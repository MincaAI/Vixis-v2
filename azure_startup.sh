#!/bin/bash
# Azure App Service: Streamlit only reads .streamlit/secrets.toml — not the STREAMLIT_SECRETS env var.
# This script materializes STREAMLIT_SECRETS into that file, then starts the app.
set -e
cd /home/site/wwwroot
mkdir -p .streamlit
python - <<'PY'
import os
from pathlib import Path

raw = os.environ.get("STREAMLIT_SECRETS", "").strip()
if raw:
    Path(".streamlit/secrets.toml").write_text(raw, encoding="utf-8")
PY
pip install -r requirements.txt
exec python -m streamlit run main.py --server.port 8000 --server.address 0.0.0.0
