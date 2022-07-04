import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
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

    st.write("""

             - ##### USA, India and Germany constituted to about 50% of the Stack Overflow users taking this survey in 2021.
             - ##### Brazil is the only country from the South American continent to be in the top 20 countries.


             """)

    data = df["Country"].value_counts()

    fig1,ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct ="%1.1f%%", shadow = False, startangle = 0)
    ax1.axis("equal")

    st.write("""#### Data from different countries""")

    st.pyplot(fig1)

    st.write("""
    ### Mean Salary based on country""")

    st.write("""

            - #####  USA, Israel and Switzerland are the only countries where the mean salary is above 100,000 dollars in 
               ##### 2021.
            - #####  Brazil, India and Turkey have the lowest mean salaries in 2021.


                 """)

    data= df.groupby(['Country'])["Salary"].mean().sort_values()
    st.bar_chart(data)

    st.write("""
    ### Mean Salary based on experience
    """)

    st.write("""

            - #####  The plot seems more or less linear up to the 35 years of experience 
               ##### point after which the salary fluctuates to a great extent.
            - #####  Salaries after 45 years of experience show a drop, possibly indicating retirement.


                 """)

    data = df.groupby(['YearsCodePro'])["Salary"].mean().sort_values()
    st.line_chart(data)

    st.title("Explore 2018,2019,2020 and 2021 data from Stack-Overflow")

    st.write("""### Salary US$ vs Country
    
    
    """)

    st.write("""

           - #####  Highest median Salary is of 110,000 US dollars in the USA.
           - #####  Lowest Median Salary is seen in India of 12,000 US dollars.


                     """)


    df11 = df1.copy()
    country_map = shorten_categories(df1.Country.value_counts(), 1200)
    df11['Country'] = df11['Country'].map(country_map)

    fig = px.box(df11,x='Country',y='salary')
    fig.update_layout(yaxis_range=[0,250001])
    st.plotly_chart(fig)

    st.write("""### Mean Salary for various Sexual orientations""")
    st.write("""

             - #####  Users under the category of Gay or Lesbian as their Sexual orientation have the highest mean 
               ##### salary of about 78,000 USD annually.
             - ##### Lowest mean salary of 54,800 USD is seen for the category of Asexual users.
             - ##### It must be noted that the number of users from each category who took this survey may largely 
               ##### affect the mean salaries. (Pie chart below demonstrates the point.)


                     """)

    sexuality_dist = df1.groupby(['Sexuality'], as_index=False).agg({'salary': pd.Series.mean})
    fig = px.pie(data_frame=sexuality_dist, names='Sexuality', values="salary")
    st.plotly_chart(fig)

    st.write("""### Number of users across sexual orientations""")
    st.write("""

             - #####  Almost 90% of the users who took the survey fall under the category of Man.
                     


                     """)

    fig = px.pie(names=df1["Sexuality"].value_counts().index, values=df1["Sexuality"].value_counts().values)
    fig.update_traces(textposition='outside', textinfo='label+percent')
    st.plotly_chart(fig)

    st.write("""### Mean Salary for Age groups""")
    st.write("""

            -  #####  The age group of 55-65 earns the highest mean salary of more than 114,000 USD per year. 
                     


                     """)




    age_dist = df1.groupby(['Age'],as_index=False).agg({'salary': pd.Series.mean})

    fig = px.pie( data_frame=age_dist, names='Age', values="salary")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

    st.write("""### Total money earned vs Age group and Genders.""")
    st.write("""

            - #####  The group of 25-30 year old men have earned almost 2.2 Billion USD from 2018 - 2021, 
               ##### which is the highest.
            - #####  Even though the age group of 55-60 has the highest mean salary, this group has earned a total
               ##### of less than half a billion USD from 2018-2021.  



                         """)


    sal_dist = df1.groupby(['Age',"Gender"],as_index=False).agg({'salary': pd.Series.sum})
    bar = px.bar(data_frame=sal_dist,x="Age",y='salary',color="Gender",width=1000)
    bar.update_yaxes(title = "Total salary earned in USD $")
    st.plotly_chart(bar)


    st.write("""### Coutry-wise and Educational level-wise mean salaries. """)
    st.write("""

            - #####  Users from the USA with a Doctorate have the highest mean salary of about 146,000 USD.  
            - #####  Users from USA who have an Education of below graduation, earn almost 3 times more than
               ##### users with a Doctorate degree from India,Mexico and Ukraine. 
                            
                         


                         """)

    d = df11.groupby(['Country', 'EdLevel'],
                     as_index=False).agg({'salary': pd.Series.mean})
    d.sort_values(by='salary', ascending=False, inplace=True)
    fig = px.bar(x=d.salary,
                   y=d.Country,
                   color=d.EdLevel,
                   orientation="h",width=1000,height=650)

    fig.update_layout(xaxis_title='Mean salary in USD',
                        yaxis_title='Country')
    st.plotly_chart(fig)
    #
    st.write("""### Mean Salaries of Genders with different Employment status""")
    st.write("""

           - #####  Mean salary of Females who are not employed is almost 3000 USD more than the mean salary
              ##### of female users who are employed full time.
           - #####  It is difficult to draw any inference on the salaries of users who are retired, as there 
              ##### are only male users who are retired and have input their salary details.


                             """)

    d = df1.groupby(['Gender', 'Employment'],
                    as_index=False).agg({'salary': pd.Series.mean})
    d.sort_values(by='salary', ascending=False, inplace=True)
    fig = px.bar(x=d.salary,
                   y=d.Gender,
                   color=d.Employment,
                   orientation="h",width=1000)

    fig.update_layout(xaxis_title='Mean salary in USD',
                        yaxis_title='Gender spectrum')
    st.plotly_chart(fig)
    #
    st.write("""### Number of users across Gender spectrum""")

    st.write("""

             - #####  Almost 92% of the users have been men.
             - #####  This is to be kept in mind while considering other gender based inferences drawn 
                ##### from the study.


                                 """)

    fig =px.pie(names= df1["Gender"].value_counts().index,values = df1["Gender"].value_counts().values,labels=df1["Gender"].value_counts().index)
    st.plotly_chart(fig)
    #



    st.write("""### WordClouds
     
     """)

    st.write("""

            - #####  Size of the word in the below Wordclouds correspond to the number of times 
               ##### that word was used.
            - #####  It can be seen that Javascript, Python, HTML, CSS and SQL remain to be the top
               ##### programming languages that users are currently working with or would like to work with
               ##### in the future.
                               



                                     """)

    st.write("""#### Word Cloud of Languages that the users have to use currently

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

    st.write("""#### Word Cloud of Languages that the users want to use in the future
    
    """)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(word_cloud2)
    plt.axis("off")
    st.pyplot(fig)

    st.write("""### Sunburst!

     """)

    st.write("""

            - #####  Below is the highly interactive and informative Plotly Sunburst object.
               ##### (Click and hover for specific insights.)
            - #####  The path from center in the order of Year,Country,Employment status and finally the education level.
            - #####  The color scale of the Sunburst chart corresponds to mean salary in USD.                    



                                     """)



    ## SUNBURST
    sun = df11.groupby(['year','Employment',"Country","EdLevel"], as_index=False).agg({'salary': pd.Series.mean})
    fig = px.sunburst(data_frame=sun,path=['year',"Country",'Employment',"EdLevel"], names='year',values='salary',color='salary'
                      ,color_continuous_scale='RdBu',width=1000,height=650)
    fig.update_traces(outsidetextfont_family= "Arial",insidetextfont_family="Arial",hoverlabel_font_size=
                        15, selector = dict(type='sunburst'))
    fig.update_layout(coloraxis_showscale = True)

    st.plotly_chart(fig)



