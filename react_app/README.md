# Resume AI React

This is a new React implementation of the resume matcher interface. The original Streamlit app remains unchanged.

## Setup

From the project root:

```bash
cd react_app
npm install
../.venv/bin/pip install -r requirements.txt
```

## Run

Start the API:

```bash
cd react_app
npm run api
```

Start the React app in a second terminal:

```bash
cd react_app
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

The API reuses the existing Python modules for extraction, preprocessing, scoring, and LLM feedback. Your root `.env` is still used for provider keys.
