# Vixis

## Déploiement sur Streamlit Cloud

Pour que l’app fonctionne après déploiement :

1. **Commande de lancement** : `streamlit run main.py`

2. **Secrets** (Streamlit Cloud : *Settings → Secrets*) — à renseigner au format TOML :

   **Authentification Microsoft (connexion utilisateur) :**
   ```toml
   [auth]
   redirect_uri = "https://VOTRE-APP.streamlit.app/oauth2callback"
   cookie_secret = "une-chaîne-aléatoire-longue"
   client_id = "..."
   client_secret = "..."
   server_metadata_url = "https://login.microsoftonline.com/VOTRE_TENANT_ID/v2.0/.well-known/openid-configuration"
   ```
   Important : `redirect_uri` doit être l’URL de votre app déployée (ex. `https://vixispro.streamlit.app/oauth2callback`), et la même URL doit être enregistrée comme URI de redirection dans Azure/Entra.

   **SharePoint et MongoDB (bouton « Update Data ») :**
   ```toml
   [sharepoint]
   TENANT_ID = "..."
   CLIENT_ID = "..."
   CLIENT_SECRET = "..."
   RESOURCE = "https://graph.microsoft.com/"
   SITE_URL = "vixis.sharepoint.com:/sites/Intranet"
   DRIVE_ID = "..."
   FOLDER_ID = "..."
   MONGO_URL = "mongodb+srv://..."
   DB_NAME = "Vixis"
   ```

3. **Si la connexion Microsoft ne marche pas** : vérifier dans Azure/Entra que l’URI de redirection de l’application correspond exactement à `https://VOTRE-APP.streamlit.app/oauth2callback`.