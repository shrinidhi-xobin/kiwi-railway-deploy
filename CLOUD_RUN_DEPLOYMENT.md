# Cloud Run Deployment

## Container Contract

The image serves plain HTTP on port `8080`. Cloud Run terminates HTTPS at the edge and forwards requests to Nginx inside the container.

Build and deploy:

```bash
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/kiwi:latest

gcloud run deploy kiwi \
  --image REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/kiwi:latest \
  --region REGION \
  --port 8080 \
  --allow-unauthenticated
```

Before deployment, test the image locally:

```bash
docker build -t kiwi-cloudrun .
docker run --rm -p 8080:8080 -e PORT=8080 kiwi-cloudrun
curl http://localhost:8080/
```

## Required Configuration

Set these through Cloud Run environment variables or Secret Manager. Do not commit values to the repository.

- Django secret key required by the Kiwi base image
- Database connection settings required by the Kiwi base image
- Redis/cache connection settings, if enabled
- `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`
- `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET`
- `SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAIN` when domain restriction is required
- `ALLOWED_HOSTS` containing the Cloud Run URL and any custom domain
- `CSRF_TRUSTED_ORIGINS` containing `https://` versions of those domains

Use Secret Manager for sensitive values:

```bash
gcloud run services update kiwi \
  --region REGION \
  --set-secrets DJANGO_SECRET_KEY=kiwi-django-secret:latest,SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=google-oauth-client-id:latest,SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=google-oauth-client-secret:latest
```

The Cloud Run service account needs `roles/secretmanager.secretAccessor` for those secrets.

## Google OAuth

Add the exact callback URL to the Google OAuth client:

```text
https://SERVICE-HASH-REGION.a.run.app/complete/google-oauth2/
```

For a custom domain, add:

```text
https://YOUR_DOMAIN/complete/google-oauth2/
```

The OAuth client origin should also include the public Cloud Run or custom domain origin.

## Persistent Data

Cloud Run instances have ephemeral local storage. `/Kiwi/uploads/` must not be treated as durable storage. Configure Kiwi to use durable external storage, preferably Google Cloud Storage, for uploaded attachments and media. If the base image cannot be configured for object storage, use a supported Cloud Run volume strategy and verify concurrent read/write behavior.

## Database and Redis

Use managed external services:

- Cloud SQL or the supported external database for Kiwi
- Memorystore or another private Redis endpoint when Redis is required

Configure VPC egress or a Serverless VPC Access connector when those services are private. Run database migrations before serving traffic, and set Cloud Run connection limits appropriate for autoscaling.

## Operations

- Pin the Kiwi base image to a tested version or digest instead of `latest` before production rollout.
- Configure a startup probe and monitor container logs.
- Set request timeout and memory based on attachment upload size.
- Set `min-instances=1` if cold-start latency is unacceptable.
- Confirm session storage is shared across instances.
- Verify uploads, Google login, logout, CSRF, password reset, and static assets after deployment.
