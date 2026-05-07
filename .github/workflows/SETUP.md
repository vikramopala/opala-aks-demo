# Opala AKS Deployment — One-Time Setup Guide

Developers only need to do **Step 3** for each new app.
Steps 1 and 2 are done once by the platform team.

---

## Step 1 — Platform team: create the Azure service principal (once)

Run in Azure Cloud Shell:

```bash
az ad sp create-for-rbac \
  --name "opala-github-deploy" \
  --role Contributor \
  --scopes /subscriptions/<your-subscription-id> \
  --sdk-auth
```

Copy the full JSON output. Add it as a GitHub **organisation secret** named `AZURE_CREDENTIALS`
in: `github.com/opala-org` → Settings → Secrets → Actions → New organisation secret.

---

## Step 2 — Platform team: host the reusable workflow (once)

Create a repo called `opala-platform` in the `opala-org` GitHub organisation.
Copy `opala-deploy.yml` into `.github/workflows/` in that repo.

---

## Step 3 — Developer: add deploy.yml to your app repo (per app)

1. Copy `deploy.yml` into your repo at `.github/workflows/deploy.yml`
2. Edit the three lines under `with:`:

```yaml
with:
  app_name: "your-app-name"   # ← change this
  app_port: 8000               # ← change to your app's port
  replicas: 2                  # ← optional
```

3. Push to `main` — GitHub Actions deploys automatically.
4. Check the Actions tab for the public URL printed at the end.

---

## What the developer does NOT need to know

- Azure credentials
- ACR name or login
- kubectl commands
- AKS cluster name
- Docker build commands
- Pull secret management

All of that is handled by `opala-deploy.yml` centrally.

---

## Repo structure required in each app

```
your-app/
├── Dockerfile          ← required (app must have this)
├── .github/
│   └── workflows/
│       └── deploy.yml  ← copy from this template, edit 3 lines
└── ... (your app code)
```
