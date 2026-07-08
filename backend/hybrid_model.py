import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    StackingClassifier,
    ExtraTreesClassifier,
)
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_selection import SelectFromModel




# 1. LOAD DATASET

df = pd.read_csv("/content/Dataset_useful_top20.csv")

target_col = "Type"
df[target_col] = df[target_col].astype("category").cat.codes

X = df.drop(columns=[target_col])
y = df[target_col]

print(f"Dataset shape: {X.shape}")
print(f"Class distribution:\n{y.value_counts()}\n")

# 2. FEATURE ENGINEERING

def engineer_features(X: pd.DataFrame) -> pd.DataFrame:
    """Add interaction ratios and statistical aggregates."""
    X = X.copy()
    cols = X.columns.tolist()

    # Ratio features between all column pairs (top 5 pairs by index)
    for i in range(min(5, len(cols))):
        for j in range(i + 1, min(6, len(cols))):
            c1, c2 = cols[i], cols[j]
            denom = X[c2].replace(0, np.nan)
            X[f"ratio_{c1}_{c2}"] = (X[c1] / denom).fillna(0)

    # Row-level statistics
    X["row_mean"]   = X[cols].mean(axis=1)
    X["row_std"]    = X[cols].std(axis=1).fillna(0)
    X["row_max"]    = X[cols].max(axis=1)
    X["row_min"]    = X[cols].min(axis=1)
    X["row_range"]  = X["row_max"] - X["row_min"]

    return X

X_eng = engineer_features(X)
print(f"Feature count after engineering: {X_eng.shape[1]}")


# 3. TRAIN-TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X_eng, y, test_size=0.2, stratify=y, random_state=42
)


# 4. HANDLE CLASS IMBALANCE WITH SMOTE 

if HAS_SMOTE:
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)
    print(f"After SMOTE — train shape: {X_train.shape}")




# 5. BASE ESTIMATORS (each wrapped in a Pipeline)


# --- Random Forest ---
rf = Pipeline([
    ("imp",  SimpleImputer(strategy="median")),
    ("rf",   RandomForestClassifier(
        n_estimators=500,
        max_depth=20,
        min_samples_split=3,
        min_samples_leaf=1,
        max_features="sqrt",
        bootstrap=True,
        oob_score=True,
        random_state=42,
        n_jobs=-1,
    ))
])

# --- Extra Trees ---
et = Pipeline([
    ("imp", SimpleImputer(strategy="median")),
    ("et",  ExtraTreesClassifier(
        n_estimators=500,
        max_depth=20,
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    ))
])

# --- Gradient Boosting ---
gb = Pipeline([
    ("imp", SimpleImputer(strategy="median")),
    ("gb",  GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        random_state=42,
    ))
])

# --- XGBoost ---

xgb = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("xgb", XGBClassifier(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            use_label_encoder=False,
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
            tree_method="hist",   # fast on CPU
        ))
    ])

# --- LightGBM  ---

lgb = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("lgb", LGBMClassifier(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=6,
            num_leaves=63,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbose=-1,
        ))
    ])

# --- ANN ---
mlp = Pipeline([
    ("imp",    SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("mlp",    MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        activation="relu",
        solver="adam",
        alpha=0.0003,
        learning_rate="adaptive",
        max_iter=600,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=15,
        random_state=42,
    ))
])

# --- KNN ---
knn_base = Pipeline([
    ("imp",    SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("knn",    KNeighborsClassifier(
        n_neighbors=5,
        weights="distance",
        metric="minkowski",
    ))
])
knn = CalibratedClassifierCV(knn_base, cv=5, method="isotonic")


# 6. BUILD ESTIMATOR LIST DYNAMICALLY

estimators = [
    ("rf",  rf),
    ("et",  et),
    ("gb",  gb),
    ("mlp", mlp),
    ("knn", knn),
    ("xgb", xgb),
    ("lgb", lgb)
]


# 7. STACKING CLASSIFIER (meta-learner = Logistic Regression)
#    Uses out-of-fold predictions → reduces overfitting

meta_learner = LogisticRegression(
    C=1.0,
    max_iter=1000,
    solver="lbfgs",
    multi_class="auto",
    random_state=42,
)

stacking_model = StackingClassifier(
    estimators=estimators,
    final_estimator=meta_learner,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    stack_method="predict_proba",
    passthrough=True,   # also pass raw features to meta-learner
    n_jobs=-1,
)


# 8. TRAIN

print("Training Stacking Ensemble...")
stacking_model.fit(X_train, y_train)


# 9. EVALUATION

y_pred  = stacking_model.predict(X_test)
acc     = accuracy_score(y_test, y_pred)

print(f"\n{'='*50}")
print(f"  STACKING ENSEMBLE ACCURACY : {acc * 100:.2f}%")
print(f"{'='*50}\n")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Cross-validation sanity check
cv_scores = cross_val_score(
    stacking_model, X_eng, y,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring="accuracy",
    n_jobs=-1,
)
print(f"5-Fold CV Accuracy: {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")


# 10. SAVE TRAINED MODEL


import joblib

MODEL_NAME = "hybrid_model.pkl"

joblib.dump(
    stacking_model,
    MODEL_NAME,
    compress=3
)

print(f"\nModel saved successfully: {MODEL_NAME}")





# 11. PREDICTION FUNCTION

def predict_sample(raw_sample: list) -> tuple[str, float]:
    """
    raw_sample : list of original feature values (before engineering).
    Returns    : (label_string, phishing_probability)
    """
    sample_df  = pd.DataFrame([raw_sample], columns=X.columns)
    sample_eng = engineer_features(sample_df)

    proba = stacking_model.predict_proba(sample_eng)[0]
    phishing_prob = proba[1]                       # probability of class 1

    label = "Phishing" if phishing_prob >= 0.5 else "Legitimate"
    return label, phishing_prob


