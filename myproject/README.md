# Email and Message Spam Detector

A small web application that classifies an email or message as **spam** or **not spam (ham)**. It serves a browser-based form, uses a pre-trained scikit-learn model for predictions, and stores each prediction in a SQLite database.

## Features

- Web form for submitting a message.
- FastAPI endpoints for predictions and prediction history.
- Saved model loaded from `spam_model.pkl` at application startup.
- SQLite persistence for submitted messages, labels, and timestamps.
- Jupyter notebook (`spam.ipynb`) containing the model-training workflow.

## Project layout

```text
myproject/
├── app.py                 # FastAPI application and API endpoints
├── databse.py             # SQLite connection and prediction-history functions
├── spam_model.pkl         # Pre-trained scikit-learn model
├── spam.ipynb             # Model-training notebook
└── template/
    └── page.html          # Browser interface
```

## Requirements

- Python 3.9 or later.
- `fastapi`
- `uvicorn`
- `joblib`
- `scikit-learn`
- For running the training notebook: `jupyter` and `pandas`.

The model is serialized in `spam_model.pkl`. Use a scikit-learn version compatible with the one used to create that file; scikit-learn does not guarantee that serialized models work across arbitrary versions.

## Installation

Open a terminal in the project directory and create/activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the packages needed to run the web application:

```powershell
python -m pip install fastapi uvicorn joblib scikit-learn
```

To open and run the training notebook as well:

```powershell
python -m pip install jupyter pandas
python -m jupyter notebook
```

There is currently no dependency lockfile or `requirements.txt`; the commands above list the runtime and optional notebook packages.

## Run the application

From the project directory, start the development server:

```powershell
python -m uvicorn app:app --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser. Interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

The model file and HTML page are loaded relative to `app.py`, so keep `spam_model.pkl` and `template/page.html` in the locations shown in the project layout.

## API

### `POST /predict`

Submit a JSON object with a non-empty `message`:

```json
{
  "message": "Congratulations, you have won a prize!"
}
```

Example response:

```json
{
  "prediction": "spam"
}
```

The `prediction` value is either `"spam"` or `"ham"`. An empty or whitespace-only message returns HTTP `400`.

### `GET /history`

Returns saved predictions, newest first. Each record includes `id`, `message`, `prediction`, and `created_at`.

## Training the model

The notebook trains a TF-IDF and Multinomial Naive Bayes pipeline using columns named `Category` and `Message`, with categories `spam` and `ham`. It reports classification metrics and is the workflow for building a replacement model file.

The notebook currently reads its CSV dataset from a machine-specific path (`C:\Users\HP\Downloads\archive (7)\spam.csv`). To train on another machine, update that path to the location of your dataset. The web application itself uses the existing `spam_model.pkl` and does not need the CSV to make predictions.

## Prediction history database

The database helper creates a `predictions` table automatically when the app starts. **The current implementation places `spm_history.db` in the parent directory of `C:\Users\HP\Downloads\archive (7)\spam.csv`** (the `Downloads` directory on that machine). For another environment, update `Base_dir` in `databse.py` to a writable location before running the application. The database and its history are not included in the repository.

## Notes

- The project uses the module name `databse.py` (spelled this way); keep that filename unless the import in `app.py` is updated too.
- This is a basic classifier and may misclassify messages. Do not treat its output as a guarantee or rely on it as the sole spam filter.
