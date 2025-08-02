import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(layout="wide", page_title="Electronics Sales Analysis")

st.title("📈 Electronics Sales Data Dashboard")
st.write("Analyzing customer purchase behavior and sales trends for ABC Manufacturing.")

# --- Define the path to your CSV file ---
# Make sure 'Electronic_sales_Sep2023-Sep2024.csv' is in the same directory as this Python script
CSV_FILE_PATH = 'Electronic_sales_Sep2023-Sep2024.csv'

try:
    # --- Load Data Directly ---
    df = pd.read_csv(CSV_FILE_PATH)
    st.success(f"File '{CSV_FILE_PATH}' loaded successfully!")

    # --- Data Preprocessing (as per P7 design) ---
    st.sidebar.header("Data Preprocessing Status:")
    initial_rows = df.shape[0]
    st.sidebar.write(f"- Initial rows: {initial_rows}")

    df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
    df['Add-ons Purchased'] = df['Add-ons Purchased'].fillna('None')
    df['Add-on Total'] = df['Add-on Total'].fillna(0)
    
    critical_missing_before = df[['Age', 'Gender', 'Loyalty Member', 'Payment Method']].isnull().sum().sum()
    df.dropna(subset=['Age', 'Gender', 'Loyalty Member', 'Payment Method'], inplace=True)
    if critical_missing_before > 0:
        st.sidebar.write(f"- Dropped rows with missing critical info: {critical_missing_before}")

    df.drop_duplicates(inplace=True)
    st.sidebar.write(f"- Removed duplicates. Remaining rows: {df.shape[0]}")

    df_completed_sales = df[df['Order Status'] == 'Completed'].copy()
    st.sidebar.write(f"- Filtered for 'Completed' orders. Rows for analysis: {df_completed_sales.shape[0]}")

    df_completed_sales['Loyalty Member'] = df_completed_sales['Loyalty Member'].map({'Yes': 1, 'No': 0})
    df_completed_sales['Promotion_Flag'] = df_completed_sales['Promotion_Flag'].fillna('No').map({'Yes': 1, 'No': 0})
    st.sidebar.write("- Preprocessing completed!")

    st.subheader("Raw Data Preview (Completed Orders Only)")
    st.dataframe(df_completed_sales.head())

    # --- Feature Engineering (for aggregated data for specific charts) ---
    df_completed_sales['Year'] = df_completed_sales['Purchase Date'].dt.year
    df_completed_sales['Month'] = df_completed_sales['Purchase Date'].dt.month
    df_completed_sales['Day'] = df_completed_sales['Purchase Date'].dt.day
    df_completed_sales['DayOfWeek'] = df_completed_sales['Purchase Date'].dt.dayofweek
    df_completed_sales['Quarter'] = df_completed_sales['Purchase Date'].dt.quarter
    df_completed_sales['WeekOfYear'] = df_completed_sales['Purchase Date'].dt.isocalendar().week.astype(int)

    # Aggregate daily sales for overall trend
    daily_sales = df_completed_sales.groupby('Purchase Date')['Quantity'].sum().reset_index()


    # --- Interactive Charts ---
    st.header("Sales Performance Visualizations")

    # Chart 1: Total Quantity Sold Over Time (Daily)
    st.subheader("1. Daily Total Quantity Sold Over Time")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(daily_sales['Purchase Date'], daily_sales['Quantity'], label='Daily Total Quantity Sold', color='skyblue')
    ax1.set_title('Total Quantity Sold Over Time (Daily)')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Quantity Sold')
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Chart 2: Total Quantity Sold by Product Type
    st.subheader("2. Total Quantity Sold by Product Type")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_completed_sales, x='Product Type', y='Quantity', estimator=sum, ci=None, palette='viridis', ax=ax2)
    ax2.set_title('Total Quantity Sold by Product Type')
    ax2.set_xlabel('Product Type')
    ax2.set_ylabel('Total Quantity Sold')
    st.pyplot(fig2)

    # Chart 3: Monthly Sales Seasonality
    st.subheader("3. Monthly Sales Seasonality")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    monthly_sales = df_completed_sales.groupby('Month')['Quantity'].sum().reset_index()
    sns.barplot(data=monthly_sales, x='Month', y='Quantity', palette='magma', ax=ax3)
    ax3.set_title('Total Quantity Sold by Month (Seasonality)')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Total Quantity Sold')
    st.pyplot(fig3)

    # Chart 5: Customer Age Distribution and its relation to Quantity Sold
    st.subheader("5. Customer Age Distribution and Sales Relationship")
    col1, col2 = st.columns(2) # Use columns for side-by-side plots

    with col1:
        fig5a, ax5a = plt.subplots(figsize=(7, 5))
        sns.histplot(df_completed_sales['Age'], bins=20, kde=True, color='green', ax=ax5a)
        ax5a.set_title('Distribution of Customer Age')
        ax5a.set_xlabel('Age')
        ax5a.set_ylabel('Count')
        st.pyplot(fig5a)

    with col2:
        fig5b, ax5b = plt.subplots(figsize=(7, 5))
        sns.scatterplot(data=df_completed_sales, x='Age', y='Quantity', alpha=0.5, hue='Product Type', palette='tab10', ax=ax5b)
        ax5b.set_title('Quantity Sold vs. Customer Age by Product Type')
        ax5b.set_xlabel('Age')
        ax5b.set_ylabel('Quantity Sold per Transaction')
        st.pyplot(fig5b)
    
    # Chart 6: Distribution of Product Ratings
    st.subheader("6. Distribution of Product Ratings")
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df_completed_sales, x='Rating', palette='rocket', ax=ax6)
    ax6.set_title('Distribution of Product Ratings (1-5 Stars)')
    ax6.set_xlabel('Rating')
    ax6.set_ylabel('Number of Ratings')
    st.pyplot(fig6)


except FileNotFoundError:
    st.error(f"Error: The file '{CSV_FILE_PATH}' was not found. Please make sure the CSV file is in the same directory as this Python script.")
    st.info("You can also upload a CSV file if you prefer, by uncommenting the `st.sidebar.file_uploader` line and commenting out the `CSV_FILE_PATH` line.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.info("Please check the CSV file format and column names.")


# --- Footer ---
st.markdown("---")
st.markdown("Developed for Data Science Solution Assignment. Data preprocessing and visualizations based on P7 design.")
