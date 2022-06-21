import streamlit as st
import numpy as np
import pickle


def load_model():
    with open('saved_steps.pkl', 'rb') as f:
        dt = pickle.load(f)
    return dt

data = load_model()

regressor_loaded = data["model"]
le_c = data["le_country"]
le_e =data["le_edu"]

def show_predict():
    st.title ("Software Developer Salary Prediction-2021")

    st.write("""## We need some information to predict the salary""")

    countries = ("United States of America",
                "India",
                "Germany",
                "United Kingdom of Great Britain and Northern Ireland",
                "Canada",
                "Brazil",
                "France",
                "Spain",
                "Netherlands",
                "Australia",
                "Poland" ,
                "Russian Federation",
                "Sweden",
                "Italy",
                "Turkey",
                "Israel",
                "Switzerland",
                "Norway" )

    education = ("Master's Degree", 'Bachelor’s Degree', 'Post grad',"Less than a bachelors")

    country = st.selectbox("Country",countries)
    education = st.selectbox("Educational Level",education)
    experience = st.slider("Years of experience",0,30,3)

    ok = st.button("Calculate Salary")

    if ok :
        x =np.array([[country,education,experience]])
        x[:,0] = le_c.transform(x[:,0])
        x[:,1] = le_e.transform(x[:,1])
        x=x.astype(float)

        salary = (regressor_loaded.predict(x))*78.07
        st.subheader(f"estimated salary converted rupees : {salary[0]:.2f}")