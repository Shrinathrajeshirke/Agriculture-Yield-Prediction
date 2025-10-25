#  Agricultural Yield Prediction System

##  Business Problem
Developed an end-to-end machine learning pipeline to predict agricultural crop yields based on environmental and farming factors. This system helps farmers optimize resource allocation and make data-driven decisions for better crop planning.

##  Key Features
- **Automated ETL Pipeline**: Processes and transforms agricultural data from multiple sources
- **Multi-Model Comparison**: Tests 7 different ML algorithms to find optimal performance
- **Hyperparameter Optimization**: GridSearchCV for automatic model tuning
- **Production Deployment**: Flask web application for real-time predictions
- **Robust Error Handling**: Comprehensive logging and exception management
- **Modular Architecture**: Clean, maintainable code structure

##  Technologies Used
- **Programming**: Python, HTML
- **ML Libraries**: Scikit-learn, XGBoost, CatBoost
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Web Framework**: Flask
- **Model Persistence**: Dill/Pickle

##  Model Performance
- **Best Algorithm**: Linear Regression
- **R² Score**: 0.9387
- **Models Tested**: Linear Regression, KNN, Decision Tree, Random Forest, XGBoost, CatBoost, AdaBoost

##  Project Architecture

### Data Pipeline
1. **Data Ingestion**: Loads raw agricultural data and splits into train/test sets
2. **Data Transformation**: Handles missing values, feature scaling, and categorical encoding  
3. **Model Training**: Compares multiple algorithms with hyperparameter tuning
4. **Model Evaluation**: Selects best performing model based on R² score
5. **Deployment**: Flask web app for real-time yield predictions

### Key Components
- `src/components/data_ingestion.py` - Data loading and splitting
- `src/components/data_transformation.py` - Feature engineering pipeline
- `src/components/model_trainer.py` - ML model training and selection
- `src/pipeline/predict_pipeline.py` - Prediction pipeline for new data
- `app.py` - Flask web application

##  Getting Started

### Prerequisites
```bash
Python 3.8+
pip package manager
