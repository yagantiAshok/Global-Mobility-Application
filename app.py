


import scipy
import scipy.sparse
import sklearn
from sklearn.pipeline import Pipeline
from visa.constants import SCHEMA_FILE
import streamlit as st
from visa.pipeline.prediction_pipeline import visaData,VisaClassifier

from visa.utils.main_utile import read_yaml

data = read_yaml(SCHEMA_FILE)

defualt = data.ui.default_columns

st.set_page_config("Visa Approval",layout="centered")
st.title("VIsa Approval Status")
st.header("Applicant Deatils")


cols = st.columns(2)

with cols[0]:
    
    continent = st.selectbox("Continent",options=['Asia', 'Africa', 'North America', 'Europe', 'South America', 'Oceania'], index= 0 if defualt["continent"]=="Asia" else 1 )
    education_of_employee = st.selectbox("Education_of_employee",options=['High School', "Master's", "Bachelor's", 'Doctorate'],index= 0 if defualt["education_of_employee"]=="maters's" else 1)
    has_job_experience = st.selectbox("Has_job_experience",options=['N', 'Y'],index= 0 if defualt["has_job_experience"]=="Y" else 1)
    requires_job_training = st.selectbox("Requires_job_training",options=['N', 'Y'],index = 0 if defualt["requires_job_training"]=="N" else 1)
    no_of_employees = st.number_input("No_of_employees",value = int(defualt["no_of_employees"]))

with cols[1]:
    region_of_employment = st.selectbox("Region_of_employment",options = ['West', 'Northeast', 'South', 'Midwest', 'Island'],index= 0 if defualt["region_of_employment"]=="west" else 1)
    prevailing_wage = st.number_input("Prevailing_wage", value= float(defualt["prevailing_wage"]))
    unit_of_wage = st.selectbox("Unit_of_wage",options=['Hour', 'Year', 'Week', 'Month'],index= 0 if defualt["unit_of_wage"]=="year" else 1)
    full_time_position = st.selectbox("full_time_position",options=['N', 'Y'], index= 0 if defualt["full_time_position"]=="Y" else 1)
    comapny_age = st.number_input("comapny_age",value = int(defualt["comapny_age"]))




data = visaData(continent=continent,
                education_of_employee=education_of_employee,
                has_job_experience=has_job_experience,
                requires_job_training=requires_job_training,
                no_of_employees=no_of_employees,
                region_of_employment=region_of_employment,
                prevailing_wage=prevailing_wage,
                unit_of_wage=unit_of_wage,
                full_time_position=full_time_position,
                comapny_age=comapny_age)

data_frame = data.get_visa_data_in_dataframe()

prediction = VisaClassifier()

result = prediction.predict(data_frame=data_frame)[0]

if st.button("Predict"):

    if result == 0 :

        st.success("VISA APPROVED")
    else:

        st.error("VISA REJECTED")



                    




