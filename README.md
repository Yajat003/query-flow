# Data Analyst Agent

An AI-powered data analysis application built using the **Agno Agent Framework** and **Streamlit**. This agent allows the users to upload local datasets (CSV/Excel) and query them using pure natural language. Behind the scenes, it translates user intents into highly optimized SQL queries executed locally via **DuckDB**, making complex data exploration accessible without needing SQL expertise.

### Key Features

* **Free-Tier LLM Support** 
* **In-Memory SQL Engine (DuckDB)** 
* **Data Preprocessing Pipeline:** Automatically handles missing values (`NA`, `N/A`, `missing`), performs regex cleaning for strings, and automatically parses numeric/date types.

---

## Project Structure

```text
query-flow/
│
├── services/
│   ├── __init__.py      
│   ├── data_service.py  # 1: Data ingestion, cleaning, and DuckDB setup
│   └── agent.py         # 2: LLM orchestration and native tool guardrails
│
├── app.py               # 3: UI Layout & Streamlit state orchestration
├── requirements.txt     
└── README.md            
```

---

## Tech Stack

* **UI Framework:** Streamlit
* **AI Agent Core:** Agno (formerly Phidata)
* **LLM Backends:** Google AI Studio (Gemini 2.0 Flash) / Groq API (Llama 3.3 70B)
* **OLAP Database:** DuckDB
* **Data Manipulation:** Pandas & OpenPyXL (Excel engine)

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Yajat003/query-flow.git](https://github.com/Yajat003/query-flow.git)
cd query-flow
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run

Execute the application using the Streamlit CLI:

```bash
streamlit run app.py
```

1. Open your browser to the local URL provided by the terminal (typically `http://localhost:8501`).
2. Navigate to the sidebar and select the preferred model provider (**Google Gemini** or **Groq**), and enter your respective API key.
3. Upload any valid `.csv` or `.xlsx` file.
4. Start chatting with the data (e.g., *"Show me the average revenue grouped by region"* or *"Find the top 5 rows where the status is missing"*).
