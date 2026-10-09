# ZubairHub Codebase Cleanup & Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sequentially resolve deployment blockers, invalid model names, broken Streamlit parameters, startup latency bottlenecks, resource leaks, and git hygiene issues in ZubairHub.

**Architecture:** 
1. Fix foundational runtime & dependency configs (UTF-8 `runtime.txt`, dependency list).
2. Fix model identifier string (`gemini-2.0-flash`) and deprecate invalid `width="stretch"` UI arguments.
3. Fix logic errors in `fuel_price.py` (URL join, date picker unpacking).
4. Refactor `app.py` and `computer_vision.py` to use lazy imports and deferred PyTorch initialization to drop startup latency from ~15s to <1s.
5. Add resource management (`try...finally` temp file unlinking, PDF handle closure).
6. Update `.gitignore` to ignore `venv_x86_64/` and scratch files, and link weather images.

**Tech Stack:** Python 3.12/3.13, Streamlit, Google GenAI SDK, PyTorch / HuggingFace Transformers, PyMuPDF, ReportLab.

**Spec:** Codebase Review Report (`codebase_review.md`).

## Global Constraints
- ARM64 Apple Silicon compliance on local commands (`arch -arm64`).
- Streamlit UI stability and backwards/forwards compatibility.
- Commit message format: `<ticket number> | <changes> (<feat/fix>)` (e.g. `ZH-101 | ... (fix)`).
- Preserve existing documentation and comments.
- No tests on `readme_test` pickslips unless explicitly requested.

---

### Task 1: Fix Deployment & Runtime Configurations

**Files:**
- Modify: `runtime.txt`
- Modify: `requirements.txt`
- Delete: `requirements.txt.new`

- [ ] **Step 1: Convert `runtime.txt` from UTF-16LE to plain UTF-8**
Ensure `runtime.txt` contains `python-3.13\n` encoded as standard UTF-8 without BOM.
- [ ] **Step 2: Add `reportlab` to `requirements.txt` and remove `requirements.txt.new`**
Add `reportlab>=4.0.0` so `generate_masked_pdf.py` runs without missing dependencies, and delete leftover `requirements.txt.new`.
- [ ] **Step 3: Verify encoding and dependencies**
Run `file runtime.txt` and confirm `ASCII text`.
- [ ] **Step 4: Commit**
`git add runtime.txt requirements.txt && git rm requirements.txt.new`
Commit: `ZH-101 | fix runtime encoding and add missing dependencies (fix)`

---

### Task 2: Correct AI Model Name & Safe Client Initialization

**Files:**
- Modify: `modules/utils/generative_ai.py`
- Modify: `app.py`

- [ ] **Step 1: Update model identifier in `generative_ai.py`**
Replace `"gemini-3.5-flash"` with `"gemini-2.0-flash"` in `DEFAULT_MODEL` and quota mappings.
- [ ] **Step 2: Update model selection in `app.py`**
Replace `"gemini-3.5-flash"` with `"gemini-2.0-flash"` in `MODELS` dict and default fallback.
- [ ] **Step 3: Safe client initialization**
In `generative_ai.py`, wrap `google.genai.Client` so an empty/missing API key displays a clean warning in Streamlit rather than throwing an unhandled exception at import time.
- [ ] **Step 4: Verify syntax & import**
Run: `arch -arm64 .venv/bin/python -c "from modules.utils.generative_ai import DEFAULT_MODEL; assert DEFAULT_MODEL == 'gemini-2.0-flash'"`
- [ ] **Step 5: Commit**
Commit: `ZH-102 | update default gemini model to 2.0-flash and safe-guard client init (fix)`

---

### Task 3: Replace Invalid `width="stretch"` Streamlit Parameters

**Files:**
- Modify: `modules/computer_vision.py`
- Modify: `modules/natural_language.py`
- Modify: `modules/artificial_intelligence.py`
- Modify: `modules/bank_parser.py`
- Modify: `modules/weather_forecast.py`
- Modify: `modules/fuel_price.py`

- [ ] **Step 1: Replace `width="stretch"` with `use_container_width=True`**
Update all instances across:
  - `modules/computer_vision.py`
  - `modules/natural_language.py`
  - `modules/artificial_intelligence.py`
  - `modules/bank_parser.py`
  - `modules/weather_forecast.py`
  - `modules/fuel_price.py`
- [ ] **Step 2: Verify no `width="stretch"` remaining**
Run: `grep -rn 'width=["\x27]stretch["\x27]' modules/`
Expected: 0 matches.
- [ ] **Step 3: Commit**
Commit: `ZH-103 | replace invalid width stretch parameter with use_container_width (fix)`

---

### Task 4: Fix Logic & Edge-Case Bugs in `fuel_price.py`

**Files:**
- Modify: `modules/fuel_price.py`

- [ ] **Step 1: Fix URL join**
Replace `os.path.join(BASE_URL, ENDPOINT)` with `f"{BASE_URL}/{ENDPOINT}"` or `urllib.parse.urljoin`.
- [ ] **Step 2: Fix Date Picker Range Unpacking**
Handle single-element tuple return during range selection:
```python
date_range = st.date_input("Select date range:", ...)
if not isinstance(date_range, (list, tuple)) or len(date_range) < 2:
    st.info("Please select both start and end dates.")
    return
start_date, end_date = date_range[0], date_range[1]
```
- [ ] **Step 3: Fix unbound variable in footer**
Ensure `{df['date'].max()}` is only rendered if `df` is defined and non-empty.
- [ ] **Step 4: Verify syntax**
Run: `arch -arm64 .venv/bin/python -m py_compile modules/fuel_price.py`
- [ ] **Step 5: Commit**
Commit: `ZH-104 | fix url joining and date input unpacking in fuel price module (fix)`

---

### Task 5: Implement Lazy Loading in `app.py` & `computer_vision.py`

**Files:**
- Modify: `app.py`
- Modify: `modules/computer_vision.py`

- [ ] **Step 1: Refactor `page_names_to_func` in `app.py` to store lazy function loaders**
Change `page_names_to_func = { '📌 Introduction': load_intro, ... }` so functions are NOT invoked on app startup.
- [ ] **Step 2: Lazy initialize DETR in `computer_vision.py`**
Move `detector = DetrObjectDetection()` into a cached function (`@st.cache_resource def get_detector(): ...`) so PyTorch and ResNet-50 are only loaded into memory when the user actually navigates to Object Detection.
- [ ] **Step 3: Verify fast startup**
Time import of `app.py`:
Run: `arch -arm64 .venv/bin/python -c "import time; t0 = time.time(); import app; print(f'Startup import time: {time.time()-t0:.2f}s')"`
Expected: < 1.5 seconds.
- [ ] **Step 4: Commit**
Commit: `ZH-105 | implement lazy loading in app and computer vision module (feat)`

---

### Task 6: Temporary File & Resource Cleanup

**Files:**
- Modify: `modules/computer_vision.py`
- Modify: `modules/natural_language.py`
- Modify: `modules/utils/document_parser.py`

- [ ] **Step 1: Wrap temporary file usage in `try...finally` in `computer_vision.py`**
Ensure temp files created with `NamedTemporaryFile` are removed with `os.unlink()`.
- [ ] **Step 2: Wrap temporary file usage in `try...finally` in `natural_language.py`**
Ensure uploaded files saved to temp disk are cleaned up when processing completes.
- [ ] **Step 3: Ensure PyMuPDF file handles are closed in `document_parser.py`**
Ensure `pdf_document.close()` is called in `PDFExtractor`.
- [ ] **Step 4: Commit**
Commit: `ZH-106 | add temp file cleanup and close document handles (fix)`

---

### Task 7: Workspace & Git Hygiene

**Files:**
- Modify: `.gitignore`
- Modify: `modules/weather_forecast.py`

- [ ] **Step 1: Update `.gitignore`**
Add `venv_x86_64/`, `Untitled.ipynb`, `prasarana_route.ipynb`, `*.xlsx.bak` to `.gitignore`.
- [ ] **Step 2: Connect weather forecast images**
In `modules/weather_forecast.py`, point image paths to the existing `images/` directory (`images/sunny.jpg`, `images/rainy.jpg`, etc.) rather than returning `None`.
- [ ] **Step 3: Clean untracked garbage**
Remove leftover temporary or unused files.
- [ ] **Step 4: Commit**
Commit: `ZH-107 | update gitignore for large assets and restore weather images (fix)`

