import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("University Analytics Dashboard")

df = pd.read_csv("university_student_data.csv")

st.sidebar.header("Filters")

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

selected_term = st.sidebar.multiselect(
    "Select Term",
    options=df["Term"].unique(),
    default=df["Term"].unique()
)

filtered_df = df[
    (df["Year"].isin(selected_year)) &
    (df["Term"].isin(selected_term))
]

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Retention",
    f"{filtered_df['Retention Rate (%)'].mean():.1f}%"
)

col2.metric(
    "Average Satisfaction",
    f"{filtered_df['Student Satisfaction (%)'].mean():.1f}%"
)

col3.metric(
    "Total Enrolled",
    int(filtered_df["Enrolled"].sum())
)

st.subheader("Retention Rate Over Time")

retention = filtered_df.groupby("Year")["Retention Rate (%)"].mean()

fig1, ax1 = plt.subplots(figsize=(8,5))

ax1.plot(
    retention.index,
    retention.values,
    marker='o'
)

st.pyplot(fig1)

st.subheader("Student Satisfaction by Year")

fig2, ax2 = plt.subplots(figsize=(8,5))

sns.barplot(
    data=filtered_df,
    x="Year",
    y="Student Satisfaction (%)",
    ax=ax2
)

st.pyplot(fig2)

st.subheader("Enrollment by Department")

department_data = {
    "Engineering": filtered_df["Engineering Enrolled"].sum(),
    "Business": filtered_df["Business Enrolled"].sum(),
    "Arts": filtered_df["Arts Enrolled"].sum(),
    "Science": filtered_df["Science Enrolled"].sum()
}

fig3, ax3 = plt.subplots(figsize=(7,7))

ax3.pie(
    department_data.values(),
    labels=department_data.keys(),
    autopct='%1.1f%%'
)

st.pyplot(fig3)

st.subheader("Filtered Data")

st.dataframe(filtered_df)