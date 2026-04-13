#!/bin/bash
# Azure: Streamlit reads .streamlit/secrets.toml only — see azure_write_secrets.py
set -e
cd /home/site/wwwroot
mkdir -p .streamlit
python azure_write_secrets.py
pip install -r requirements.txt
exec python -m streamlit run main.py --server.port 8000 --server.address 0.0.0.0
