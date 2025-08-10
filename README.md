
# EMS Minimal Demo (Local Docker)

## Overview
Minimal Education Management System scaffold (FastAPI backend, React frontend) for local testing.
Includes Excel import, dynamic attributes (JSON stored in students.data), audit entries, simple analytics.

## Run
Requires Docker & docker-compose.

```
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Notes
- This environment is **for testing only**. Security is intentionally minimal.
- After validating workflows we will add reCAPTCHA server checks, CSRF, rate limiting, DB roles, RLS, backups, and more.
