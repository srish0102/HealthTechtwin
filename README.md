# HealthTechtwin: AI-Powered Metabolic Digital Twin

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

> **A Clinical Decision Support System (CDSS) that simulates metabolic health outcomes using Machine Learning and real-time parameter tuning.**

---

## Executive Summary
**HealthTechtwin** is not just a disease predictor; it is a **Digital Twin Simulator**. While traditional AI models simply output a binary classification (Sick/Healthy), MetaboTwin creates a dynamic virtual profile of the patient. It allows users to adjust critical lifestyle variables—such as Glucose levels, BMI, and Sleep patterns—to visualize how specific changes impact their long-term health risk curve in real-time.

---

## Key Features

### 1. Hospital-Grade Intake Flow
* **Secure Check-In System:** Simulates a real-world clinical kiosk with Patient ID and Name tracking.
* **Context-Aware Forms:** The application uses session-state logic to adapt questions based on biological gender (e.g., triggering *Gestational History* protocols for female patients).

### 2. Hybrid AI Architecture
* **The Core Brain:** A **Random Forest Classifier** trained on the PIMA Indians Diabetes Dataset (768 clinical records) to detect non-linear biological patterns.
* **The Logic Layer (Post-Processing):** A custom algorithm that augments the AI's raw probability score with external lifestyle factors not present in the original dataset:
    * *Smoking Penalty:* +10% probabilistic risk.
    * *Sedentary Lifestyle:* +5% metabolic penalty.
    * *Sleep Deprivation (<6hrs):* Cortisol-induced stress factor.
    * *Familial Clustering:* Cumulative risk scoring for multi-condition family history.

### 3.  Interactive "What-If" Simulation
* **Sensitivity Analysis:** The system runs **120+ micro-simulations** instantly to generate a `Glucose-to-Risk` projection curve. This helps patients understand exactly what their target glucose level should be to enter the "Safe Zone."

### 4.  Persistent Data Layer
* **Local SQL Backend:** Integrated **SQLite** database captures simulation snapshots, allowing for longitudinal tracking of patient progress over time.

---

##  Technical Architecture

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Custom CSS-styled interface with "Wizard" step logic. |
| **Model** | Scikit-Learn | Random Forest (n_estimators=100) with probability calibration. |
| **Data Engine** | Pandas / NumPy | Real-time data frame manipulation for simulation loops. |
| **Storage** | SQLite3 | Lightweight relational database for history logging. |
| **DevOps** | Git / VS Code | Version control and local environment management. |

---

##  Installation & Usage

### Prerequisites
* Python 3.8 or higher
* VS Code (Recommended)
* Can use Google collab but there can be isuues with the UI

### Step 1: Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/MetaboTwin.git](https://github.com/YOUR_USERNAME/MetaboTwin.git)
cd MetaboTwin



Step 2: Set Up Virtual Environment

Linux/Mac:
           python3 -m venv venv
           source venv/bin/activate
Windowns:
           python -m venv venv
          .\venv\Scripts\activate

Step 3: Install Dependencies 

pip install -r requirements.txt

Step 4: Initialize the System
First, train the model to generate the twin_brain.pkl file:
          python3 TrainModel.py

Then, launch the application: 
          streamlit run app.py


>>>Project Structure 

HealthTechtwin/
│
├── Data/
│   └── diabetes.csv        # PIMA Clinical Dataset (Raw Data)
│
├── Models/
│   └── twin_brain.pkl      # Serialized Machine Learning Model
│
├── app.py                  # Main Application (UI, Logic Layer, Simulation Loop)
├── db_manager.py           # Database Interface (SQL Operations)
├── TrainModel.py           # Training Pipeline (Preprocessing -> Training -> Serialization)
├── requirements.txt        # Project Dependencies
└── README.md               # Documentation

Future Roadmap (v2.0)
> Dataset Migration: Transitioning to the CDC BRFSS Dataset (250k+ records) for higher demographic fidelity.
> LLM Integration: Implementing an OpenAI API wrapper to provide natural language explanations of the risk factors.
> Wearable Sync: API endpoints to ingest real-time data from Fitbit/Apple Health.

## Contributing

Contributions are always welcome! If you have ideas to improve the medical logic or UI, please follow these steps:

1.  **Fork** the repository.
2.  Create a new branch (`git checkout -b feature-improve-logic`).
3.  Commit your changes (`git commit -m 'Added BMI visualization'`).
4.  Push to the branch (`git push origin feature-improve-logic`).
5.  Open a **Pull Request**.

### Star this Repo
If you find this project useful or interesting, please give it a star! It helps others find it.
