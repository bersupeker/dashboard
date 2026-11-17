# Arçelik AI use case 07: dealer potential, fair targets & incentive design

This is a descriptive dashboard. It compares each dealer's sales target with the potential of its catchment area and flags targets that are far above or below what the area suggests. There is no forecasting, ML or optimisation: only documented formulas and rule-based thresholds. **All data is dummy.**

## Open the dashboard
Double-click **`dashboard/index.html`**. It is one self-contained file: all data, JS, CSS and charts (hand-written SVG) are inline. It needs no internet connection and no server, and works in any recent Chrome, Edge, Safari or Firefox.

## Regenerate everything
Needs Python 3.9+ with `pandas` and `numpy`.

```bash
python scripts/generate_data.py     # writes data/districts.csv, dealers.csv, monthly_sales.csv (seed 20241101)
python scripts/build_dashboard.py   # prints sanity checks/assertions, writes dashboard/index.html
python scripts/test_dashboard.py    # optional: headless browser test + docs/screenshots/*.png
                                    #   (needs `pip install playwright`; uses installed Chrome,
                                    #    or run `playwright install chromium`)
```

`build_dashboard.py` stops with an error if a check fails. It checks row counts, nulls in key columns, flag shares (10–20%), potential index range, Σ fair target = Σ target per region, and the EMPEROR rule.

## Folder structure
```
data/        districts.csv, dealers.csv, monthly_sales.csv, data_dictionary.md
scripts/     generate_data.py, build_dashboard.py, dashboard_template.html (dashboard source), test_dashboard.py
dashboard/   index.html (built output; do not edit, edit the template instead)
docs/        one_page_note.md/.pdf, demo_script.md, screenshots/
```

## Configuration
- **Flag thresholds and potential-index weights**: the `RULES` and `WEIGHTS` constants at the top of the `<script>` in `scripts/dashboard_template.html`. Rebuild after editing. The Python checks in `build_dashboard.py` use the same values (`RULES`, `W`).
- **Default period**: `DEFAULT_PERIOD` (last 12 months, so that KPIs can be compared with the previous 12 months).

## Run with Streamlit
`streamlit_app.py` embeds `dashboard/index.html` full-width and adds CSV/PDF downloads in the sidebar.

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Deploy to Streamlit Community Cloud:** push this folder to GitHub with `streamlit_app.py` at the repo root. Then go to share.streamlit.io → *Create app* → pick the repo, branch `main` and main file `streamlit_app.py` → *Deploy*. The built `dashboard/index.html` must be committed, because the cloud app does not rebuild it.
