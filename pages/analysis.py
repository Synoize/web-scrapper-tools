import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dataset Analysis App")

# Sidebar for file upload
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

def home_page():
 if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

        # Display the dataset
        st.subheader("Dataset Preview")
        st.write(df.head())

        # Dataset information
        st.subheader("Dataset Information")
        st.write("Shape of dataset:", df.shape)
        st.write("Columns:", df.columns.tolist())
        st.write("Missing values:")
        st.write(df.isnull().sum())
        st.write("Data types:")
        st.write(df.dtypes)

        # Summary statistics
        st.subheader("Summary Statistics")
        st.write(df.describe())

        # Data visualization options
        st.sidebar.header("Visualization")
        if st.sidebar.checkbox("Show correlation heatmap"):
            st.subheader("Correlation Heatmap")
            plt.figure(figsize=(10, 6))
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
            st.pyplot(plt)

        if st.sidebar.checkbox("Show column distributions"):
            st.subheader("Column Distributions")
            selected_column = st.sidebar.selectbox("Select a column", df.select_dtypes(include=np.number).columns)
            plt.figure(figsize=(8, 4))
            sns.histplot(df[selected_column], kde=True, bins=30)
            plt.title(f"Distribution of {selected_column}")
            st.pyplot(plt)

        # Interactive data filtering
        st.sidebar.header("Filter Data")
        filter_column = st.sidebar.selectbox("Select a column for filtering", df.columns)
        unique_values = df[filter_column].unique()
        filter_value = st.sidebar.selectbox("Select a value", unique_values)
        filtered_df = df[df[filter_column] == filter_value]
        st.subheader(f"Filtered Data ({filter_column} = {filter_value})")
        st.write(filtered_df)

        # Advanced analyses
        st.sidebar.header("Advanced Analysis")

        # Pairplot
        if st.sidebar.checkbox("Show pairplot"):
            st.subheader("Pairplot")
            st.text("Visualizing relationships between numerical columns")
            selected_columns = st.sidebar.multiselect("Select columns for pairplot", df.select_dtypes(include=np.number).columns, default=df.select_dtypes(include=np.number).columns[:2])
            if len(selected_columns) > 1:
                sns.pairplot(df[selected_columns])
                st.pyplot(plt)
            else:
                st.warning("Please select at least two columns for the pairplot.")

        # Outlier detection
        if st.sidebar.checkbox("Detect Outliers"):
            st.subheader("Outlier Detection")
            numeric_columns = df.select_dtypes(include=np.number).columns
            outlier_column = st.selectbox("Select a column for outlier detection", numeric_columns)
            Q1 = df[outlier_column].quantile(0.25)
            Q3 = df[outlier_column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[outlier_column] < lower_bound) | (df[outlier_column] > upper_bound)]
            st.write(f"Number of outliers in {outlier_column}: {len(outliers)}")
            st.write(outliers)

        # Custom aggregation
        if st.sidebar.checkbox("Custom Aggregation"):
            st.subheader("Custom Aggregation")
            agg_column = st.selectbox("Select a column for aggregation", df.columns)
            agg_function = st.selectbox("Select an aggregation function", ["mean", "sum", "count", "min", "max"])
            grouped = df.groupby(agg_column).agg({agg_column: agg_function})
            st.write(grouped)

    except Exception as e:
        st.error(f"Error: {e}")
 else:
     st.info("Please upload a CSV file to get started.")

def about_page():
    st.info("The **Dataset Analysis App** is a Streamlit-based interactive web application that allows users to upload and analyze datasets in CSV format. It provides comprehensive insights into the dataset, including statistical summaries, visualizations, and advanced analytical tools.")
    st.write("""
## Features

### 1. **File Upload**
- Users can upload datasets in CSV format via the sidebar.

### 2. **Dataset Preview**
- Display the first few rows of the dataset for a quick overview.

### 3. **Dataset Information**
- Shape of the dataset (rows and columns).
- List of column names.
- Missing values in each column.
- Data types of each column.

### 4. **Summary Statistics**
- Statistical summaries (e.g., mean, median, standard deviation) for numerical columns.

### 5. **Visualization Options**
- **Correlation Heatmap**: Visualize correlations between numerical columns.
- **Column Distributions**: View histograms with optional KDE (Kernel Density Estimation) for selected numerical columns.

### 6. **Interactive Data Filtering**
- Filter data based on unique values in a selected column.

### 7. **Advanced Analyses**
- **Pairplot**: Visualize relationships between selected numerical columns.
- **Outlier Detection**: Identify and display rows with outlier values in numerical columns.
- **Custom Aggregation**: Perform aggregation operations (mean, sum, count, min, max) on grouped data.

---

## How to Use
1. **Upload a File**: Use the sidebar to upload a CSV file.
2. **Explore the Dataset**: View dataset preview, shape, column information, and missing values.
3. **Visualize Data**: Use the sidebar to select visualizations and specify parameters.
4. **Perform Analysis**: Utilize tools like outlier detection, pairplot visualization, and custom aggregation to analyze the dataset.

---

## Technologies Used
- **Streamlit**: For building the interactive user interface.
- **Pandas**: For data manipulation and analysis.
- **Seaborn**: For advanced data visualization.
- **Matplotlib**: For rendering plots.

---

## Future Enhancements
- Add support for Excel and JSON file uploads.
- Incorporate machine learning model training and evaluation.
- Provide downloadable reports for analyses.


""")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About"])

# Display the selected page
if page == "Home":
    home_page()
elif page == "About":
    about_page()
    