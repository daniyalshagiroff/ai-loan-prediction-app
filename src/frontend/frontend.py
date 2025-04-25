import streamlit as st
import requests

# Page title
st.title('AI Loan Approval Prediction')

st.write("Enter the details. Only Loan Term and CIBIL Score are mandatory.")

# Mandatory fields
loan_term = st.number_input('Loan Term (in months)', min_value=1, max_value=480, value=12)
cibil_score = st.number_input('CIBIL Score', min_value=300, max_value=900, value=700)

st.markdown("---")  # Divider line

st.subheader('Optional Fields')

no_of_dependents = st.text_input('Number of Dependents (OPTIONAL)')
education = st.selectbox('Education (OPTIONAL)', options=[None, 0, 1], format_func=lambda x: "-" if x is None else "Graduate" if x == 0 else "Not Graduate")
self_employed = st.selectbox('Self Employed (OPTIONAL)', options=[None, 0, 1], format_func=lambda x: "-" if x is None else "No" if x == 0 else "Yes")

income_annum = st.text_input('Annual Income (OPTIONAL)')
loan_amount = st.text_input('Loan Amount (OPTIONAL)')
residential_assets_value = st.text_input('Residential Assets Value (OPTIONAL)')
commercial_assets_value = st.text_input('Commercial Assets Value (OPTIONAL)')
luxury_assets_value = st.text_input('Luxury Assets Value (OPTIONAL)')
bank_asset_value = st.text_input('Bank Asset Value (OPTIONAL)')

# Submit button
if st.button('Check Loan Approval'):
    # Prepare data
    data = {
        "no_of_dependents": int(no_of_dependents) if no_of_dependents else None,
        "education": education,
        "self_employed": self_employed,
        "income_annum": int(income_annum) if income_annum else None,
        "loan_amount": int(loan_amount) if loan_amount else None,
        "loan_term": loan_term,
        "cibil_score": cibil_score,
        "residential_assets_value": int(residential_assets_value) if residential_assets_value else None,
        "commercial_assets_value": int(commercial_assets_value) if commercial_assets_value else None,
        "luxury_assets_value": int(luxury_assets_value) if luxury_assets_value else None,
        "bank_asset_value": int(bank_asset_value) if bank_asset_value else None
    }

    # Send request to Flask API
    try:
        response = requests.post('http://127.0.0.1:5000/predict', json=data)

        if response.status_code == 200:
            result = response.json()
            if result['prediction'] == 1:
                st.success('✅ The loan is most likely to be APPROVED!')
            else:
                st.error('❌ The loan is most likely to be REJECTED!')
        else:
            st.error('Server error: ' + str(response.status_code))

    except Exception as e:
        st.error(f'Connection error: {e}')