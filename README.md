# Loan Approval Predictor — MVP (FastAPI backend + Streamlit frontend)

**Structure** (separate folders for backend and frontend):
```
loan-approval/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       └── test_api.py
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── colab/loan_model_training.ipynb
├── .github/workflows/ci-cd.yml
└── README.md
```

## Quick local run (dev)
1. Train the model using the Colab notebook (open `colab/loan_model_training.ipynb`) or run a local training script to create `backend/model/loan_model.pkl`.
2. Start backend (from repo/backend):
   ```bash
   pip install -r backend/requirements.txt
   uvicorn main:app --reload --port 8000
   ```
3. Start frontend (from repo/frontend):
   ```bash
   pip install -r frontend/requirements.txt
   streamlit run app.py --server.port 8501
   ```
4. Use the Streamlit UI to call the backend at http://localhost:8000/predict

## Deployed on Render
1. Frontend: https://loan-approval-frontend-latest.onrender.com/
2. Backend: https://loan-approval-backend-latest.onrender.com/predict

## DevOps 
- **CI (GitHub Actions)**: runs tests and lints, builds Docker images. Automates checks so changes don't break the system.
- **Containerization (Docker)**: packages backend & frontend for consistent deployment across environments.
- **CD (Render)**: push-to-deploy services that automatically update on new commits (connect GitHub repo).
- **Model Versioning**: trained model `loan_model.pkl` is stored in backend. The CI pipeline validates model metrics before deployment to prevent regressions.
- **Benefits**: reduces manual approval delays, avoids human copy/paste errors, and provides repeatable, auditable deployments.
