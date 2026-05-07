# Opala AKS — Developer Guide

Deploy any app to Opala's shared Kubernetes cluster in **3 steps**.  
No Docker knowledge, no Azure access, no kubectl required.

---

## What you need

| You provide | Platform provides |
|---|---|
| Your app code | AKS cluster |
| A `Dockerfile` | Azure Container Registry (opalaacr) |
| A `deploy.yml` (copy template below) | CI/CD pipeline, secrets, OIDC auth |

---

## Step 1 — Add a Dockerfile to your repo

Pick the template for your stack from the `dockerfiles/` folder in this repo:

| Stack | Template file |
|---|---|
| Python / FastAPI | `dockerfiles/Dockerfile.fastapi` |
| Python / Flask | `dockerfiles/Dockerfile.flask` |
| Node.js / Express API | `dockerfiles/Dockerfile.node` |
| React (static web app) | `dockerfiles/Dockerfile.react` |
| Next.js | `dockerfiles/Dockerfile.nextjs` |
| .NET / C# API | `dockerfiles/Dockerfile.dotnet` |

Copy the relevant file to the **root of your repo** and rename it `Dockerfile`.  
Edit the `EXPOSE` port if your app uses a different one.

> **Rule:** your app must respond to `GET /health` with HTTP 200.  
> This is how Kubernetes knows your pod is alive. Add it if it doesn't exist yet.

---

## Step 2 — Add deploy.yml to your repo

Create `.github/workflows/deploy.yml` in your repo with this content:

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: choice
        options: [dev, stg, tst, prd]
        default: dev

jobs:
  deploy:
    uses: OpalaDev/opala-platform/.github/workflows/opala-deploy.yml@main
    with:
      app_name:    "your-app-name"    # ← change: lowercase, hyphens only
      app_port:    8000               # ← change: port your app listens on
      replicas:    2                  # ← optional: number of pods
      environment: ${{ inputs.environment || 'dev' }}
    secrets: inherit
```

Change only the `app_name` and `app_port` lines. Everything else stays the same.

---

## Step 3 — Push to main

```bash
git add Dockerfile .github/workflows/deploy.yml
git commit -m "add opala deployment"
git push origin main
```

GitHub Actions runs automatically. Check the **Actions** tab in your repo.  
The public URL is printed at the end of the workflow run.

---

## Rules & conventions

| Rule | Why |
|---|---|
| `app_name` must be lowercase with hyphens only | Kubernetes naming constraint |
| Your app must expose `GET /health` → HTTP 200 | K8s liveness + readiness probe |
| `Dockerfile` must be at the repo root | `az acr build` looks here |
| One `app_name` per repo | Keeps deployments isolated |
| Don't store secrets in code | Use GitHub environment secrets via the platform team |

---

## Environments

| Environment | Branch trigger | Use for |
|---|---|---|
| `dev` | auto on push to `main` | daily development |
| `stg` | manual trigger | pre-release testing |
| `tst` | manual trigger | QA / integration tests |
| `prd` | manual trigger | production release |

---

## FAQ

**My build failed — where do I look?**  
Go to your repo → Actions tab → click the failed run → expand the failing step.

**How do I re-deploy without a code change?**  
Go to Actions → Deploy → Run workflow → pick environment → Run.

**How do I change the number of pods?**  
Edit `replicas:` in your `deploy.yml` and push.

**How do I add environment variables / secrets?**  
Ask the platform team to add them as GitHub environment secrets or Kubernetes secrets.  
Never put secrets in your `Dockerfile` or code.

**I need a database / Redis / blob storage — what do I do?**  
Open a request with the platform team. They'll provision it and give you the connection string as a secret.

**How do I roll back?**  
Go to Actions → find a previous successful run → Re-run jobs.

---

## Need help?

Slack: `#platform-engineering`  
Repo: `OpalaDev/opala-platform`
