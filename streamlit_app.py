import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Education Analytics Dashboard", layout="wide")

st.title("🎓 Education Analytics Dashboard")

# Read data from CSV
df = pd.read_csv("students.csv")

st.subheader("Student Data")
st.dataframe(df)

st.subheader("Average Marks by Subject")
avg_marks = df[["math", "science", "english"]].mean()

fig, ax = plt.subplots()
ax.bar(avg_marks.index, avg_marks.values)
ax.set_ylabel("Average Marks")
st.pyplot(fig)

st.subheader("Student Attendance")

fig2, ax2 = plt.subplots()
ax2.bar(df["name"], df["attendance"])
ax2.set_ylabel("Attendance (%)")
st.pyplot(fig2)

st.subheader("Pass vs Fail")

result_count = df["result"].value_counts()

fig3, ax3 = plt.subplots()
ax3.pie(result_count, labels=result_count.index, autopct="%1.1f%%", startangle=90)
st.pyplot(fig3)