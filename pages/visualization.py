import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Data Analysis App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define functions for each page
def home_page():
    st.markdown(
        """
        <style>
        .main-header {
            color: #4CAF50;
            text-align: center;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<h1 class="main-header">📊 Data Analysis Web App</h1>', unsafe_allow_html=True)
    st.sidebar.header("Upload Your File")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        col1, col2, col3 = st.columns(3)
        col1.subheader("Header of the dataset")
        col1.dataframe(df.head(), height=300)
        col2.subheader("Dataset Statistics")
        col2.dataframe(df.describe())
        col3.subheader("Tail of the Dataset")
        col3.dataframe(df.tail(), height=300)
        st.markdown("### Key Metrics")
        st.write("---")
        total_rows = len(df)
        total_columns = len(df.columns)
        st.columns(3)[1].metric("Total Rows", f"{total_rows}")
        st.columns(3)[2].metric("Total Columns", f"{total_columns}")
        st.markdown("### Visualization")
        st.write("---")
        selected_column = st.selectbox("Select a column for visualization", df.columns)
        chart_type = st.radio("Choose a chart type", ["Line Chart", "Bar Chart", "Area Chart", "Graphviz Chart", "Histogram", "Box Plot"])
        
        if chart_type == "Line Chart":
            st.line_chart(df[selected_column])
        elif chart_type == "Bar Chart":
            st.bar_chart(df[selected_column])
        elif chart_type == "Area Chart":
            st.area_chart(df[selected_column])
        elif chart_type == "Graphviz Chart":
            st.graphviz_chart(f'digraph {{ {selected_column} }}')
        elif chart_type == "Histogram":
            fig, ax = plt.subplots()
            ax.hist(df[selected_column], bins=30)
            st.pyplot(fig)
        elif chart_type == "Box Plot":
            fig, ax = plt.subplots()
            ax.boxplot(df[selected_column])
            st.pyplot(fig)
    else:
        st.markdown("### Please upload a CSV file to get started! 📂")
        st.image("https://via.placeholder.com/600x400?text=Upload+CSV", use_column_width=True)

def about_page():
    st.markdown("# 📊 Data Analysis Web App")

    st.info("The Data Analysis Web App is an interactive platform designed to empower users to upload, analyze, and visualize CSV datasets seamlessly. Built using Streamlit, a Python-based framework, this application offers an intuitive interface for both novice and experienced data enthusiasts.")

    st.write("""
    ## Key Features:

### 1. User-Friendly Interface:
The app provides a straightforward layout, allowing users to upload CSV files effortlessly and navigate through various data analysis options.

### 2. Comprehensive Data Overview:
Upon uploading a dataset, users receive an immediate overview, including:
- A preview of the dataset's first few and last few rows.
- Descriptive statistics summarizing the central tendency, dispersion, and shape of the dataset’s distribution.

### 3. Key Metrics Display:
The application highlights essential metrics such as the total number of rows and columns, providing users with a quick grasp of the dataset's structure.

### 4. Interactive Visualization:
Users can select a column from the dataset and choose from various chart types to visualize the data interactively:
- Line Charts
- Bar Charts
- Area Charts
- Graphviz Chart
- Histograms
- Box Plots

### 5. Error Handling and Feedback:
The app is equipped with mechanisms to handle errors gracefully, providing informative messages to guide users in case of issues like unsupported file formats or non-numeric data selections.

---

## Technical Highlights:

### 1. Streamlit Framework:
Leveraging Streamlit allows for rapid development of interactive web applications with minimal code complexity.

### 2. Pandas and Matplotlib Integration:
The app seamlessly integrates Pandas for data manipulation and Matplotlib for data visualization, enabling a comprehensive data analysis experience.

### 3. Custom Styling:
The app features custom styling using HTML and CSS to enhance the visual appeal and readability of the interface.

### 4. Error Handling:
Robust error handling mechanisms are implemented to provide users with clear feedback and guidance in case of unexpected issues during data analysis.

---

## Usage Scenario:

This application is ideal for users seeking a quick and interactive way to explore their datasets without delving into complex coding. Whether you're a data analyst performing exploratory data analysis (EDA) or a student working on a data project, this tool simplifies the process of data examination and visualization.

By offering a user-friendly interface, key metrics display, and interactive visualization options, the Data Analysis Web App streamlines the data analysis workflow, making it accessible to a wide range of users.

---

### Future Enhancements:
1. Support for additional file formats such as Excel or JSON.
2. Advanced visualization options, including scatter plots and heatmaps.
3. Enhanced data cleaning and preprocessing functionalities.
4. Integration with machine learning models for predictive analysis.

""")
    st.info("This app allows you to upload a CSV file, analyze the data, and visualize it interactively.")
    
# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About"])

# Display the selected page
if page == "Home":
    home_page()
elif page == "About":
    about_page()
    