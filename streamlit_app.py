"""
Streamlit wrapper for the Use case 07 dashboard.

The dashboard itself is the self-contained file dashboard/index.html
(data, JS, CSS and charts inline). This app simply embeds it, and offers the
CSV data and the one-page note as downloads.

Local run:  streamlit run streamlit_app.py
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
HTML = ROOT / "dashboard" / "index.html"

st.set_page_config(page_title="Arçelik · Dealer Potential & Fair Targets", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

# Use the full browser width and remove Streamlit's default page padding
st.markdown("""
<style>
  .block-container {padding: 0.5rem 0.75rem 0 0.75rem; max-width: 100%;}
  header[data-testid="stHeader"] {height: 0; visibility: hidden;}
  footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def find_dashboard():
    """Find the dashboard HTML wherever it was uploaded in the repo."""
    if HTML.exists():
        return HTML
    roots = {ROOT, Path.cwd()}
    found = []
    for r in roots:
        for p in r.rglob("*"):
            if p.is_file() and p.suffix.lower() in (".html", ".htm") and ".git" not in p.parts \
                    and p.name.lower() != "dashboard_template.html":
                found.append(p)
    # prefer index.html in a folder called dashboard, then any index.html, then any html
    found.sort(key=lambda p: (p.name.lower() != "index.html", p.parent.name.lower() != "dashboard"))
    return found[0] if found else None


html_path = find_dashboard()
if html_path is None:
    st.error("Dashboard HTML not found in the repository. Upload the `dashboard` folder "
             "(containing `index.html`) next to `streamlit_app.py`.")
    files = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
                   if p.is_file() and ".git" not in p.parts)
    st.write(f"App folder: `{ROOT}`. Files the app can see:")
    st.code("\n".join(files) or "(none)")
    st.stop()

components.html(html_path.read_text(encoding="utf-8"), height=1000, scrolling=True)

with st.sidebar:
    st.header("Downloads")
    for f in ["dealers.csv", "districts.csv", "monthly_sales.csv"]:
        p = ROOT / "data" / f
        if p.exists():
            st.download_button(f, p.read_bytes(), file_name=f, mime="text/csv", use_container_width=True)
    note = ROOT / "docs" / "one_page_note.pdf"
    if note.exists():
        st.download_button("one_page_note.pdf", note.read_bytes(), file_name=note.name,
                           mime="application/pdf", use_container_width=True)
    st.caption("Dummy data for a course assignment. Descriptive analysis only.")
