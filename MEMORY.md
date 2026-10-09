# Project Memory & Handoffs

## Overview
- **Repository:** zubairhub
- **Initialized:** 2026-10-09

## Active Tickets & Workflows
- **Completed Review & Refactoring Sprint:**
  - `ZH-101` (`90a84ec`): Fixed `runtime.txt` encoding (converted from UTF-16LE with BOM to UTF-8 `python-3.13`), added `reportlab>=4.0.0` dependency to `requirements.txt`.
  - `ZH-102` (`918ae11`): Updated Gemini model from non-existent `gemini-3.5-flash` to `gemini-2.0-flash`, added safe-guard to `Client` initialization when `GEMINI_API_KEY` is absent.
  - `ZH-103` (`16f9e9d`): Replaced invalid `width="stretch"` Streamlit parameter with `use_container_width=True` across 6 modules.
  - `ZH-104` (`f0a51c4`): Fixed URL construction (`os.path.join` replaced with `/`), 1-element tuple unpacking crash on date picker, and footer `df` `UnboundLocalError` in `modules/fuel_price.py`.
  - `ZH-105` (`fb8b0ca`): Implemented lazy page rendering in `app.py` and `@st.cache_resource` for `DetrObjectDetection` in `modules/computer_vision.py` (slashing app startup import time from ~15s to 1.41s).
  - `ZH-106` (`0d018b3`): Implemented `try...finally` temporary file cleanup (`os.unlink`) in `computer_vision.py` and `natural_language.py`; added context manager protocol (`__enter__`, `__exit__`) and handle resetting to `PDFExtractor` in `modules/utils/document_parser.py`.
  - `ZH-107` (`ed2227d`): Updated `.gitignore` to exclude `venv_x86_64/`, `Untitled.ipynb`, `prasarana_route.ipynb`, `*.xlsx.bak`; restored weather forecast image handling and tracked lightweight image assets in `images/`.
  - `ZH-110` (`fb41474`): Added historical events overlay with vertical dashed badges on Plotly chart, category filtering, and interactive timeline expander in `modules/fuel_price.py` powered by `modules/fuel_price_data/events.json`.
  - `ZH-112` (`026826d`): Fixed event markers rendering using native Plotly shapes and annotations anchored to `paper`, staggered overlapping badges with `yshift`, widened default date range to full dataset history, resolved path via `__file__`, and added empty state feedback.
  - `ZH-113`: Migrated deprecated `use_container_width=True` to modern `width='stretch'` across all Streamlit UI components (`st.image`, `st.dataframe`, `st.plotly_chart`, `st.data_editor`, `st.download_button`).

## Architectural Decisions & Notes
- Added `justfile` with ARM64-compliant commands (`setup`, `setup-uv`, `run`) adhering to Apple Silicon conventions.
- Updated global instructions in `~/.gemini/GEMINI.md` to include Skill-First Superpowers activation and Selective Subagent Delegation/Management rules.
- Streamlit Page Routing: Use lazy callback mapping `{"Name": lambda: import_and_render()}` in `app.py` to prevent eager imports of heavy ML/torch/vision packages during initial app boot.
- Document & Image Parsing: Always use context managers or `try...finally` with explicit `os.unlink()` for temp files created via `NamedTemporaryFile(delete=False)`.
- Fuel Price Analytics: Event annotations in Plotly use native `fig.add_shape(type='line', x0=ev['date'], x1=ev['date'], yref='paper')` and `fig.add_annotation(x=ev['date'], y=1, yref='paper', yanchor='bottom', yshift=...)` with ISO string dates (`YYYY-MM-DD`) rather than `fig.add_vline` with numeric timestamps, guaranteeing rock-solid cross-platform rendering on Plotly datetime axes.
- Streamlit Layout Parameters: Migrated all instances of deprecated `use_container_width=True` to modern `width='stretch'` across all UI elements (`st.image`, `st.dataframe`, `st.plotly_chart`, `st.data_editor`, `st.download_button`).


## Deployment Status
- Remote `origin/main` is fully up to date with local `main` (synced at commit `fb41474`).
- GitHub authentication verified via Personal Access Token (PAT).
- Working tree is clean.
