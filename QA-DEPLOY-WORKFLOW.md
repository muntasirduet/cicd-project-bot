# 🔍 QA-Gated Deployment Workflow

## Overview

Every deployment to **staging** or **production** must pass QA first.
You (or the team) review the QA report in Discord, then approve with `deploy`.

---

## 🔄 Full Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 1. Trigger  │───►│ 2. QA Test  │───►│ 3. Discord  │───►│ 4. Deploy   │
│    (You)    │    │   (Auto)    │    │  Approval   │    │  (Auto)     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 🚀 How to Use

### Option A: Through Me (Discord)

1. **Tell me to QA:**
   ```
   @Hermes QA my-cicd-project
   ```

2. **I run tests and post report:**
   ```
   🔍 QA Report — my-cicd-project
   ✅ Root Endpoint — 200 (9ms)
   ✅ Health Check — 200 (4ms)
   ✅ Deploy Info — 200 (3ms)
   ✅ 404 Handler — 404 (2ms)
   
   🏆 Verdict: PASS ✅
   ```

3. **You approve:**
   ```
   deploy
   ```

4. **I deploy:**
   ```
   🚀 Deploying...
   ✅ Deployed successfully!
   ```

### Option B: GitHub Actions (Self-Service)

1. Go to **Actions → QA-Gated Deploy**
2. Click **Run workflow**
3. Select environment (staging / production)
4. Workflow runs QA tests → pauses for approval
5. Approved user clicks **Approve** → deploys automatically

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `qa-deploy.py` | Automated QA test runner |
| `deploy.sh` | Manual deploy script |
| `.github/workflows/qa-gated-deploy.yml` | GitHub Actions workflow |
| `qa-report.json` | Machine-readable test results |
| `qa-report.md` | Human-readable Discord report |

---

## ✅ What QA Checks

| Test | Description |
|------|-------------|
| Root Endpoint | Returns welcome message + valid timestamp |
| Health Check | Returns `{status: "healthy"}` |
| Deploy Info | Returns metadata with .NET version |
| 404 Handler | Invalid routes return 404 correctly |
| Performance | Average response time < 50ms |

---

## ⚠️ Adding More Tests

Edit `qa-deploy.py` and add to the `tests` list:

```python
("My New Feature", "GET", "/api/feature", 200, lambda r: "expected" in r.text),
```

---

## 🔐 Required Secrets (for GitHub Actions)

| Secret | Purpose |
|--------|---------|
| `SSH_PRIVATE_KEY` | Deploy to server via SSH |
| `SERVER_HOST` | Target server IP/hostname |
| `SERVER_USER` | SSH username |
| `PROD_URL` | Post-deploy health check URL |

---

## 🛠️ For nopCommerce Projects

When you switch to nopCommerce, I will add:
- Admin panel navigation tests
- Plugin configuration form validation
- Responsive breakpoint checks
- JavaScript console error detection
- Screenshot comparison (visual regression)

---

## 💬 Discord Commands

| Command | What I Do |
|---------|-----------|
| `qa` or `qa my-cicd-project` | Run QA tests + post report |
| `deploy` | Deploy the project (after QA pass) |
| `qa force` | Skip QA and deploy immediately |
| `status` | Check if API is running + health |
