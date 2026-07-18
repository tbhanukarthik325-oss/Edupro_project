import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Eduvista Analytics Dashboard",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📚 Eduvista Analytics Dashboard")

st.markdown("""
### Learner Demographics and Course Enrollment Behavior Analysis

Welcome to the **Eduvista Analytics Dashboard**. This interactive dashboard provides
insights into learner demographics, course enrollments, revenue generation,
teacher expertise, and payment behavior. Users can apply filters to explore
different learner segments and understand enrollment trends.
""")

st.markdown("---")

# -----------------------------
# Load Data from CSV
# -----------------------------
users = pd.read_csv("data/users.csv", sep=";")
courses = pd.read_csv("data/courses.csv", sep=";")
teachers = pd.read_csv("data/teachers.csv", sep=";")
transactions = pd.read_csv("data/transactions.csv", sep=";")

print(users.columns)
print(courses.columns)
print(teachers.columns)
print(transactions.columns)
# -----------------------------
# Convert Transaction Date
# -----------------------------
transactions["TransactionDate"] = pd.to_datetime(
    transactions["TransactionDate"]
)

transactions["Month"] = transactions["TransactionDate"].dt.strftime("%b %Y")
# -----------------------------
# Create Age Groups
# -----------------------------
users["AgeGroup"] = pd.cut(
    users["Age"],
    bins=[0, 17, 25, 35, 45, 100],
    labels=["<18", "18-25", "26-35", "36-45", "45+"]
)
# -----------------------------
# KPI Calculations
# -----------------------------
total_users = len(users)
total_courses = len(courses)
total_teachers = len(teachers)
total_enrollments = len(transactions)
total_revenue = transactions["Amount"].sum()
average_age = users["Age"].mean()

average_revenue = transactions["Amount"].mean()



average_enrollments_per_course = (
    total_enrollments / total_courses
)


# -----------------------------
# KPI Cards
# -----------------------------
st.header("📊 Dashboard Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("👥 Total Users", f"{total_users:,}")
col2.metric("📚 Total Courses", f"{total_courses:,}")
col3.metric("👨‍🏫 Total Teachers", f"{total_teachers:,}")
col4.metric("📝 Total Enrollments", f"{total_enrollments:,}")
col5.metric(
    label="💰 Total Revenue",
    value=f"₹ {total_revenue:,.0f}"
)

st.header("📈 Additional Insights")

col1, col2, col3 = st.columns(3)

col1.metric(
    label="🎂 Average Age",
    value=f"{average_age:.1f} Years"
)

col2.metric(
    label="💵 Avg Transaction",
    value=f"₹ {average_revenue:,.2f}"
)
col3.metric(
    label="📝 Avg Enrollments/Course",
    value=f"{average_enrollments_per_course:.1f}"
)

# -----------------------------
# Executive Summary
# -----------------------------
st.markdown("## 📌 Executive Summary")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"""
        👥 **Total Learners:** {total_users:,}

        📚 **Courses Available:** {total_courses:,}

        📝 **Total Enrollments:** {total_enrollments:,}
        """
    )

with col2:
    st.success(
        f"""
        💰 **Total Revenue:** ₹ {total_revenue:,.2f}

        👨‍🏫 **Total Teachers:** {total_teachers:,}

        📈 **Dashboard Status:** Updated
        """
    )
# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🎯 Filters")

selected_age = st.sidebar.selectbox(
    "Select Age Group",
    ["All"] + list(users["AgeGroup"].dropna().unique())
)

selected_gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(users["Gender"].unique())
)

selected_category = st.sidebar.selectbox(
    "Select Course Category",
    ["All"] + sorted(courses["CourseCategory"].unique())
)

selected_level = st.sidebar.selectbox(
    "Select Course Level",
    ["All"] + sorted(courses["CourseLevel"].unique())
)
# -----------------------------
# Apply Filters
# -----------------------------
filtered_users = users.copy()
filtered_courses = courses.copy()
filtered_teachers = teachers.copy()
filtered_transactions = transactions.copy()

# Filter Users
if selected_age != "All":
    filtered_users = filtered_users[
        filtered_users["AgeGroup"] == selected_age
    ]

if selected_gender != "All":
    filtered_users = filtered_users[
        filtered_users["Gender"] == selected_gender
    ]

# Filter Courses
if selected_category != "All":
    filtered_courses = filtered_courses[
        filtered_courses["CourseCategory"] == selected_category
    ]

if selected_level != "All":
    filtered_courses = filtered_courses[
        filtered_courses["CourseLevel"] == selected_level
    ]
    # =====================================================
# 👥 Learner Demographics
# =====================================================
st.markdown("---")
st.header("👥 Learner Demographics")


# Charts Row 1
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Age Distribution")

    fig_age = px.histogram(
        filtered_users,
        x="Age",
        nbins=10,
        title="Age Distribution"
    )

    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.subheader("👨‍🎓 Gender Distribution")

    gender_count = filtered_users["Gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "Count"]

    fig_gender = px.pie(
        gender_count,
        names="Gender",
        values="Count",
        hole=0.4,
        title="Gender Distribution"
    )

    st.plotly_chart(fig_gender, use_container_width=True)
    # =====================================================
# 📚 Course Analysis
# =====================================================
st.markdown("---")
st.header("📚 Course Analysis")
   
# -----------------------------
# Course Category Popularity
# -----------------------------
st.header("📚 Course Category Popularity")

category_count = filtered_courses["CourseCategory"].value_counts().reset_index()
category_count.columns = ["CourseCategory", "Count"]

fig_category = px.bar(
    category_count,
    x="CourseCategory",
    y="Count",
    title="Course Categories",
    text_auto=True
)

st.plotly_chart(fig_category, use_container_width=True)
# -----------------------------
# Course Level Distribution
# -----------------------------
st.subheader("🎓 Course Level Distribution")

level_count = filtered_courses["CourseLevel"].value_counts().reset_index()
level_count.columns = ["CourseLevel", "Count"]

fig_level = px.pie(
    level_count,
    names="CourseLevel",
    values="Count",
    hole=0.4,
    title="Course Level Distribution"
)

st.plotly_chart(fig_level, use_container_width=True)
# =====================================================
# 💰 Enrollment & Revenue Analysis
# =====================================================
st.markdown("---")
st.header("💰 Enrollment & Revenue Analysis")
# -----------------------------
# Monthly Enrollment Trend
# -----------------------------
st.subheader("📈 Monthly Enrollment Trend")

monthly = (
    filtered_transactions
    .groupby("Month")
    .size()
    .reset_index(name="Enrollments")
)

fig_month = px.line(
    monthly,
    x="Month",
    y="Enrollments",
    markers=True,
    title="Monthly Enrollment Trend"
)

st.plotly_chart(fig_month, use_container_width=True)

# -----------------------------
# Revenue by Course Category
# -----------------------------
st.subheader("💰 Revenue by Course Category")

merged = filtered_transactions.merge(
    filtered_courses,
    on="CourseID"
)

revenue = (
    merged.groupby("CourseCategory")["Amount"]
    .sum()
    .reset_index()
)

fig_revenue = px.bar(
    revenue,
    x="CourseCategory",
    y="Amount",
    color="CourseCategory",
    text="Amount",
    title="Revenue by Course Category"
)

st.plotly_chart(fig_revenue, use_container_width=True)
# -----------------------------
# Top 10 Most Popular Courses
# -----------------------------
st.subheader("🏆 Top 10 Most Popular Courses")

course_popularity = (
    filtered_transactions.merge(filtered_courses, on="CourseID")
    .groupby("CourseName")
    .size()
    .reset_index(name="Enrollments")
    .sort_values(by="Enrollments", ascending=False)
    .head(10)
)

fig_top_courses = px.bar(
    course_popularity,
    x="Enrollments",
    y="CourseName",
    orientation="h",
    color="Enrollments",
    text="Enrollments",
    title="Top 10 Most Popular Courses"
)

fig_top_courses.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig_top_courses, use_container_width=True)
# =====================================================
# 👨‍🏫 Teacher Analysis
# =====================================================
st.markdown("---")
st.header("👨‍🏫 Teacher Analysis")

# -----------------------------
# Teacher Expertise Distribution
# -----------------------------
st.subheader("👨‍🏫 Teacher Expertise Distribution")

expertise = (
    filtered_teachers["Expertise"]
    .value_counts()
    .reset_index()
)

expertise.columns = ["Expertise", "Count"]

fig_expertise = px.bar(
    expertise,
    x="Expertise",
    y="Count",
    color="Expertise",
    text="Count",
    title="Teacher Expertise Distribution"
)

st.plotly_chart(fig_expertise, use_container_width=True)



# =====================================================
# 📊 Advanced Insights
# =====================================================
st.markdown("---")
st.header("📊 Advanced Insights")

# -----------------------------
# Age Group vs Course Category
# -----------------------------
merged_data = (
    filtered_transactions
    .merge(filtered_users[["UserID", "AgeGroup"]], on="UserID")
    .merge(filtered_courses[["CourseID", "CourseCategory"]], on="CourseID")
)

st.subheader("🔥 Age Group vs Course Category")

age_category = (
    merged_data
    .groupby(["AgeGroup", "CourseCategory"])
    .size()
    .reset_index(name="Enrollments")
)

fig_age_category = px.bar(
    age_category,
    x="AgeGroup",
    y="Enrollments",
    color="CourseCategory",
    barmode="group",
    title="Course Category Preference by Age Group"
)

st.plotly_chart(fig_age_category, use_container_width=True)
# -----------------------------
# Age Group vs Course Category
# -----------------------------

st.header("📊 Age Group vs Course Category")

# Join Users → Transactions → Courses
age_category = (
    filtered_transactions
    .merge(filtered_users[["UserID", "AgeGroup"]], on="UserID")
    .merge(filtered_courses[["CourseID", "CourseCategory"]], on="CourseID")
)

heatmap_data = (
    age_category
    .groupby(["AgeGroup", "CourseCategory"])
    .size()
    .reset_index(name="Enrollments")
)

fig_heatmap = px.density_heatmap(
    heatmap_data,
    x="CourseCategory",
    y="AgeGroup",
    z="Enrollments",
    color_continuous_scale="Blues",
    title="Age Group vs Course Category"
)

st.plotly_chart(fig_heatmap, use_container_width=True)


# -----------------------------
# Gender vs Course Level
# -----------------------------
st.header("👨‍🎓 Gender vs Course Level")

gender_level = (
    filtered_transactions
    .merge(filtered_users[["UserID", "Gender"]], on="UserID")
    .merge(filtered_courses[["CourseID", "CourseLevel"]], on="CourseID")
)

gender_level_data = (
    gender_level
    .groupby(["Gender", "CourseLevel"])
    .size()
    .reset_index(name="Enrollments")
)

fig_gender_level = px.bar(
    gender_level_data,
    x="CourseLevel",
    y="Enrollments",
    color="Gender",
    barmode="group",
    text="Enrollments",
    title="Gender vs Course Level"
)

st.plotly_chart(fig_gender_level, use_container_width=True)
# -----------------------------
# Revenue by Course Level
# -----------------------------
st.header("💰 Revenue by Course Level")

level_revenue = (
    filtered_transactions
    .merge(filtered_courses[["CourseID", "CourseLevel"]], on="CourseID")
)

level_revenue = (
    level_revenue
    .groupby("CourseLevel")["Amount"]
    .sum()
    .reset_index()
)

fig_level_revenue = px.bar(
    level_revenue,
    x="CourseLevel",
    y="Amount",
    color="CourseLevel",
    text="Amount",
    title="Revenue Generated by Course Level"
)

fig_level_revenue.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(fig_level_revenue, use_container_width=True)
# -----------------------------
# Top 10 Highest Revenue Courses
# -----------------------------
st.header("💸 Top 10 Highest Revenue Courses")

course_revenue = (
    filtered_transactions
    .merge(filtered_courses[["CourseID", "CourseName"]], on="CourseID")
    .groupby("CourseName")["Amount"]
    .sum()
    .reset_index()
    .sort_values(by="Amount", ascending=False)
    .head(10)
)

fig_course_revenue = px.bar(
    course_revenue,
    x="Amount",
    y="CourseName",
    orientation="h",
    color="Amount",
    text="Amount",
    title="Top 10 Highest Revenue Courses"
)

fig_course_revenue.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

fig_course_revenue.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig_course_revenue, use_container_width=True)



# -----------------------------
# Payment Method Distribution
# -----------------------------
st.header("💳 Payment Method Distribution")

payment = (
    filtered_transactions["PaymentMethod"]
    .value_counts()
    .reset_index()
)

payment.columns = ["PaymentMethod", "Count"]

fig_payment = px.pie(
    payment,
    names="PaymentMethod",
    values="Count",
    hole=0.4,
    title="Payment Method Distribution"
)

st.plotly_chart(fig_payment, use_container_width=True)

# =====================================================
# 📋 Data Explorer
# =====================================================
st.markdown("---")
st.header("📋 Data Explorer")

# -----------------------------
# Display Data
# -----------------------------
st.header("Users Table")
st.dataframe(
    filtered_users,
    use_container_width=True,
    hide_index=True
)

st.header("Courses Table")
st.dataframe(
    filtered_courses,
    use_container_width=True,
    hide_index=True
)

st.header("Teachers Table")
st.dataframe(
    filtered_teachers,
    use_container_width=True,
    hide_index=True
)

st.header("Transactions Table")
st.dataframe(
    filtered_transactions,
    use_container_width=True,
    hide_index=True
)
# -----------------------------
# Download Filtered Transactions
# -----------------------------
st.header("📥 Download Filtered Data")

csv = filtered_transactions.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Transactions CSV",
    data=csv,
    file_name="Eduvista_filtered_transactions.csv",
    mime="text/csv"
)
# -----------------------------
# Dashboard Footer
# -----------------------------
st.markdown("---")

st.markdown(
    """
    ### 📌 Project Information

    **Project:** Learner Demographics and Course Enrollment Behavior Analysis on Eduvista

    **Tools Used:**
    - MySQL
    - Python
    - Pandas
    - Streamlit
    - Plotly
    - VS Code

    **Developed By:** Tirumalakonda Bhanu Karthik
    """
)
st.markdown("---")

st.markdown(
    """
    <div style='text-align:center; color:gray; font-size:15px;'>
        <b>Eduvista Learner Demographics and Course Enrollment Behavior Analysis</b><br>
        Developed using <b>Python • Streamlit • MySQL • Plotly</b><br>
        © 2026
    </div>
    """,
    unsafe_allow_html=True
)


