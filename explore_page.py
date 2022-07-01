import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
from wordcloud import WordCloud
import seaborn as sns
import plotly.express as px


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

def shorten_categories(cat,cut_off):
    cat_map = {}
    for i in range(len(cat)):
        if cat.values[i] >= cut_off:
            cat_map[cat.index[i]] = cat.index[i]
        else:
            cat_map[cat.index[i]] = "other"
    return cat_map


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

@st.cache
def load_data1():
    df1 = pd.read_csv("clean_df.csv")
    return df1


df  = load_data()
df1 = load_data1()


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

    st.write("""
    ### Mean Salary based on country""")

    data= df.groupby(['Country'])["Salary"].mean().sort_values()
    st.bar_chart(data)

    st.write("""
    ### Mean Salary based on experience
    """)

    data = df.groupby(['YearsCodePro'])["Salary"].mean().sort_values()
    st.line_chart(data)

    st.title("Explore 2018,2019,2020 and 2021 data from Stack-Overflow")

    st.write("""### Salary US$ vs Country
    
    
    """)
    df11 = df1.copy()
    country_map = shorten_categories(df1.Country.value_counts(), 1200)
    df11['Country'] = df11['Country'].map(country_map)

    fig = px.box(df11,x='Country',y='salary')
    st.plotly_chart(fig)

    st.write("""### Mean Salary for various Sexual orientations""")

    sexuality_dist = df1.groupby(['Sexuality'], as_index=False).agg({'salary': pd.Series.mean})
    fig = px.pie(data_frame=sexuality_dist, names='Sexuality', values="salary")
    st.plotly_chart(fig)

    st.write("""### Number of users across sexual orientations""")


    fig = px.pie(names=df1["Sexuality"].value_counts().index, values=df1["Sexuality"].value_counts().values)
    st.plotly_chart(fig)

    st.write("""### Mean Salary for Age groups""")

    age_dist = df1.groupby(['Age'], as_index=False).agg({'salary': pd.Series.mean})
    fig = px.pie(data_frame=age_dist, names='Age', values="salary")
    st.plotly_chart(fig)

    st.write("""### Mean Salaries for different Education levels for all countries""")
    d = df11.groupby(['Country', 'EdLevel'],
                     as_index=False).agg({'salary': pd.Series.mean})
    d.sort_values(by='salary', ascending=False, inplace=True)
    fig = px.bar(x=d.salary,
                   y=d.Country,
                   color=d.EdLevel,
                   orientation="h")

    fig.update_layout(xaxis_title='Mean salary in USD',
                        yaxis_title='Country')
    st.plotly_chart(fig)
    #
    st.write("""### Mean Salaries for all Genders with different Employment status""")
    d = df1.groupby(['Gender', 'Employment'],
                    as_index=False).agg({'salary': pd.Series.mean})
    d.sort_values(by='salary', ascending=False, inplace=True)
    fig = px.bar(x=d.salary,
                   y=d.Gender,
                   color=d.Employment,
                   orientation="h")

    fig.update_layout(xaxis_title='Mean salary in USD',
                        yaxis_title='Gender spectrum')
    st.plotly_chart(fig)
    #
    st.write("""### Number of users across Gender spectrum""")
    fig =px.pie(names= df1["Gender"].value_counts().index,values = df1["Gender"].value_counts().values,labels=df1["Gender"].value_counts().index)
    st.plotly_chart(fig)
    #

    st.write("""### Mean Salary for Age groups""")
    salary_mean = df1.groupby(['year'], as_index=False).agg({'salary': pd.Series.mean})
    fig =px.pie(data_frame =salary_mean,names= 'year',values = "salary")
    st.plotly_chart(fig)
    #

    st.write("""### Word Cloud of Languages that the users have to use currently
     
     """)

    ##Wordcloud
    have_text = " ".join(df1['lang_have'])
    want_text = " ".join(df1['lang_want'])
    word_cloud1 = WordCloud(collocations=False, background_color='white').generate(have_text)
    word_cloud2 = WordCloud(collocations=False, background_color='white').generate(want_text)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(word_cloud1)
    plt.axis("off")
    st.pyplot(fig)

    st.write("""### Word Cloud of Languages that the users want to use in the future
    
    """)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(word_cloud2)
    plt.axis("off")
    st.pyplot(fig)






