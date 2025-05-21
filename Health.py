import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

# Set up connection to MySQL database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='paul',
    database='nutrition_paradox',
)

def run_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(result, columns=columns)

# Streamlit app UI
st.set_page_config(page_title="Nutrition 🍽️ Paradox Dashboard📊", layout="wide")
st.title("Nutrition 🍽️ Paradox Dashboard📊")
st.markdown('<h3 style="color: #007a5e;"> Compare Global Obesity and Malnutrition Statistics ⚖️</h3>', unsafe_allow_html=True)

from streamlit_option_menu import option_menu

# Sidebar for choosing between queries
with st.sidebar:
    selected = option_menu(
        "🔍 Global Health Insights by Query",  # Title
        ["Obesity", "Malnutrition", "Combined"],  # Menu options
        icons=["heartbeat", "leaf", "balance-scale"],  # Icons (FontAwesome)
        menu_icon="stethoscope",  # Sidebar Icon
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#eafaf1"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#c3f0db",
            },
            "nav-link-selected": {"background-color": "#2a9d8f", "color": "white"},
        }
    )

# Background and app box styling
st.markdown("""
    <style>
    /* PAGE BACKGROUND - Dark Orange to Golden Yellow Gradient */
    body {
        background: linear-gradient(135deg, #56ab2f, #00b4db);
        background-attachment: fixed;
        background-size: cover;
    }

    /* MAIN APP BOX - Pure White */
    .stApp {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        margin: 2% auto;
        width: 95%;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Dropdown menu for selecting a query

# Obesity Queries section
if selected == "Obesity":
    option = st.selectbox(
        'Select a query to display:', ["Top 5 regions with the highest average obesity levels in the most recent year(2022)", 
                                       "Top 5 countries with highest obesity estimates", 
                                       "Obesity trend in India over the years(Mean_estimate)", 
                                       "Average obesity by gender", 
                                       "Country count by obesity level category and age group", 
                                       "Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)",
                                       "Average obesity by age group",
                                       "Top 10 Countries with consistent low obesity (low average + low CI)over the years",
                                       "Countries where female obesity exceeds male by large margin (same year)",
                                       "Global average obesity percentage per year"])
                                
# Obesity queries
# Run queries based on selection
    # Submit button
    if st.button('Submit'):
        if option == 'Top 5 regions with the highest average obesity levels in the most recent year(2022)':
            q1 = """
            SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            WHERE Year = 2022
            GROUP BY Region
            ORDER BY Avg_Obesity DESC
            LIMIT 5;
            """
            df1 = run_query(q1)
            st.dataframe(df1)
            st.bar_chart(df1.set_index("Region"))

        elif option == 'Top 5 countries with highest obesity estimates':
            q2 = """
            SELECT Country, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            GROUP BY Country
            ORDER BY Avg_Obesity DESC
            LIMIT 5;
            """
            df2 = run_query(q2)
            st.dataframe(df2)
            st.bar_chart(df2.set_index("Country"))

        elif option == 'Obesity trend in India over the years(Mean_estimate)':
            q3 = """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Obesity_India
            FROM obesity
            WHERE Country = 'India'
            GROUP BY Year;
            """
            df3 = run_query(q3)
            st.line_chart(df3.set_index("Year"))

        elif option == 'Average obesity by gender':
            q4 = """
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            GROUP BY Gender;
            """
            df4 = run_query(q4)
            st.dataframe(df4)
            st.bar_chart(df4.set_index("Gender"))

        elif option == 'Country count by obesity level category and age group':
            q5 = """
            SELECT Obesity_Level, age_group, COUNT(DISTINCT Country) AS Country_Count
            FROM obesity
            GROUP BY Obesity_Level, age_group;
            """
            df5 = run_query(q5)
            st.dataframe(df5)
            fig = px.bar(df5, x="age_group", y="Country_Count", color="Obesity_Level", barmode="group")
            st.plotly_chart(fig)

        elif option == 'Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)':
            q6 = """
            (
            SELECT Country, ROUND(AVG(CI_Width), 2) AS Avg_CI
            FROM obesity
            GROUP BY Country
            ORDER BY Avg_CI DESC
            LIMIT 5
            )
            UNION
            (
            SELECT Country, ROUND(AVG(CI_Width), 2) AS Avg_CI
            FROM obesity
            GROUP BY Country
            ORDER BY Avg_CI ASC
            LIMIT 5
            );
            """
            df6 = run_query(q6)
            st.dataframe(df6)
            fig6 = px.bar(df6, x='Country', y='Avg_CI', color='Avg_CI',
                  title='Countries with Highest and Lowest Average CI_Width (Obesity)',
                  labels={'Avg_CI': 'Avg CI Width'})
            st.plotly_chart(fig6)

        elif option == 'Average obesity by age group':
            q7 = """
            SELECT age_group, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            GROUP BY age_group;
            """
            df7 = run_query(q7)
            st.dataframe(df7)
            st.bar_chart(df7.set_index("age_group"))

        elif option == 'Top 10 Countries with consistent low obesity (low average + low CI)over the years':
            q8 = """
            SELECT Country, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity, ROUND(AVG(CI_Width), 2) AS Avg_CI
            FROM obesity
            GROUP BY Country
            HAVING Avg_Obesity < 20 AND Avg_CI < 5
            ORDER BY Avg_Obesity ASC
            LIMIT 10;
            """
            df8 = run_query(q8)
            st.dataframe(df8)
            # Simple grouped bar chart with Plotly
            fig8 = px.bar(
            df8.melt(id_vars="Country", value_vars=["Avg_Obesity", "Avg_CI"]),
            x="Country", y="value", color="variable", barmode="group",
            title="Top 10 Countries with Consistent Low Obesity (Mean Estimate & CI)",
            labels={"value": "Estimate"}
            )
            st.plotly_chart(fig8)

        elif option == 'Countries where female obesity exceeds male by large margin (same year)':
            q9 = """
            SELECT f.Country, f.Year, ROUND(f.Mean_Estimate - m.Mean_Estimate, 2) AS Diff
            FROM obesity f
            JOIN obesity m ON f.Country = m.Country AND f.Year = m.Year AND f.Gender = 'Female' AND m.Gender = 'Male'
            WHERE f.Mean_Estimate - m.Mean_Estimate > 10
            ORDER BY Diff DESC;
            """
            df9 = run_query(q9)
            st.dataframe(df9)
            # Horizontal bar chart with Plotly
            fig = px.bar(df9, x='Diff', y='Country', color='Year', orientation='h',
            title="Countries Where Female Obesity Exceeds Male by Large Margin",
            labels={'Diff': 'Difference (Female - Male)'})
            st.plotly_chart(fig)

        elif option == 'Global average obesity percentage per year':
            q10 = """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Global_Avg_Obesity
            FROM obesity
            GROUP BY Year;
            """
            df10 = run_query(q10)
            st.line_chart(df10.set_index("Year"))

# Malnutrition Queries section
if selected == "Malnutrition":
    option = st.selectbox(
        'Select a query to display:', ["Avg. malnutrition by age group",
                                       "Top 5 countries with highest malnutrition(mean_estimate)",
                                       "Malnutrition trend in African region over the years",
                                       "Gender-based average malnutrition",
                                       "Malnutrition level-wise (average CI_Width by age group)",
                                       "Yearly malnutrition change in specific countries(India, Nigeria, Brazil)",
                                       "Regions with lowest malnutrition averages",
                                       "Countries with increasing malnutrition",
                                       "Min/Max malnutrition levels year-wise comparison",
                                       "High CI_Width flags for monitoring(CI_width > 5)"])

# Malnutrition queries
# Run queries based on selection
    # Submit button
    if st.button('Submit'):
        if option == 'Avg. malnutrition by age group':
            q1 = """
            SELECT age_group, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY age_group;
            """
            df1 = run_query(q1)
            st.dataframe(df1)
            st.bar_chart(df1.set_index("age_group"))

        elif option == 'Top 5 countries with highest malnutrition(mean_estimate)':
            q2 = """
            SELECT Country, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Country
            ORDER BY Avg_Malnutrition DESC
            LIMIT 5;
            """
            df2 = run_query(q2)
            st.dataframe(df2)
            st.bar_chart(df2.set_index("Country"))

        elif option == 'Malnutrition trend in African region over the years':
            q3 = """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            WHERE Region = 'Africa'
            GROUP BY Year;
            """
            df3 = run_query(q3)
            st.line_chart(df3.set_index("Year"))

        elif option == 'Gender-based average malnutrition':
            q4 = """
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Gender;
            """
            df4 = run_query(q4)
            st.dataframe(df4)
            st.bar_chart(df4.set_index("Gender"))

        elif option == 'Malnutrition level-wise (average CI_Width by age group)':
            q5 = """
            SELECT malnutrition_level, age_group, ROUND(AVG(CI_Width), 2) AS Avg_CI_Width
            FROM malnutrition
            GROUP BY malnutrition_level, age_group;
            """
            df5 = run_query(q5)
            st.dataframe(df5)
            # Plotly grouped bar chart
            fig = px.bar(
            df5,
            x='age_group',
            y='Avg_CI_Width',
            color='malnutrition_level',
            barmode='group',
            title="Average CI_Width by Age Group and Malnutrition Level",
            labels={'Avg_CI_Width': 'Average CI Width', 'age_group': 'Age Group'}
            )
            st.plotly_chart(fig)

        elif option == 'Yearly malnutrition change in specific countries(India, Nigeria, Brazil)':
            q6 = """
            SELECT Year, Country, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            WHERE Country IN ('India', 'Nigeria', 'Brazil')
            GROUP BY Year, Country;
            """
            df6 = run_query(q6)
            st.dataframe(df6)
            fig = px.line(df6, x='Year', y='Avg_Malnutrition', color='Country', markers=True)
            st.plotly_chart(fig)

        elif option == 'Regions with lowest malnutrition averages':
            q7 = """
            SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Region
            ORDER BY Avg_Malnutrition ASC
            LIMIT 5;
            """
            df7 = run_query(q7)
            st.dataframe(df7)
            fig7 = px.bar(df7, x='Avg_Malnutrition', y='Region', orientation='h',
            title='Regions with Lowest Average Malnutrition',
            labels={'Avg_Malnutrition': 'Average Malnutrition'})
            st.plotly_chart(fig7)

        elif option == 'Countries with increasing malnutrition':
            q8 = """
            SELECT Country, MIN(Mean_Estimate) AS Min_Estimate, MAX(Mean_Estimate) AS Max_Estimate
            FROM malnutrition
            GROUP BY Country
            HAVING Max_Estimate - Min_Estimate > 0;
            """
            df8 = run_query(q8)
            st.dataframe(df8)
            # Calculate difference for visualization
            df8['Increase'] = df8['Max_Estimate'] - df8['Min_Estimate']
            fig8 = px.bar(df8.sort_values(by='Increase', ascending=False).head(10),
            x='Country', y='Increase',
            title='Top 10 Countries with Increasing Malnutrition',
            labels={'Increase': 'Change in Mean Estimate'})
            st.plotly_chart(fig8)

        elif option == 'Min/Max malnutrition levels year-wise comparison':
            q9 = """
            SELECT Year, MIN(Mean_Estimate) AS Min_Malnutrition, MAX(Mean_Estimate) AS Max_Malnutrition
            FROM malnutrition
            GROUP BY Year;
            """
            df9 = run_query(q9)
            st.dataframe(df9)
            st.line_chart(df9.set_index("Year"))

        elif option == 'High CI_Width flags for monitoring(CI_width > 5)':
            q10 = """
            SELECT *
            FROM malnutrition
            WHERE CI_Width > 5;
            """
            df10 = run_query(q10)
            st.dataframe(df10)
            fig10 = px.scatter(
            df10,
            x="Country",
            y="CI_Width",
            color="Year",
            size="CI_Width",
            hover_data=["age_group"],
            title="High CI_Width (> 5) for Malnutrition - By Country and Year"
            )
            st.plotly_chart(fig10)
            fig10b = px.box(
            df10,
            x="age_group",
            y="CI_Width",
            color="Region",
            title="Distribution of High CI_Width by Age Group and Region"
            )
            st.plotly_chart(fig10b)
  
# Combined Queries section
if selected == "Combined":
    option = st.selectbox(
        'Select a query to display:', ["Obesity vs malnutrition comparison by country(any 5 countries)",
                                       "Gender-based disparity in both obesity and malnutrition",
                                       "Region-wise avg estimates side-by-side(Africa and America)",
                                       "Countries with obesity up & malnutrition down",
                                       "Age-wise trend analysis"])
    
# Combined queries
# Run queries based on selection
    # Submit button
    if st.button('Submit'):
        if option == 'Obesity vs malnutrition comparison by country(any 5 countries)':
            q1 = """
            SELECT o.Country,
                   ROUND(AVG(o.Mean_Estimate), 2) AS Obesity,
                   ROUND(AVG(m.Mean_Estimate), 2) AS Malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
            WHERE o.Country IN ('India', 'Brazil', 'Nigeria', 'United States of America', 'China')
            GROUP BY o.Country;
            """
            df1 = run_query(q1)
            st.dataframe(df1)
            fig = px.bar(df1.melt(id_vars="Country", value_name="Estimate"), x="Country", y="Estimate", color="variable", barmode='group', title="Obesity vs Malnutrition")
            st.plotly_chart(fig)

        elif option == 'Gender-based disparity in both obesity and malnutrition':
            q2 = """
            SELECT o.Gender,
                   ROUND(AVG(o.Mean_Estimate), 2) AS Avg_Obesity,
                   ROUND(AVG(m.Mean_Estimate), 2) AS Avg_Malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Gender = m.Gender AND o.Year = m.Year
            GROUP BY o.Gender;
            """
            df2 = run_query(q2)
            st.dataframe(df2)
            fig = px.bar(df2.melt(id_vars="Gender", value_name="Estimate"), x="Gender", y="Estimate", color="variable", barmode='group', title="Gender-Based Comparison")
            st.plotly_chart(fig)

        elif option == 'Region-wise avg estimates side-by-side(Africa and America)':
            q3 = """
            SELECT o.Region,
                   ROUND(AVG(o.Mean_Estimate), 2) AS Avg_Obesity,
                   ROUND(AVG(m.Mean_Estimate), 2) AS Avg_Malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Region = m.Region AND o.Year = m.Year
            WHERE o.Region IN ('Africa', 'Americas')
            GROUP BY o.Region;
            """
            df3 = run_query(q3)
            st.dataframe(df3)
            df3_melted = df3.melt(id_vars='Region', value_vars=['Avg_Obesity', 'Avg_Malnutrition'],
                          var_name='Metric', value_name='Estimate')
            fig3 = px.bar(df3_melted, x='Region', y='Estimate', color='Metric', barmode='group',
                  title="Obesity vs Malnutrition - Africa vs Americas")
            st.plotly_chart(fig3)

        elif option == 'Countries with obesity up & malnutrition down':
            q4 = """
            SELECT o.Country
            FROM (
            SELECT Country, MAX(Mean_Estimate) - MIN(Mean_Estimate) AS Obesity_Trend
            FROM obesity
            GROUP BY Country
            ) o
            JOIN (
            SELECT Country, MIN(Mean_Estimate) - MAX(Mean_Estimate) AS Malnutrition_Trend
            FROM malnutrition
            GROUP BY Country
            ) m ON o.Country = m.Country
            WHERE o.Obesity_Trend > 0 AND m.Malnutrition_Trend > 0;

            """
            df4 = run_query(q4)
            st.dataframe(df4)
            fig4 = px.bar(df4, x='Country', title='Countries with Rising Obesity & Declining Malnutrition')
            st.plotly_chart(fig4)

        elif option == 'Age-wise trend analysis':
            q5 = """
            SELECT o.age_group,
                   ROUND(AVG(o.Mean_Estimate), 2) AS Avg_Obesity,
                   ROUND(AVG(m.Mean_Estimate), 2) AS Avg_Malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.age_group = m.age_group AND o.Year = m.Year
            GROUP BY o.age_group;
            """
            df5 = run_query(q5)
            st.dataframe(df5)
            fig = px.bar(df5.melt(id_vars="age_group", value_name="Estimate"), x="age_group", y="Estimate", color="variable", barmode='group', title="Age-wise Trends")
            st.plotly_chart(fig)

connection.close()