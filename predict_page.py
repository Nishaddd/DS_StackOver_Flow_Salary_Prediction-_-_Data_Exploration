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
    st.title ("Software Developer Salary Prediction"
              "-Based on 2021 Stack Overflow Data")

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

        salary = (regressor_loaded.predict(x))
        st.subheader(f"Estimated yearly salary : {salary[0]:.2f}$")

        try :
            from api_request import curr_converter

            rate,status_code = curr_converter()
            if status_code == 200:
                sal = salary[0] * rate
                st.subheader(f"Salary converted to INR as of today : {sal:.2f}")

            else :
                pass
        except :
            pass

