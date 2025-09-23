# Stack Overflow Programming Language Popularity Analysis

## Project Overview
This project analyzes the popularity of different programming languages over time using **Stack Overflow post data**. Each post on Stack Overflow is tagged with a programming language, allowing us to measure trends and see which languages gained or lost popularity across different periods.

The analysis includes:
- Data cleaning and timestamp handling
- Pivoting data for time-series analysis
- Data visualization with Matplotlib
- Smoothing time-series data to reveal trends
- Comparative analysis for different time periods (2008–2012, 2015–2018, 2018–2021, 2021–Ongoing)
- Year-specific insights (e.g., 2020 trends)

---

## Data Description
- **Source:** Stack Overflow QueryResults.csv
- **Columns:**
  - `DATE`: The month of the data record
  - `TAG`: Programming language tag
  - `POSTS`: Number of posts for the given tag in that month

---

## Project Steps

### 1. Preliminary Data Exploration
- Read CSV into a Pandas DataFrame
- Checked shape, first & last rows, and column counts
- Understood the data and column types

### 2. Data Cleaning
- Converted `DATE` from string to `datetime` objects
- Ensured proper handling of missing or NaN values

### 3. Data Manipulation
- Pivoted DataFrame to have **dates as rows** and **programming languages as columns**
- Filled missing values with 0 for proper analysis
- Counted posts per language

### 4. Data Visualization
- Plotted line charts to show popularity trends over time
- Created multi-line charts for all programming languages
- Added styling: figure size, tick font, axis labels, legends
- Applied **rolling mean (window=6)** to smooth trends

### 5. Comparative Analysis
- Analyzed popularity over specific periods:
  - 2008–2012
  - 2015–2018
  - 2018–2021
  - 2021–Ongoing
- Identified top 3 languages for each period and visualized using bar charts
- Analyzed **year 2020** separately for detailed trends

---

## Key Findings
- Python consistently emerged as the most popular language over time
- Java, JavaScript, and C# remained strong in early years
- Rolling mean helps visualize trends clearly by smoothing noisy data
- Popularity trends shift across periods, showing growth or decline of languages

---

## Technologies Used
- Python 3.x
- Pandas for data manipulation
- Matplotlib for visualization
- Jupyter Notebook for analysis workflow

---

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/PrakashSaud/Python_Projects.git
