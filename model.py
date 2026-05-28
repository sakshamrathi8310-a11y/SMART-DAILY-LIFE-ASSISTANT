import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
import joblib

def train_and_save():

    df = pd.read_csv("C:\\projects\\Smart Daily Life Assistant\\data.csv")

    # Feature Engineering
    df['sleep_eff'] = df['sleep'] / 8
    df['activity'] = df['steps'] / 10000

    X = df[['sleep','screen_time','steps','work_hours','mood','food','sleep_eff','activity']]

    y_stress = df['stress']
    y_prod = df['productivity']
    y_health = df['health']

    pipeline_cls = Pipeline([
        ("imputer", SimpleImputer()),
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier())
    ])

    pipeline_reg1 = Pipeline([
        ("imputer", SimpleImputer()),
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor())
    ])

    pipeline_reg2 = Pipeline([
        ("imputer", SimpleImputer()),
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor())
    ])

    pipeline_cls.fit(X, y_stress)
    pipeline_reg1.fit(X, y_prod)
    pipeline_reg2.fit(X, y_health)

    joblib.dump(pipeline_cls, "stress.pkl")
    joblib.dump(pipeline_reg1, "prod.pkl")
    joblib.dump(pipeline_reg2, "health.pkl")

def load_models():
    return (
        joblib.load("stress.pkl"),
        joblib.load("prod.pkl"),
        joblib.load("health.pkl")
    )