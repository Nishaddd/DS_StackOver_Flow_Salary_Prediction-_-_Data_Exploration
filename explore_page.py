import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(cat,cut_off):
    cat_map = {}
    for i in range(len(cat)):
        if cat.values[i] >= cut_off:
            cat_map[cat.index[i]] = cat.index[i]
        else:
            cat_map[cat.index[i]] = "other"
    return cat_map

def clean_exp(x):
    if x == 'Less than 1 year':
        return 0.5
    elif x == 'More than 50 years':
        return 50
    return float(x)

def clean_edu (x):
    if "Master’s degree" in x:
        return "Master's Degree"
    if "Bachelor’s degree" in x:
        return "Bachelor’s Degree"
    if "Professional degree" in x or "doctoral degree" in x :
        return "Post grad"
    return "Less than a bachelors"


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[['Country', 'EdLevel', "YearsCodePro", 'Employment', "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df.dropna(inplace=True)
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop('Employment', axis=1)
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 200000]
    df = df[df["Salary"] >= 1000]
    df = df[df["Country"] != "other"]
    df.YearsCodePro = df.YearsCodePro.apply(clean_exp)
    df.EdLevel = df.EdLevel.apply(clean_edu)
    return df

df  = load_data()

def show_explore():
    st.title("Explore Software Engineer Salaries")
    st.write("""
    
    ## Stack Overflow Developer Salaries 2021
    
    """)

    data = df["Country"].value_counts()

    fig1,ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct ="%1.1f%%", shadow = False, startangle = 0)
    ax1.axis("equal")

    st.write("""#### Data from different countries""")

    st.pyplot(fig1)

    st.write("""### 
    Mean Salary based on country""")

    data= df.groupby(['Country'])["Salary"].mean().sort_values()
    st.bar_chart(data)

    st.write("""
    ### Mean Salary based on experience
    """)

    data = df.groupby(['YearsCodePro'])["Salary"].mean().sort_values()
    st.line_chart(data)





















