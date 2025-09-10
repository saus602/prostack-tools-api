# ProStack Tools API — QuickStart

**Goal:** Run a minimal API that your ProStack GPT (via Actions) and your WordPress site can both call.  
This bundle gives you:
- FastAPI app with license gating (`x-ps-license`)
- Endpoints: intake, parse reports (mock), prequal (mock), stack optimize (mock), applications, status, sub-tracker
- OpenAPI spec (served at `/openapi.json` automatically)
- WordPress plugin to mint & display licenses after WooCommerce checkout
- Postman collection for testing
- GPT Instructions template

> Built for fast deployment and easy iteration. Start mocked → later swap in real logic.

---

## 0) Prereqs

- **Python 3.11+** (recommended)
- **pip** (or uv / pipx if you prefer)
- Windows users: Prefer `psycopg[binary]` wheels; avoid building `psycopg2-binary` from source

---

## 1) Run the API locally

```bash
cd prostack-tools-api
python -m venv .venv
# Windows:
#   .venv\Scripts\activate
# macOS/Linux:
#   source .venv/bin/activate

pip install -r requirements.txt

# Copy env
cp .env.sample .env

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Open: <http://localhost:8080/docs> and <http://localhost:8080/openapi.json>

**Health check**:
```bash
curl http://localhost:8080/health
```

---

## 2) Expose your API for GPT Actions

Pick one (examples; use whichever you already like):

- **Railway/Render/Fly.io/Vercel (server)**: Deploy this directory as a service with Python buildpack.
- **Cloudflare Tunnel or ngrok**: Point a secure tunnel to `http://localhost:8080` to get a public URL.
- Map DNS: `api.yourdomain.com` → your service URL.

Once live, confirm: `https://api.yourdomain.com/openapi.json` loads.

---

## 3) Connect your Custom GPT (Actions)

In *GPT Builder → Configure → Actions → Import from URL*:  
- Paste your OpenAPI URL: `https://api.yourdomain.com/openapi.json`
- Security: **API Key (Header)** with name `x-ps-license` (the GPT will ask the user to paste their license)
- Tool description should mirror operation summaries so GPT picks correctly.

---

## 4) Install the WordPress Plugin (License Bridge)

- Zip the `wp-plugin/prostack-license-bridge` folder, upload via **Plugins → Add New → Upload**.
- Activate.
- Go to **Settings → ProStack License Bridge**:
  - API URL: `https://api.yourdomain.com`
  - Woo Secret: set a long random string, also put it in `.env` under `WOO_WEBHOOK_SECRET`.
- Add shortcode `[prostack_license]` to your **Order Received** page or **My Account**.

On **order completed**, the plugin calls `/v1/licenses`, saves the license to the user, and shows it via shortcode. The client then pastes this license into the GPT.

---

## 5) Test with Postman

Import `postman/ProStack.postman_collection.json` and run the requests (set the `x-ps-license` you received).

---

## 6) Swap mock logic for real

- Edit `app/routes/*.py` and `app/core/*.py`.
- Replace stubs in:
  - `reports.py` → parse PDF/JSON of credit reports
  - `prequal.py` → call prequal aggregators (non-scraping)
  - `stack.py` → your rules engine + optimizer
- Add persistence (Postgres) later (this starter uses in-memory + JSON files for speed).

---

## 7) Windows notes (build errors)

If you saw `pydantic-core` or `psycopg2-binary` wheel errors:
```bash
pip install "psycopg[binary]==3.1.18"
pip install "pydantic==2.8.2" "pydantic-core==2.20.1"
```
(Already pinned in `requirements.txt`.)

---

## 8) Security

- All “real” endpoints require header: `x-ps-license: <license>`
- `/v1/licenses` also checks `X-Woo-Signature` when invoked by WP
- Do not store full credentials or OTPs; keep PII encrypted-at-rest when you add a DB
- Rotate secrets; enable TLS

---

## 9) File map

```
prostack-tools-api/
  app/
    main.py
    deps.py
    models.py
    core/
      auth.py
      rules_engine.py
    routes/
      health.py
      licenses.py
      intake.py
      reports.py
      prequal.py
      stack.py
      applications.py
      subtracker.py
  data/
    licenses.json
  requirements.txt
  .env.sample
  README.md (this file)
```

Happy stacking!
