import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# File path
file_path = "County Data 2.xlsx"

# Load data
try:
    df = pd.read_excel(file_path)
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading the file: {e}")

# Rename 'Row Labels' to 'County'
df = df.rename(columns={'Row Labels': 'County'})

# Create new features / columns
# Total Population
if {'Male', 'Female', 'Intersex'}.issubset(df.columns):
    df['Total_Population'] = df['Male'] + df['Female'] + df['Intersex']

# Create the Density column: Total_Population divided by Land Area
df['Density'] = df['Total_Population'] / df['Land Area']

# Create the Family_Size column: Total_Population divided by Total Households
df['Family_Size'] = df['Total_Population'] / df['Total Households']

# Creation of Kenya, sum of the counties and average for financial health %
columns_to_sum = df.columns.drop("Financial_Health")
kenya_totals = df[columns_to_sum].sum(numeric_only=True)
financial_health_avg = df["Financial_Health"].mean()
kenya_totals["Financial_Health"] = financial_health_avg

# Calculate Family Size for Kenya (Total_Population / Total Households)
kenya_totals['Family_Size'] = kenya_totals['Total_Population'] / kenya_totals['Total Households']

# Add the calculated summary for Kenya
kenya_df = pd.DataFrame(kenya_totals).transpose()
kenya_df.insert(0, df.columns[0], "Kenya")
df = pd.concat([df, kenya_df], ignore_index=True)

# Remove Kenya row from the DataFrame for visualizations
df_without_kenya = df[df['County'] != 'Kenya']

# Summary statistics for Kenya (to be shown in the left pane)
kenya_summary = kenya_df[['County', 'Total_Population', 'Land Area', 'Density', 'Family_Size', 'GDP_Mkes', 'Primary_School', 'Secondary_School', 'Financial_Health']]

# Round the summary statistics for Kenya to 1 decimal place
kenya_summary = kenya_summary.round(1)

# Set up Streamlit app layout
st.set_page_config(layout="wide")

# Sidebar for menu options (left pane)
with st.sidebar:
    st.header("Select Options")
    
    # Display Kenyan Flag
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/2560px-Flag_of_Kenya.svg.png", width=120)  # Kenyan Flag
    
    # Checkbox to show Kenya summary statistics
    show_kenya = st.checkbox("Show Summary Statistics for Kenya")
    
    # Dropdown for KPI selection
    kpi_selection = st.selectbox("Select KPI to view", 
                                 ['Total_Population', 'Density', 'Family_Size', 'GDP_Mkes', 
                                  'Primary_School', 'Secondary_School', 'Financial_Health'])
    
    # Dropdown for counties to compare
    selected_counties = st.multiselect("Select up to 5 counties to compare", 
                                       df_without_kenya['County'].unique(), max_selections=5)
    
    # Show summary checkbox moved to sidebar
    show_kpi_summary = st.checkbox("Show Summary of KPIs by County", value=False)

# Function to display summary statistics for Kenya
def display_kenya_summary():
    st.subheader("Summary Statistics for Kenya")
    st.write(kenya_summary)

# Function to plot selected KPI by county
def plot_kpi(kpi_column):
    st.subheader(f"{kpi_column} by County")
    # Sort the data by the selected KPI in descending order
    sorted_df = df_without_kenya.sort_values(by=kpi_column, ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='County', y=kpi_column, data=sorted_df, ax=ax, palette='viridis')
    ax.set_title(f'{kpi_column} by County', fontsize=16, color='darkblue')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

# Function to compare selected counties for a specific KPI
def compare_counties(kpi_column, counties):
    st.subheader(f"Comparison of {kpi_column} between Counties")
    filtered_df = df_without_kenya[df_without_kenya['County'].isin(counties)]
    # Sort the data by the selected KPI in descending order
    sorted_filtered_df = filtered_df.sort_values(by=kpi_column, ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='County', y=kpi_column, data=sorted_filtered_df, ax=ax, palette='coolwarm')
    ax.set_title(f'Comparison of {kpi_column} for Selected Counties', fontsize=16, color='darkgreen')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

# Function to display summary KPIs by county
def display_summary_kpis():
    st.subheader("County KPI Summary")
    kpis = ['Total_Population', 'Density', 'Family_Size', 'GDP_Mkes', 'Primary_School', 'Secondary_School', 'Financial_Health']
    for kpi in kpis:
        plot_kpi(kpi)

# Function to give insights based on selected KPI
def display_kpi_insights(kpi_column):
    st.subheader(f"Insights on {kpi_column}")
    
    if kpi_column == "Total_Population":
        st.write("Total Population gives an indication of how many people reside in a given county. Larger populations may indicate more significant resource demands, infrastructure needs, and potential markets for goods and services.")
    
    elif kpi_column == "Density":
        st.write("Population density provides a measure of how crowded a county is. Higher density might indicate urbanized areas with better access to services but might also highlight challenges such as congestion and pollution.")
    
    elif kpi_column == "Family_Size":
        st.write("Family size indicates the average number of people in a household. A large average family size could suggest social or economic factors affecting household configurations, such as lower levels of education or limited access to family planning services.")
    
    elif kpi_column == "GDP_Mkes":
        st.write("GDP (Gross Domestic Product) is an essential indicator of a county's economic performance. Higher GDP reflects a wealthier county, while lower GDP suggests economic challenges.")
    
    elif kpi_column == "Primary_School":
        st.write("The primary school enrollment rate gives an idea of the accessibility of education for young children. Higher rates may reflect better educational infrastructure and greater societal emphasis on education.")
    
    elif kpi_column == "Secondary_School":
        st.write("The secondary school enrollment rate reflects the ability of young people to continue their education beyond primary school. A higher rate may indicate better access to educational facilities and opportunities.")
    
    elif kpi_column == "Financial_Health":
        st.write("Financial health is a crucial metric indicating the domestic financial health of persons in a county as a percentage of its population. Higher financial health indicates better access to employment and economic activities, while lower scores may suggest financial challenges.")

# Main content of the app
st.title("Kenya County Data Analysis")
st.write("A Data Analysis Project by Vincent Kemboi x Africa Data School, 2024")

# Display summary statistics for Kenya based on the checkbox
if show_kenya:
    display_kenya_summary()

# Show the selected KPI's visualization
if selected_counties:
    compare_counties(kpi_selection, selected_counties)
else:
    plot_kpi(kpi_selection)

# Optionally, show a summary of all KPIs
if show_kpi_summary:
    display_summary_kpis()

# Display insights based on the selected KPI
display_kpi_insights(kpi_selection)
