import streamlit as st
import requests
import json

st.set_page_config(page_title='Loan Approval Demo', layout='centered')

st.title('Loan Approval Predictor — Demo (Streamlit)')
st.write('Fill the form and click **Predict**. This app calls the FastAPI backend at /predict.')

with st.form('loan_form'):
    gender = st.selectbox('Gender', ['Male', 'Female', None])
    married = st.selectbox('Married', ['Yes', 'No', None])
    education = st.selectbox('Education', ['Graduate', 'Not Graduate', None])
    applicant_income = st.number_input('Applicant Income', value=2500.0)
    coapp_income = st.number_input('Coapplicant Income', value=0.0)
    loan_amount = st.number_input('Loan Amount (in thousands)', value=100.0)
    credit_history = st.selectbox('Credit History', [1.0, 0.0, None])
    property_area = st.selectbox('Property Area', ['Urban', 'Rural', 'Semiurban', None])
    submit = st.form_submit_button('Predict')

if submit:
    payload = {
        'Gender': gender,
        'Married': married,
        'Education': education,
        'ApplicantIncome': applicant_income,
        'CoapplicantIncome': coapp_income,
        'LoanAmount': loan_amount,
        'Credit_History': credit_history,
        'Property_Area': property_area
    }

    backend_url = 'http://localhost:8000/predict'
    try:
        r = requests.post(backend_url, json=payload, timeout=5)
        if r.status_code == 200:
            res = r.json()
            if 'error' in res:
                st.error(res['error'])
            else:
                if res.get('approved') == 'Yes':
                    st.success(f"Approved ✅ — score: {res.get('score'):.3f}")
                else:
                    st.error(f"Rejected ❌ — score: {res.get('score'):.3f}")
        else:
            st.error(f'Backend returned status {r.status_code}')
    except Exception as e:
        st.error(f'Error calling backend: {e}')
