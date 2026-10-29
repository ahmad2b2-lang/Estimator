# Estimator

Engineering project hub — a single-file HTML web app (no database, no build step). Data is stored in the browser (localStorage); use the front page's **Backup everything (JSON)** to keep a copy.

Open `index.html` in any browser, or enable GitHub Pages for this repo to use it online.

## Modules
- **Equipment Types Module** — define each equipment type once (Discipline, Name, optional Variant) with the drawings needed per one unit, per drawing type. Also manages the drawing types (abbreviation, full name, drawing size).
- **Drawings Register Module** — pick Plant (H4, H1, M1, W1), equipment and quantity; drawings required per drawing type are calculated automatically.
- **Drawing Quantities Module** — quantity of drawings per drawing type by size (A/B/D/E) and the equivalent A-size quantity.
- **Other Deliverables** — Phase, Type, Deliverable Name, Cost (USD).
- **Cost Estimate Page** — Section 1: Drawings Development Cost (equivalent A-size drawings × hours per drawing).
