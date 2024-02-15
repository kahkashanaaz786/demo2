import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from plotly.offline import iplot, plot
from plotly.subplots import make_subplots
import warnings
import datetime
import streamlit as st

# Load data
df = pd.read_csv(r"job and salary.csv")

# Title
emoji = "📊"
st.title(f"{emoji} Job and Salary Dashboard {emoji}")
st.image('s.jfif', caption='The more the Salary the happier we be', use_column_width=True)

# Sidebar Filters
selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(df['work_year'].unique()))
selected_experience_level = st.sidebar.selectbox("Select Experience Level", ["All"] + list(df['experience_level'].unique()))

# Filter data based on selected filters
if selected_year != "All":
    df_filtered = df[df['work_year'] == selected_year]
else:
    df_filtered = df

if selected_experience_level != "All":
    df_filtered = df_filtered[df_filtered['experience_level'] == selected_experience_level]

# Remove unnecessary columns and duplicates
df_filtered.drop(['salary', 'company_location'], axis=1, inplace=True)
df_filtered.drop_duplicates(inplace=True)

# Years of Work plot
emoji = "💵"
st.subheader(f"{emoji} Years of Work Plot: {emoji}")
fig_years_of_work = px.line(df_filtered['work_year'].value_counts(), x=df_filtered['work_year'].value_counts().index, y=df_filtered['work_year'].value_counts().values,
                            markers=True, labels={'x': 'Year', 'y': 'Number of Employees'},
                            title=f'Years of Work for {selected_year}', line_shape="linear",
                            color_discrete_sequence=['#cc2114'], template='plotly_dark')
st.plotly_chart(fig_years_of_work)

# Job Title with Salaries USD plot
emoji = "💰"
st.subheader(f"{emoji} Job Title with Salaries USD Plot: {emoji}")
df_job_title_USD = df_filtered.groupby('job_title')['salary_in_usd'].sum()
fig_job_title_salary = px.bar(df_job_title_USD.sort_values(ascending=False)[:10], orientation='h',
                               labels={'value': 'Salary in USD', 'job_title': 'Job Title'},
                               title='Job Title with Salaries USD', template='plotly_dark',
                               color=df_job_title_USD.index[:10], text_auto=True)
st.plotly_chart(fig_job_title_salary)

# Sidebar Filters
selected_currency = st.sidebar.selectbox("Select Preferred Currency", ["All"] + list(df['salary_currency'].unique()))

# Filter data based on selected filters
if selected_currency != "All":
    df_filtered = df[df['salary_currency'] == selected_currency]
else:
    df_filtered = df

# Remove unnecessary columns if they exist
if 'salary' in df.columns and 'company_location' in df.columns:
    df.drop(['salary', 'company_location'], axis=1, inplace=True)


col1, col2 = st.columns(2)
# Job Category General plot
with col1:
    emoji = "📉 "
    st.subheader(f"Job Category General Plot {emoji}")

    df_job_category_general = df_filtered['job_category'].value_counts()
    fig_job_category_general = px.bar(df_job_category_general,
                                      labels={'job_category': 'Job Category'},
                                      title=f"Needed of Jobs Category in {selected_year}",
                                      color_discrete_sequence=['#b3079c'],
                                      template='plotly_dark',
                                      text_auto=True)
    st.plotly_chart(fig_job_category_general)



col1, col2 = st.columns(2)
# Employee Residence plot
with col1:
    emoji = "🤑"
    st.subheader(f"Employee Residence Plot {emoji}")

    df_employee_residence = df_filtered['employee_residence'].value_counts()
    fig_employee_residence = px.bar(df_employee_residence[:10],
                                     template='plotly_dark',
                                     labels={'employee_residence': 'Name of Country', 'value': 'Value'},
                                     title='Top Country in the World in Data Science',
                                     text_auto=True,
                                     color_discrete_sequence=['#dd0be0'])
    st.plotly_chart(fig_employee_residence)

# Employment Type plot
with col2:
    emoji = "🌐"
    st.subheader(f"Employment Type Plot {emoji}")

    df_employment_type = df_filtered['employment_type'].value_counts()
    fig_employment_type = px.bar(df_employment_type,
                                  template='plotly_dark',
                                  labels={'employment_type': 'Employment Type', 'value': 'Value'},
                                  title='Type of Employment for Data Analysts',
                                  text_auto=True,
                                  color_discrete_sequence=['#dd0be0'])
    st.plotly_chart(fig_employment_type)

# Salary by Employee Residence plot
emoji = "📉 "
st.subheader(f"Salary by Employee Residence Plot {emoji}")

fig_salary_by_residence = px.scatter_geo(df_filtered,
                                         locations='employee_residence',
                                         locationmode='country names',
                                         color='salary_in_usd',
                                         hover_name='employee_residence',
                                         title='Salary by Employee Residence')
st.plotly_chart(fig_salary_by_residence)

# Experience Level pie chart
emoji = "🤝"
st.subheader(f"Experience Level Pie Chart {emoji}")

# Count the occurrences of each experience level
df_experience_level = df_filtered['experience_level'].value_counts()

# Create the pie chart
fig_experience_level = px.pie(values=df_experience_level.values,
                              names=df_experience_level.index,  # Use index as names
                              title='Experience Level for Data Analysts').update_traces(textinfo='percent+label')

# Display the pie chart
st.plotly_chart(fig_experience_level)

