# Estimator

Engineering project hub — a single-file HTML web app (no database, no build step). Data is stored in the browser (localStorage) and, when signed in with the admin account on the front page, synced to Supabase (table `estimator_data`, key `main`). The front page's **Backup everything (JSON)** keeps an extra copy.

Open `index.html` in any browser, or enable GitHub Pages for this repo to use it online.

## Estimates
Plants are grouped into estimates on the front page (default: **Estimate 1** = H1, **Estimate 2** = H4, M1, W1). Each plant belongs to one estimate; an Estimate switch in the Register, Drawing Quantities and Other Deliverables modules filters by estimate, and the Cost Estimate Page shows the estimates side by side.

## Modules
- **Equipment Types Module** — define each equipment type once (Discipline, Name, optional Variant) with the drawings needed per one unit, per drawing type, for Stage 1 and Stage 2. Also manages the drawing types (abbreviation, full name, drawing size).
- **Drawings Register Module** — pick Plant (H4, H1, M1, W1), equipment and quantity; drawings required per drawing type are calculated automatically.
- **Drawing Quantities Module** — quantity of drawings per drawing type by size (A/B/D/E) and the equivalent A-size quantity.
- **Other Deliverables** — Phase, Type, Deliverable Name, Cost (USD).
- **Cost Estimate Page** — Section 1: Drawings Development Cost (equivalent A-size drawings × hours per drawing).
