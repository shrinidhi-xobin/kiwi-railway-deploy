# Kiwi TCMS on Google Cloud Run

This repository packages [Kiwi TCMS](https://kiwitcms.org/) with Google OAuth2 login for deployment on Google Cloud Run.

## Deployment

The container serves plain HTTP on port `8080`. Cloud Run handles HTTPS and forwards requests to Nginx.

1. Enable Cloud Run, Artifact Registry, Cloud Build, and Secret Manager APIs.
2. Create the required secrets and grant the Cloud Run service account `roles/secretmanager.secretAccessor`.
3. Replace the placeholders in [cloudrun-service.yaml](cloudrun-service.yaml).
4. Build and push the image:

```bash
gcloud builds submit \
  --tag REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/kiwi:latest
```

5. Deploy the service manifest:

```bash
gcloud run services replace cloudrun-service.yaml \
  --region REGION
```

6. Allow unauthenticated web access if appropriate:

```bash
gcloud run services add-iam-policy-binding kiwi \
  --region REGION \
  --member="allUsers" \
  --role="roles/run.invoker"
```

For complete configuration, OAuth callback setup, database, Redis, storage, and operations guidance, see [CLOUD_RUN_DEPLOYMENT.md](CLOUD_RUN_DEPLOYMENT.md).

## Important

Cloud Run local storage is ephemeral. Use an external database and durable object storage for production data and uploads. Do not commit credentials or secret values.
