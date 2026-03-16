# AURA-Nepal Backend Plan

## Objective
Implement backend MVP as the data engine for existing Django template frontend.

## Scope (This implementation)
- Create `app` Django app as the main backend module.
- Move UI templates to `templates/app/` and route them through backend views.
- Implement core backend data models for upload, detection, carbon, verification, and finance.
- Add backend endpoints for upload intake, processing simulation, analytics summary, and transaction listing.
- Register all models in admin and keep media routes enabled.

## Step-by-Step Plan
1. Create and wire `app` in settings and root URLs.
2. Move templates from `templates/stitch_ui/` to `templates/app/`.
3. Refactor template inheritance to use `app/base.html`.
4. Implement backend models:
   - `UserProfile`
   - `MediaUpload`
   - `TreeDetection`
   - `CarbonRecord`
   - `VerificationLedger`
   - `FinanceTransaction`
5. Implement backend views and URL routes:
   - Home + page router
   - Media upload endpoint
   - AI processing trigger endpoint (MVP simulation)
   - Analytics JSON endpoint
   - Finance transaction JSON endpoint
6. Register models in admin.
7. Run migrations and validation checks.

## Notes
- AI detection is scaffolded as a deterministic simulation for MVP; real YOLO/Celery pipeline can plug into the same model flow.
- SQLite is kept for now; schema is compatible with moving to PostgreSQL/PostGIS in next phase.
