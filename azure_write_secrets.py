"""
Azure App Service: materialize .streamlit/secrets.toml before Streamlit starts.

Priority:
1) STREAMLIT_SECRETS — full TOML (if set and non-empty)
2) Else build [auth] + [sharepoint] from individual Application Settings (no 10k limit issues when split).

Run from /home/site/wwwroot: python azure_write_secrets.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _val(s: str | None) -> str | None:
    if s is None:
        return None
    s = s.strip()
    return s if s else None


def _toml_quote(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def build_from_env() -> str | None:
    lines: list[str] = []

    auth = {
        "redirect_uri": _val(os.environ.get("STREAMLIT_AUTH_REDIRECT_URI") or os.environ.get("AUTH_REDIRECT_URI")),
        "cookie_secret": _val(os.environ.get("STREAMLIT_AUTH_COOKIE_SECRET") or os.environ.get("AUTH_COOKIE_SECRET")),
        "client_id": _val(os.environ.get("STREAMLIT_AUTH_CLIENT_ID") or os.environ.get("AUTH_CLIENT_ID")),
        "client_secret": _val(os.environ.get("STREAMLIT_AUTH_CLIENT_SECRET") or os.environ.get("AUTH_CLIENT_SECRET")),
        "server_metadata_url": _val(
            os.environ.get("STREAMLIT_AUTH_SERVER_METADATA_URL") or os.environ.get("AUTH_SERVER_METADATA_URL")
        ),
    }
    if any(auth.values()):
        lines.append("[auth]")
        for k, v in auth.items():
            if v:
                lines.append(f'{k} = {_toml_quote(v)}')
        lines.append("")

    sp = {
        "TENANT_ID": _val(
            os.environ.get("SHAREPOINT_TENANT_ID") or os.environ.get("VIXIS_TENANT_ID") or os.environ.get("TENANT_ID")
        ),
        "CLIENT_ID": _val(
            os.environ.get("SHAREPOINT_CLIENT_ID")
            or os.environ.get("VIXIS_CLIENT_ID")
            or os.environ.get("GRAPH_CLIENT_ID")
            or os.environ.get("CLIENT_ID")
        ),
        "CLIENT_SECRET": _val(
            os.environ.get("SHAREPOINT_CLIENT_SECRET")
            or os.environ.get("VIXIS_CLIENT_SECRET")
            or os.environ.get("GRAPH_CLIENT_SECRET")
            or os.environ.get("CLIENT_SECRET")
        ),
        "RESOURCE": _val(os.environ.get("RESOURCE") or os.environ.get("RESSOURCE")),
        "SITE_URL": _val(os.environ.get("SITE_URL")),
        "DRIVE_ID": _val(os.environ.get("DRIVE_ID")),
        "FOLDER_ID": _val(os.environ.get("FOLDER_ID")),
        "MONGO_URL": _val(os.environ.get("MONGO_URL")),
        "DB_NAME": _val(os.environ.get("DB_NAME")),
    }
    if any(sp.values()):
        lines.append("[sharepoint]")
        for k, v in sp.items():
            if v:
                lines.append(f'{k} = {_toml_quote(v)}')

    return "\n".join(lines).strip() or None


def main() -> int:
    root = Path(os.environ.get("WEBSITE_SITE_PATH", "/home/site/wwwroot"))
    if not root.is_dir():
        root = Path.cwd()
    out_path = root / ".streamlit" / "secrets.toml"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    raw = _val(os.environ.get("STREAMLIT_SECRETS"))
    if raw:
        text = raw
        source = "STREAMLIT_SECRETS"
    else:
        built = build_from_env()
        if not built:
            print(
                "azure_write_secrets: no STREAMLIT_SECRETS and no individual auth/sharepoint env vars; "
                "secrets.toml not written.",
                file=sys.stderr,
                flush=True,
            )
            return 1
        text = built
        source = "env_vars"

    out_path.write_text(text, encoding="utf-8")

    try:
        import tomllib

        tomllib.loads(text)
    except Exception as e:
        print(f"azure_write_secrets: invalid TOML after write: {e}", file=sys.stderr, flush=True)
        return 1

    # Safe diagnostics (no secret values)
    keys_preview = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line and not line.startswith("["):
            k = line.split("=", 1)[0].strip()
            keys_preview.append(k)

    print(
        f"azure_write_secrets: wrote {out_path} from {source}, bytes={out_path.stat().st_size}, keys={keys_preview[:12]}...",
        file=sys.stderr,
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
