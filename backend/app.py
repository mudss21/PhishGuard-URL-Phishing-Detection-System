from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import joblib
import pandas as pd
import numpy as np
import gdown

from feature_extractor import extract_features
from blacklist_checker import is_blacklisted
from whitelist_checker import is_whitelisted



# FASTAPI APP


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# MODEL DOWNLOAD


MODEL_PATH = "hybrid_model.pkl"


def download_model():

    file_url = (
        "https://drive.google.com/uc?id=1uHuDQzVFJJ0dflSofGVsvripp2IwHCT0"
    )

    print("Downloading model...")

    gdown.download(
        file_url,
        MODEL_PATH,
        quiet=False
    )

    print("Model downloaded")


if not os.path.exists(MODEL_PATH):
    download_model()


print("Loading model...")
model = joblib.load(MODEL_PATH)
print("Model loaded")



# TRAINING FEATURE ORDER


FEATURE_COLUMNS = [
    "url_length",
    "average_subdomain_length",
    "entropy_of_url",
    "entropy_of_domain",
    "domain_length",
    "number_of_subdomains",
    "number_of_special_char_in_url",
    "number_of_digits_in_url",
    "number_of_digits_in_domain",
    "number_of_dots_in_domain",
    "number_of_slash_in_url",
    "number_of_dots_in_url",
    "path_length",
    "number_of_hyphens_in_domain",
    "number_of_hyphens_in_url",
    "having_digits_in_domain",
    "number_of_equal_in_url",
    "number_of_digits_in_subdomain",
    "having_repeated_digits_in_domain",
    "number_of_questionmark_in_url"
]



# FEATURE ENGINEERING


def engineer_features(X: pd.DataFrame) -> pd.DataFrame:

    X = X.copy()

    cols = X.columns.tolist()

    # Ratio features
    for i in range(min(5, len(cols))):
        for j in range(i + 1, min(6, len(cols))):

            c1 = cols[i]
            c2 = cols[j]

            denom = X[c2].replace(0, np.nan)

            X[f"ratio_{c1}_{c2}"] = (
                X[c1] / denom
            ).fillna(0)

    # Row-level statistics
    X["row_mean"] = X[cols].mean(axis=1)

    X["row_std"] = (
        X[cols]
        .std(axis=1)
        .fillna(0)
    )

    X["row_max"] = X[cols].max(axis=1)

    X["row_min"] = X[cols].min(axis=1)

    X["row_range"] = (
        X["row_max"] -
        X["row_min"]
    )

    return X



# REQUEST MODEL

class URLRequest(BaseModel):
    url: str



# PREDICTION LOGIC

def predict_url(url):

    try:


        # BLACKLIST CHECK

        if is_blacklisted(url):

            return {
                "prediction": "Phishing",
                "source": "Blacklist",
                "probability": 1.0
            }


        # WHITELIST CHECK

        if is_whitelisted(url):

            return {
                "prediction": "Legitimate",
                "source": "Whitelist",
                "probability": 1.0
            }


        # FEATURE EXTRACTION

        features = extract_features(url)

        df = pd.DataFrame([features])

        # Ensure original feature order
        df = df.reindex(
            columns=FEATURE_COLUMNS,
            fill_value=0
        )

      
        # FEATURE ENGINEERING
       
        df = engineer_features(df)

        print("Prediction feature count:", df.shape[1])

   
        # MODEL PREDICTION

        probability = float(
            model.predict_proba(df)[0][1]
        )

        if probability >= 0.5:

            return {
                "prediction": "Phishing",
                "source": "ML Model",
                "probability": round(probability, 4)
            }

        return {
            "prediction": "Legitimate",
            "source": "ML Model",
            "probability": round(
                1 - probability,
                4
            )
        }

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



# ROUTES

@app.get("/")
def home():

    return {
        "message": "PhishGuard API Running 🚀"
    }


@app.post("/predict")
def predict(request: URLRequest):

    return predict_url(request.url)