# Agricultural Yield Prediction System

An end-to-end machine learning pipeline that predicts crop yield (kg/hectare) from soil, seed, fertilizer, weather and irrigation inputs, served through a Flask web app.

**Live Demo:** [https://agriculture-yield-prediction-bllv.onrender.com](https://agriculture-yield-prediction-bllv.onrender.com)
> Hosted on a free tier, so the first load after inactivity may take 30-60 seconds.

---

## Business Problem

Farmers need to decide how much fertilizer and irrigation to plan for before the season starts. This project estimates expected yield from those inputs so resource allocation and crop planning can be based on data rather than guesswork.

## Dataset

| Item | Detail |
| :--- | :--- |
| Records | 16,000 |
| Target | `Yield_kg_per_hectare` (range 57.5 to 1,385.1, mean about 714) |
| Features | 6 (listed below) |

**Features and valid input ranges**

The web app only accepts values inside the range of the training data, because predictions outside it would be extrapolation and unreliable.

| Feature | Type | Training range | Accepted in app |
| :--- | :--- | :--- | :--- |
| `Soil_Quality` | float | 50.0 to 100.0 | 50 to 100 |
| `Seed_Variety` | categorical (0/1) | 0 or 1 | 0 or 1 |
| `Fertilizer_Amount_kg_per_hectare` | float | 50.0 to 300.0 | 50 to 300 |
| `Sunny_Days` | float | 51.5 to 142.4 | 50 to 150 |
| `Rainfall_mm` | float | 110.0 to 872.3 | 100 to 900 |
| `Irrigation_Schedule` | integer | 0 to 15 | 0 to 15 (whole number) |

## Model Performance

7 regression models were compared using GridSearchCV tuning, and the best was selected by R² on held-out data.

| Metric | Value |
| :--- | :--- |
| Best model | Linear Regression |
| R² (test set) | 0.9387 |

**Models tested:** Linear Regression, KNN, Decision Tree, Random Forest, AdaBoost, XGBoost, CatBoost.

| Model | R² (test) |
| :--- | :--- |
| Linear Regression | 0.9387 |

Note: a simple linear model performed best, which suggests the relationship between these inputs and yield is close to linear. 

## Key Features

- **Modular pipeline:** separate ingestion, transformation, training and prediction components
- **Preprocessing:** missing-value imputation, feature scaling and categorical encoding
- **Multi-model comparison** with GridSearchCV hyperparameter tuning
- **Flask web app** for single-record predictions, deployed on Render with gunicorn
- **Input validation** on both the form (min/max, dropdown) and the server, so out-of-range values never reach the model
- **Logging and exception handling** across all pipeline stages
- **Health check endpoint** at `/health`

## Tech Stack

| Area | Tools |
| :--- | :--- |
| Language | Python, HTML |
| ML | Scikit-learn, XGBoost, CatBoost |
| Data | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Web | Flask, Bootstrap, gunicorn |
| Persistence | Dill / Pickle |
| Hosting | Render |

## Pipeline

1. **Data ingestion:** loads raw data and splits it into train and test sets
2. **Data transformation:** imputes missing values, scales numeric features, encodes categorical features. The preprocessor is fit on training data only, to avoid leakage
3. **Model training:** trains and tunes 7 algorithms with GridSearchCV
4. **Model evaluation:** selects the best model by R² on the test set
5. **Prediction:** the saved preprocessor and model are loaded to score new inputs from the web form

## Project Structure

```text
.
├── app.py                          # Flask app, routes and input validation
├── requirements.txt                # Pinned dependencies
├── artifacts/
│   ├── model.pkl                   # Trained model
│   └── preprocessor.pkl            # Fitted preprocessing pipeline
├── src/
│   ├── components/
│   │   ├── data_ingestion.py       # Data loading and train/test split
│   │   ├── data_transformation.py  # Feature engineering pipeline
│   │   └── model_trainer.py        # Model training and selection
│   ├── pipeline/
│   │   └── predict_pipeline.py     # Prediction pipeline for new data
│   ├── exception.py                # Custom exception handling
│   ├── logger.py                   # Logging configuration
│   └── utils.py                    # Save/load helpers
└── templates/
    ├── index.html
    └── home.html                   # Prediction form
```

## Getting Started

### Prerequisites

- Python 3.11 recommended (match the version used to train the model)
- pip

### Installation

```bash
git clone https://github.com/Shrinathrajeshirke/Agriculture-Yield-Prediction

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Run the app

```bash
python app.py
```

Open http://localhost:8080 and go to `/predictdata` to use the prediction form.

### Retrain the model (optional)

```bash
python src/components/data_ingestion.py
```

This regenerates `artifacts/model.pkl` and `artifacts/preprocessor.pkl`.

## Important: Version Pinning

The saved model and preprocessor are pickle files, which depend on the library versions that created them. Loading them with different versions can fail (for example with `'SimpleImputer' object has no attribute '_fill_dtype'`).

This project is trained and served with:

```text
scikit-learn==1.5.1
numpy==1.26.4
pandas==2.2.2
```

If you change these versions, retrain the model and commit the new `artifacts/` files.

## Deployment (Render)

1. Push the repo to GitHub, including the `artifacts/` folder
2. On [render.com](https://render.com), create a **Web Service** from the repo
3. Settings:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Environment variable:** `PYTHON_VERSION` set to a version compatible with the pinned libraries (for example `3.11.9`)
4. Deploy, then test a prediction at `/predictdata`

## Limitations and Future Work

- Predictions are only reliable inside the training ranges listed above
- The model uses 6 inputs and does not account for crop type, soil chemistry or regional effects
- Planned: cross-validation, RMSE/MAE reporting, feature-importance and residual plots, and a Docker image

## Author

**Shrinath Rajeshirke**
- GitHub: [@Shrinathrajeshirke](https://github.com/Shrinathrajeshirke)
- LinkedIn: [shrinathrajeshirke](https://www.linkedin.com/in/shrinathrajeshirke/)

## License

MIT License