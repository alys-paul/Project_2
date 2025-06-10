# 🥗 Nutrition Paradox: A Global View on Obesity and Malnutrition

This project explores the global paradox of **obesity** and **malnutrition** co-existing across countries, age groups, and regions. Using WHO data, we perform data cleaning, exploratory data analysis (EDA), and develop a Streamlit dashboard to visualize and understand global nutrition trends.

---

## 📁 Project Structure

```
nutrition-paradox/
├── nutrition_paradox_eda.ipynb     # Data cleaning, transformation & EDA (Jupyter)
├── nutrition_paradox_dashboard.py  # Interactive Streamlit dashboard
├── README.md                       # Project overview
```

---

## 📊 Dataset Sources

* **Obesity & Malnutrition data** from [World Health Organization (WHO)](https://www.who.int/data)
* Contains country-wise, age-group-wise, and year-wise estimates for nutrition metrics

---

## ⚙️ Technologies Used

* **Python** (pandas, numpy, matplotlib, seaborn, plotly, PyMySQL)
* **Jupyter Notebook** for EDA
* **Streamlit** for dashboard UI
* **MySQL** for structured data storage
* **SQL** queries for dashboard filtering

---

## 📌 Features

### 📘️ Notebook: `nutrition_paradox_eda.ipynb`

* Loads and cleans raw WHO nutrition datasets
* Handles missing values, standardizes column names
* Performs exploratory visualizations (histograms, heatmaps, trend lines)
* Exports cleaned data to a MySQL database (`nutrition_paradox`)

### 🔤️ Dashboard: `nutrition_paradox_dashboard.py`

* Connects to MySQL to query live data
* Interactive views for:

  * Obesity/Malnutrition trends by country, age group, region
  * Combined insights across countries and regions
  * SQL-driven data filters with Plotly visualizations
* Modern UI with custom CSS styling and sidebar filters

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/nutrition-paradox.git
cd nutrition-paradox
```

### 2. Set up environment

Install required libraries:

```bash
pip install -r requirements.txt
```

### 3. Set up MySQL database

* Create a MySQL database named `nutrition_paradox`
* Update your `.env` file or hardcoded credentials in both files with:

```
host = "localhost"
user = "your_mysql_username"
password = "your_mysql_password"
database = "nutrition_paradox"
```

### 4. Run the notebook

Clean and upload data to MySQL using:

```bash
jupyter notebook nutrition_paradox_eda.ipynb
```

### 5. Launch the Streamlit dashboard

```bash
streamlit run nutrition_paradox_dashboard.py
```

---

### 6. 📝 Summary & Insights

* India and South-East Asia face high malnutrition rates.

* Developed countries show rising obesity, especially among adults.

* Female populations in many regions are more prone to obesity.

* CI_Width is highly variable for child datasets, indicating estimation uncertainty.


## 🤝 Acknowledgements

* World Health Organization (WHO) for global nutrition datasets
* Plotly & Streamlit for amazing open-source tools

