Here’s a detailed README.md version for your project:


---

📊 Student Habits vs Academic Performance Dashboard

📌 Overview

This project is an interactive Streamlit dashboard designed to explore the relationship between student lifestyle habits and academic performance. It combines data preprocessing, cleaning, and visualization to provide meaningful insights into how various habits affect exam scores.

The dashboard allows users to:

Filter by gender and part-time job status

View Key Performance Indicators (KPIs)

Explore interactive visualizations on study hours, sleep patterns, diet, social media use, attendance, and extracurricular activities



---

🛠 Features

Data Cleaning & Preprocessing

Standardized categorical values

Handled missing data (mean for numerical, placeholders for categorical)

Corrected unrealistic values (e.g., negative hours, out-of-range percentages)

Random assignment of gender where marked as "Other" for balance


Interactive Filters

Gender filter

Part-time job status filter


KPIs

Total Students

Average Final Exam Score

Average Sleep Hours

Average Study Hours


Visualizations (via Plotly)

1. Age Distribution by Gender


2. Study Hours vs Exam Score


3. Social Media Hours vs Exam Score


4. Attendance % vs Exam Score


5. Diet Quality vs Exam Score (Boxplot)


6. Average Exam Score by Exercise Frequency


7. Extracurricular Participation vs Exam Score


8. Sleep Hours vs Exam Score





---

📂 Technologies Used

Python – Data manipulation & analysis

Pandas & NumPy – Data cleaning & preprocessing

Matplotlib & Seaborn – Additional data visualization

Plotly Express – Interactive charts

Streamlit – Web app framework



---

🚀 How to Run

1. Clone the repository

git clone https://github.com/Shift-Adham/Habits_Performance.git
cd Habits_Performance


2. Install dependencies

pip install -r requirements.txt


3. Run the app

streamlit run app.py


4. Access the dashboard
Open your browser and go to:

http://localhost:8501



---

📊 Dataset

The dataset contains information on:

Demographics: Age, gender, student ID

Habits: Study hours, sleep hours, exercise frequency, diet quality, social media hours, extracurricular activities

Performance: Exam scores, attendance percentage

Other factors: Part-time job status, mental health rating


---

📌 Insights You Can Gain

How study time correlates with academic performance

The impact of sleep and exercise on exam scores

Whether social media usage affects performance

The role of diet quality and extracurriculars in student success


---


📜 License

This project is licensed under the MIT License – feel free to use and modify it.
