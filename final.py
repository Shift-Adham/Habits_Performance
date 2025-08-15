import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
#load data
df = pd.read_csv('student_habits_performance.csv')

print(df.describe())

# data preprocessing
# Find rows where gender is 'Other'
mask_other = df['gender'].str.lower() == 'other'

# Randomly assign Male/Female to those rows
np.random.seed(42)  # for reproducibility
df.loc[mask_other, 'gender'] = np.random.choice(['Male', 'Female'], size=mask_other.sum())


#cleaing data
# 1. Strip whitespace from column names
df.columns = df.columns.str.strip()

# 2. Standardize categorical text case (title case for categories, upper case for IDs)
df['student_id'] = df['student_id'].str.strip().str.upper()
categorical_cols = df.select_dtypes(include='object').columns.drop('student_id')

for col in categorical_cols:
    df[col] = df[col].str.strip().str.title()

# 3. Handle potential impossible values:
# Ensure numerical values are within realistic bounds (clip but not remove)
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_cols:
    if col == 'age':
        df[col] = df[col].clip(lower=0)  # Age can't be negative
    elif col.endswith('_hours'):
        df[col] = df[col].clip(lower=0)  # Hours can't be negative
    elif col.endswith('_percentage'):
        df[col] = df[col].clip(lower=0, upper=100)  # Percentages 0-100
    elif col == 'mental_health_rating':
        df[col] = df[col].clip(lower=1, upper=10)  # Ratings 1-10

# 4. Fill missing values (if any) with placeholders / averages to preserve all rows
for col in df.columns:
    if df[col].isnull().sum() > 0:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(df[col].mean())  # numerical mean
        else:
            df[col] = df[col].fillna('Unknown')       # categorical placeholder


# Verify cleaning result
#print(df.isnull().sum())
#print(df.head())

# Check result
#print(df['gender'].value_counts())

# --- Streamlit Dashboard ---

# Set page config
st.set_page_config(page_title="Student Habit vs Academic Performance", layout="wide")

# Title
st.title("Student Habit vs Academic Performance")

# Optional: Add an image (replace 'header.jpg' with your image filename)
st.image("download.png", caption="Exploring how student habits impact academic performance")
# Sidebar for filters
st.sidebar.header("Filters")
# Gender filter
gender_options = df['gender'].unique().tolist()
selected_gender = st.sidebar.multiselect("Select Gender", options=gender_options, default=gender_options)

# Part-time filter (assuming column is named 'part_time' and values like 'Yes'/'No')
if 'part_time_job' in df.columns:
    part_time_options = df['part_time_job'].unique().tolist()
    selected_part_time = st.sidebar.multiselect("Select Part-Time Status", options=part_time_options, default=part_time_options)
    filtered_df = df[(df['gender'].isin(selected_gender)) & (df['part_time_job'].isin(selected_part_time))]
else:
    filtered_df = df[df['gender'].isin(selected_gender)]

# --- KPIs Section ---
st.markdown("### Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", len(filtered_df))

with col2:
    avg_score = filtered_df['exam_score'].mean() if 'exam_score' in filtered_df.columns else np.nan
    st.metric("Avg. Final Score (%)", f"{avg_score:.1f}" if not np.isnan(avg_score) else "N/A")

with col3:
    avg_sleep = filtered_df['sleep_hours'].mean() if 'sleep_hours' in filtered_df.columns else np.nan
    st.metric("Avg. Sleep Hours", f"{avg_sleep:.1f}" if not np.isnan(avg_sleep) else "N/A")

with col4:
    avg_study = filtered_df['study_hours'].mean() if 'study_hours' in filtered_df.columns else np.nan
    st.metric("Avg. Study Hours", f"{avg_study:.1f}" if not np.isnan(avg_study) else "N/A")

# --- Visualizations Section ---
st.markdown("### Visualizations")

# 1. Age Distribution
st.subheader("Age Distribution")
fig_age = px.histogram(filtered_df, x="age", nbins=8, color="gender", barmode="group",
                       title="Age Distribution by Gender")
st.plotly_chart(fig_age, use_container_width=True)

# 2. Study Hours vs Exam Score
st.subheader("Study Hours vs Exam Score")
fig_study = px.scatter(filtered_df, x="study_hours_per_day", y="exam_score",
                       color="gender", size="attendance_percentage", hover_data=["sleep_hours"],
                       title="Study Hours vs Exam Score")
st.plotly_chart(fig_study, use_container_width=True)

# 3. Social Media Hours vs Exam Score
st.subheader("Social Media Hours vs Exam Score")
fig_social = px.scatter(filtered_df, x="social_media_hours", y="exam_score",
                        color="gender", 
                        title="Social Media Hours vs Exam Score")
st.plotly_chart(fig_social, use_container_width=True)

# 4. Attendance % vs Exam Score
st.subheader("Attendance % vs Exam Score")
fig_attendance = px.scatter(filtered_df, x="attendance_percentage", y="exam_score",
                            color="gender", 
                            title="Attendance % vs Exam Score")
st.plotly_chart(fig_attendance, use_container_width=True)

# 5. Diet Quality vs Exam Score (Boxplot)
st.subheader("Diet Quality vs Exam Score")
fig_diet = px.box(filtered_df, x="diet_quality", y="exam_score", color="diet_quality",
                  title="Exam Score by Diet Quality")
st.plotly_chart(fig_diet, use_container_width=True)

# 6. Average Exam Score by Exercise Frequency
st.subheader("Average Exam Score by Exercise Frequency")

# Calculate average exam score for each exercise frequency
avg_exercise_freq = filtered_df.groupby("exercise_frequency", as_index=False)["exam_score"].mean()

fig_exercise_freq = px.bar(avg_exercise_freq,
                           x="exercise_frequency",
                           y="exam_score",
                           color="exercise_frequency",
                           title="Average Exam Score by Exercise Frequency")

st.plotly_chart(fig_exercise_freq, use_container_width=True)


# 7. Extracurricular Participation vs Exam Score
st.subheader("Extracurricular Participation vs Exam Score")
fig_extra = px.box(filtered_df, x="extracurricular_participation", y="exam_score",
                   color="extracurricular_participation",
                   title="Exam Score by Extracurricular Participation")
st.plotly_chart(fig_extra, use_container_width=True)

# 8. Sleep Hours vs Exam Score
st.subheader("Sleep Hours vs Exam Score")
fig_sleep = px.scatter(filtered_df, 
                       x="sleep_hours", 
                       y="exam_score", 
                       color="gender",
                       title="Sleep Hours vs Exam Score")
st.plotly_chart(fig_sleep, use_container_width=True)
