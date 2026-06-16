# 😎 ZubairHub

> **Azzubair's personal web app** — one place to try out data and AI tools in your browser.

Pick a tool from the menu on the left, use it, and see results instantly. No coding needed once it's running.

---

## 📖 Table of Contents

- [What is ZubairHub?](#-what-is-zubairhub)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [How to Use](#-how-to-use)
- [Optional: Sample Bank PDF](#-optional-sample-bank-pdf)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🎯 What is ZubairHub?

ZubairHub is a **demo and portfolio app** by [Azzubair Azeman](https://www.linkedin.com/in/azzubair-azeman-b96222142/). It bundles several small projects into one easy interface — like a **digital toolbox** 🧰 for learning, demos, and personal use.

**In one sentence:** open the app, choose a tool, upload a file or ask a question, and get tables, charts, or AI answers back.

> ⚠️ Built for exploration and demos — not as a production product.

---

## ✨ Features

### 📌 Introduction
A welcome page with background on the author, skills, and work experience.

### 👨‍👩‍👧‍👦 Family Graph
Draws your family as a connected diagram so relationships are easy to see at a glance.

### 📷 Object Detection
Upload a photo — the app finds and labels things in the image (e.g. people, cars, everyday objects).

### 📄 Document Parsing
Upload a document and pull out useful structured information automatically.

### 🔍 Text Extraction
Upload a photo or scan — the app reads the words off the image, like copying text from a screenshot.

### 🔮 Generative AI
Chat with **Google Gemini**. Ask questions with text, or include an image in your prompt.

### 🏦 Bank Statement Parser
Upload a bank statement (PDF or image), or try a built-in masked sample. AI reads the transactions and shows them as a **table and charts** 📊.

### 🌥️ Weather Forecast
Pick a location in Malaysia and view forecast data from [data.gov.my](https://data.gov.my).

### ⛽ Fuel Price
Browse historical Malaysian fuel prices over a date range you choose.

### 💼 Personal
Upload a SAP Excel export, clean and reshape dates/times, then download the result.

---

## 🚀 Quick Start

### 📋 Prerequisites

| Requirement | Why you need it |
|-------------|-----------------|
| 🐍 **Python 3.13+** | Runs the app |
| 🔑 **Gemini API key** | AI chat & bank statement parsing — [Google AI Studio](https://aistudio.google.com/) |
| 📝 **Tesseract OCR** | Text Extraction only — [install guide](https://github.com/tesseract-ocr/tesseract) |

### ⚙️ Install & Run

**1️⃣ Get the code**
```sh
git clone <your-repo-url>
cd zubairhub
```

**2️⃣ Install dependencies**
```sh
pip install -r requirements.txt
```

**3️⃣ Add your API key**

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_key_here
```

**4️⃣ Launch the app**
```sh
streamlit run app.py
```

**5️⃣ Open in browser** 🌐

The app should open automatically. Use the **Navigation** menu on the left to switch tools.

---

## 🖱️ How to Use

1. ▶️ **Run** the app (`streamlit run app.py`)
2. 📂 **Pick** a tool from the sidebar
3. 📤 **Follow** the prompts — upload a file, pick options, or type a question
4. ✅ **View** results in the main area (tables, charts, images, or AI replies)

> 💡 **Bank Statement Parser tip:** choose a Gemini model and check estimated daily API quota in the sidebar.

---

## 🏦 Optional: Sample Bank PDF

Regenerate the demo bank statement used by the Bank Statement Parser:

```sh
pip install reportlab
python generate_masked_pdf.py
```

Output: `modules/bank_data/bank_statement_example.pdf` — a fake, privacy-safe statement for testing.

---

## 🛠️ Tech Stack

Built with [Streamlit](https://streamlit.io/) for the UI.

| Category | Libraries |
|----------|-----------|
| 🤖 AI | `google-genai` |
| 👁️ Computer vision | `opencv-python`, `torch`, `transformers` |
| 📝 OCR | `pytesseract` |
| 📄 PDF | `pymupdf`, `streamlit-pdf-viewer` |
| 📊 Charts & graphs | `plotly`, `networkx`, `seaborn` |
| 📁 Spreadsheets | `pandas`, `openpyxl`, `xlsxwriter` |

See `requirements.txt` for the full list.

---

## 🤝 Contributing

Suggestions and pull requests are welcome! 🎉

Open an issue if something breaks or you have an idea for a new tool.

---

## 📬 Contact

**👤 Azzubair Azeman**

| | |
|---|---|
| 📧 Email | [azzubairazeman@gmail.com](mailto:azzubairazeman@gmail.com) |
| 💼 LinkedIn | [linkedin.com/in/azzubair-azeman-b96222142](https://www.linkedin.com/in/azzubair-azeman-b96222142/) |
| 🐙 GitHub | [github.com/azzubair01](https://github.com/azzubair01) |

---

<p align="center">Made with ❤️ by Azzubair Azeman</p>
