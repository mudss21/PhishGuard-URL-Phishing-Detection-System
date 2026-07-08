# 🔒 URL Phishing Detection System

A Machine Learning-based web application that detects whether a URL is **Legitimate** or **Phishing** in real time. The application uses a hybrid machine learning model along with URL feature extraction and blacklist/whitelist verification to improve prediction accuracy.

---

## 🚀 Features

- Detects phishing URLs in real time
- Extracts over 20 URL-based security features
- Hybrid Machine Learning model for accurate predictions
- Blacklist verification using known phishing domains
- Whitelist verification using trusted domains (Tranco)
- REST API built with FastAPI
- Modern React frontend with responsive UI
- Confidence score displayed with each prediction

---

## 🛠 Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Axios

### Backend
- Python
- FastAPI
- Uvicorn

### Machine Learning
- Scikit-learn
- Pandas
- NumPy

---

## 📂 Project Structure

```
URL-Phishing-Detection/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app.py
│   ├── feature_extractor.py
│   ├── blacklist_checker.py
│   ├── whitelist_checker.py
│   ├── hybrid_model.py
│   ├── requirements.txt
│   └── ...
│
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/url-phishing-detection.git
cd url-phishing-detection
```

---

## Backend Setup

Navigate to the backend folder

```bash
cd backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the FastAPI server

```bash
uvicorn app:app --reload
```

The backend will start on

```
http://127.0.0.1:8000
```

---

## Frontend Setup

Open another terminal

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Start the development server

```bash
npm run dev
```

The frontend will start on

```
http://localhost:5173
```

---

## 📊 Machine Learning Workflow

1. User enters a URL.
2. URL features are extracted.
3. Blacklist and whitelist checks are performed.
4. Features are passed to the trained ML model.
5. The model predicts whether the URL is Legitimate or Phishing.
6. The frontend displays the prediction along with the confidence score.

---

## 📈 Features Used

Some important extracted features include:

- URL Length
- Domain Length
- Number of Dots
- Number of Digits
- Number of Subdomains
- Path Length
- URL Entropy
- Domain Entropy
- Number of Special Characters
- Number of Hyphens
- Number of Slashes
- Number of Question Marks
- Average Subdomain Length
- Equal Sign Count
- Repeated Digits
- Digit Ratio
- Special Character Ratio

---

## 📌 Future Improvements

- SSL Certificate Verification
- WHOIS Lookup
- DNS Analysis
- Google Safe Browsing API Integration
- VirusTotal API Integration
- Browser Extension
- Explainable AI using SHAP
- Deep Learning Models

---

## 📜 License

This project is intended for educational and research purposes.

---

## 👨‍💻 Author

**Md Mudassir**

B.Tech Computer Engineering  
Zakir Husain College of Engineering & Technology  
Aligarh Muslim University

LinkedIn: https://linkedin.com/in/mudss21

Email: mudss.works@gmail.com