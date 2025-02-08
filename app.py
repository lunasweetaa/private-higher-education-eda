import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Exploring Accreditation Patterns and Student Distribution in Indonesian Private Universities", layout="wide")

# Title of the app
st.title("Exploring Accreditation Patterns and Student Distribution in Indonesian Private Universities")
# 1. Upload the Dataset
import pandas as pd
import streamlit as st

st.header("Step 1: Upload Dataset")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Show the initial preview of the dataset
    st.subheader("Dataset Preview")
    st.write(df.head())
# 2. Handling Missing Data
st.header("Step 2: Handling Missing Data")

# Ensure the dataset is loaded before processing
if 'df' in locals():
    # Show missing data counts for each column
    missing_data = df.isnull().sum()
    st.write("Missing data per column:")
    st.write(missing_data)

    # Convert columns to numeric (if applicable)
    df['Student'] = pd.to_numeric(df['Student'], errors='coerce')
    df['Lecture'] = pd.to_numeric(df['Lecture'], errors='coerce')

    # Choose how to handle missing data
    fill_missing = st.radio("Choose an option for missing data", ("Fill with Median", "Fill with Mode", "Remove Rows"))

    if fill_missing == "Fill with Median":
        # Fill missing data with median for numerical columns
        df['Student'] = df['Student'].fillna(df['Student'].median())
        df['Lecture'] = df['Lecture'].fillna(df['Lecture'].median())
        st.write("Missing data in 'Student' and 'Lecture' columns have been filled with median values.")

    elif fill_missing == "Fill with Mode":
        # Fill missing data with mode for categorical columns
        if 'Accreditation' in df.columns:
            df['Accreditation'] = df['Accreditation'].fillna(df['Accreditation'].mode()[0])
        st.write("Missing data in 'Accreditation' column has been filled with mode.")

    else:
        # Remove rows with missing data
        rows_removed = df.dropna()
        st.write(f"{missing_data.sum()} rows with missing data have been removed.")
        df = rows_removed

    # Show the preview after handling missing data
    st.subheader("Preview After Handling Missing Data")
    st.write(df.head())
else:
    st.write("Please upload a dataset first.")
# 3. Removing Duplicates
st.header("Step 3: Remove Duplicates")
if st.button("Remove Duplicates"):
    before_drop = df.shape[0]
    df = df.drop_duplicates()
    after_drop = df.shape[0]
    st.write(f"Number of duplicate rows removed: {before_drop - after_drop} rows.")

st.subheader("Preview After Removing Duplicates")
st.write(df.head())
# 4. Handling Categorical Data
st.header("Step 4: Handling Categorical Data")
df['Accreditation'] = df['Accreditation'].str.strip()  # Remove extra spaces
df['Accreditation'] = df['Accreditation'].replace({
    'Unggul': 'Excellence',
    'Baik Sekali': 'Best',
    'Baik': 'Good',
    'Tidak Terakreditasi': 'Not Accredited',
    'Pembinaan': 'Worst',
    'Coming Soon': 'Temporary Accreditation'
})
st.write("The 'Accreditation' column has been standardized.")

st.subheader("Preview After Standardizing Categorical Data")
st.write(df.head())
# 5. Save the Cleaned Dataset
st.header("Step 5: Save the Cleaned Dataset")
st.write("After cleaning the data, you can download the processed CSV file.")
cleaned_data_file = "private_higher_education_indonesia_cleaned.csv"
df.to_csv(cleaned_data_file, index=False)
st.download_button("Download Cleaned Dataset", cleaned_data_file)
# 6. Data Visualization
st.header("Step 6: Data Visualization")

# Visualization for Missing Data
st.subheader("Missing Data Visualization")
missing_data_percent = (missing_data / df.shape[0]) * 100
missing_data_percent = missing_data_percent[missing_data_percent > 0]
st.bar_chart(missing_data_percent)

# Visualization for Accreditation
st.subheader("Accreditation Distribution")
accreditation_counts = df['Accreditation'].value_counts()
st.bar_chart(accreditation_counts)

# Visualization for Student Categories
st.subheader("Student Category Distribution")
category_student_counts = df['Category_Total_Student'].value_counts()
st.bar_chart(category_student_counts)

# Visualization for University Distribution by Province
st.subheader("University Distribution by Province")
province_counts = df['Province'].value_counts()
st.bar_chart(province_counts)
