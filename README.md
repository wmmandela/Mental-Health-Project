# MindPulse: Machine Learning Mental Health Assessment & Risk Predictor

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-black.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/Frontend-React%20v18-61DAFB.svg)](https://reactjs.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**MindPulse** is a machine learning–powered mental health risk screening application designed to help individuals and workplace wellness coordinators assess mental well-being and identify individuals who may benefit from professional mental health support.

The application pairs a **trained Scikit-Learn classification model** running behind a **Python Flask REST API** with an interactive **React Single-Page Application (SPA)** that collects demographic, occupational, and psychological indicators to return immediate risk evaluations and actionable recommendations.

---

## Table of Contents
- [Features](#features)
- [System Architecture](#system-architecture)
- [Assessed Indicators & Features](#assessed-indicators--features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Backend Setup (Flask API + ML Model)](#1-backend-setup-flask-api--ml-model)
  - [2. Frontend Setup (React Application)](#2-frontend-setup-react-application)
- [API Reference](#api-reference)
- [Model Details & Preprocessing](#model-details--preprocessing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Predictive ML Classification**: Pre-trained Scikit-Learn model (`mental_model.pkl`) evaluating multi-dimensional mental health signals.
- **Multivariate Assessment Questionnaire**:
  - Demographic & occupational profile (Gender, Country, Occupation, Employment mode).
  - Clinical history (Family history of mental illness, past treatment history).
  - Behavioral & lifestyle factors (Days indoors, coping struggles, habit changes, work interest, mood swings).
  - Workplace support perception (Knowledge of care options, willingness to discuss mental health).
- **Responsive React Frontend**: Real-time validation, clean form controls, and immediate visual risk feedback.
- **RESTful Architecture**: Decoupled Python Flask backend enabling easy integration with mobile or web clients.

---

## System Architecture

```mermaid
flowchart LR
    User["User / Wellness Coordinator"]
    ReactUI["React Frontend Client (:3000)"]
    Flask["Flask REST API (:5000)"]
    Encoder["Scikit-Learn Label Encoders"]
    Model[("Trained Model: mental_model.pkl")]

    User <-->|Fill Assessment| ReactUI
    ReactUI <-->|POST /predict (JSON)| Flask
    Flask -->|Categorical Vector| Encoder
    Encoder -->|Encoded Features| Model
    Model -->|Binary Risk Prediction| Flask
```

---

## Assessed Indicators & Features

The model processes 16 categorical and behavioral attributes:

| Feature Name | Description | Possible Values |
| :--- | :--- | :--- |
| `Gender` | Biological sex or self-identified gender | `Male`, `Female`, `Other` |
| `Country` | Country of residence | `Kenya`, `USA`, `UK`, `Other` |
| `Occupation` | Professional domain | `Teacher`, `Engineer`, `Doctor`, `Other` |
| `self_employed` | Independent contractor / business owner status | `Yes`, `No` |
| `family_history` | Family background of mental health disorders | `Yes`, `No` |
| `treatment` | Prior history of mental health counseling or treatment | `Yes`, `No` |
| `Days_Indoors` | Duration spent indoors without social outdoor activity | `1-14 days`, `15-30 days`, `31+ days` |
| `Growing_Stress` | Perceived escalation of daily stress | `Yes`, `No` |
| `Changes_Habits` | Notable disruptions to sleep, diet, or routines | `Yes`, `No` |
| `Mental_Health_History` | Documented personal history of mental health challenges | `Yes`, `No` |
| `Mood_Swings` | Frequent abrupt emotional shifts | `Yes`, `No` |
| `Coping_Struggles` | Frequency of difficulty managing life stressors | `Never`, `Sometimes`, `Often` |
| `Work_Interest` | Degree of engagement and focus in daily tasks | `Low`, `Medium`, `High` |
| `Social_Weakness` | Self-reported difficulty in social interactions | `Low`, `Medium`, `High` |
| `mental_health_interview` | Willingness to discuss mental wellness with an employer | `Yes`, `No` |
| `care_options` | Awareness of available employer or community care resources | `Yes`, `No` |

---

## Project Structure

```
Mental-Health-Project/
├── backend/
│   ├── model/
│   │   └── mental_model.pkl          # Serialized Scikit-Learn trained model
│   ├── app.py                        # Flask API server & prediction handler
│   ├── analyze_model.py              # Model inspection script
│   ├── test_predict_thorough.py      # Automated model input validation
│   ├── test_requests.py              # Mock HTTP client test script
│   └── requirements.txt              # Python library dependencies
├── frontend/
│   ├── public/                       # Static index HTML & assets
│   ├── src/
│   │   ├── App.js                    # Assessment form & state management
│   │   ├── App.css                   # Custom responsive styling
│   │   └── index.js                  # React DOM entry point
│   ├── package.json                  # NPM packages & scripts
│   └── webpack.config.js             # Webpack build configuration
└── .gitignore                        # Git exclusions for Python & Node
```

---

## Getting Started

### Prerequisites
- **Python**: 3.9, 3.10, or 3.11
- **Node.js**: v16 or higher with npm

---

### 1. Backend Setup (Flask API + ML Model)

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start the Flask server
python app.py
```
The Flask server will start listening on `http://127.0.0.1:5000`.

---

### 2. Frontend Setup (React Application)

In a separate terminal window:

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Launch development server
npm start
```
The React application will launch at **[http://localhost:3000](http://localhost:3000)**.

---

## API Reference

### Health / Root Check
- **`GET /`**
  - Validates API availability and model loading status.

### Predict Mental Health Risk
- **`POST /predict`**
  - **Headers**: `Content-Type: application/json`
  - **Payload Example**:
    ```json
    {
      "features": [
        "Male", "USA", "Engineer", "No", "Yes", "Yes",
        "1-14 days", "Yes", "Yes", "Yes", "Yes", "Sometimes",
        "Medium", "Medium", "No", "Yes"
      ]
    }
    ```
  - **Success Response (200 OK)**:
    ```json
    {
      "prediction": 1,
      "status": "success",
      "interpretation": "Mental health consultation recommended."
    }
    ```

---

## Model Details & Preprocessing

- **Algorithm**: Supervised Classification (Random Forest / Logistic Regression pipeline).
- **Encoding**: Scikit-Learn `LabelEncoder` for uniform mapping of qualitative survey responses to numeric tensors.
- **Persistence**: Saved via `joblib` for fast zero-overhead deserialization in serverless or containerized environments.

---

## Disclaimer

*MindPulse is a research and educational prototype designed for informational risk screening. It is **not** a substitute for professional medical advice, clinical diagnosis, or psychotherapy. If you or someone you know is experiencing a mental health crisis, please contact a licensed healthcare provider or your local emergency crisis hotline.*

---

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/model-calibration`).
3. Commit your changes (`git commit -m 'feat: improve label encoder handling for unseen categories'`).
4. Push to your branch (`git push origin feature/model-calibration`).
5. Open a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).
