# Lab 10 — Blockchain Invoice Verification

Simulate blockchain-style invoice immutability using a Flask REST API running in Docker. Register an invoice, verify it against a SHA-256 hash, and detect tampering.

**Lab environment:** Docker Desktop (local machine) — required for this lab  
**Estimated time:** 30 minutes

---

## Overview

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check service status |
| `/register` | POST | Register invoice and store its hash |
| `/verify` | POST | Verify invoice — detect tampering |
| `/invoices` | GET | List all registered invoices |

---

## Step 1 — Clone the Lab 10 source from GitHub

```bash
git clone https://github.com/tertiarycourses/TGS-2026064859-Autonomous-AI-Agents-with-OpenClaw.git
cd TGS-2026064859-Autonomous-AI-Agents-with-OpenClaw/labs/lab-10-blockchain-invoice
```

---

## Step 2 — Build the Docker image

```bash
#docker build -t openclaw/invoice-verify:latest .
docker build -t invoice-verify:1.0 .
```

Expected output:
```
Successfully built xxxxxxxxxx
Successfully tagged invoice-verify:latest
```

---

## Step 3 — Run the blockchain verification container

```bash
#docker run -d -p 5000:5000 --name invoice-verify \
  openclaw/invoice-verify:latest

docker run -d \
  --name invoice-verify \
  -p 5000:5000 \
  invoice-verify:1.0
sleep 2
curl http://localhost:5000/health
```

Expected output:
```json
{"invoices": 0, "status": "ok"}
```

---

## Step 4 — Register a test invoice

```bash
curl -X POST http://localhost:5000/store -H "Content-Type: application/json" -d "{\"invoice_id\":\"INV-2026-001\",\"vendor\":\"Tertiary Infotech\",\"amount\":1500.00,\"date\":\"2026-07-11\"}"
```

Expected output:
```
{"status":"stored"}
```

---

## Step 5 — Verify the invoice — same data (should pass)

```bash
curl -X POST http://localhost:5000/verify \
  -H 'Content-Type: application/json' \
  -d '{"invoice_id":"INV-2026-001","vendor":"Tertiary Infotech",
       "amount":1500.00,"date":"2026-07-11"}'
```

Expected output:
```json
{"invoice_id": "INV-2026-001", "verified": true, "tampered": false}
```

---

## Step 6 — Tamper test — change amount (should fail)

```bash
curl -X POST http://localhost:5000/verify \
  -H 'Content-Type: application/json' \
  -d '{"invoice_id":"INV-2026-001","vendor":"Tertiary Infotech",
       "amount":9999.00,"date":"2026-07-11"}'
```

Expected output:
```json
{"invoice_id": "INV-2026-001", "verified": false, "tampered": true}
```

> The SHA-256 hash of the tampered data does not match the stored hash — simulating blockchain immutability.

---
# step 7 -Now perform the tamper test
Change the amount from 1500.00 to 9999.00:

```bash
curl -X POST http://localhost:5000/verify \
-H "Content-Type: application/json" \
-d "{\"invoice_id\":\"INV-2026-001\",\"vendor\":\"Tertiary Infotech\",\"amount\":9999.00,\"date\":\"2026-07-11\"}"

Expected output:
```json
{"invoice_id":"INV-2026-001","tampered":true,"verified":false}

```


```

## Verification

| Check | Expected |
|-------|----------|
| `curl http://localhost:5000/health` | `{"invoices": 1, "status": "ok"}` |
| Verify with correct data | `"verified": true, "tampered": false` |
| Verify with wrong amount | `"verified": false, "tampered": true` |

---

## Cleanup

```bash
docker stop invoice-verify
docker rm invoice-verify
```

---

## Reference

- Lab source code: https://github.com/tertiarycourses/TGS-2026064859-Autonomous-AI-Agents-with-OpenClaw/tree/main/labs/lab-10-blockchain-invoice
- Flask docs: https://flask.palletsprojects.com
