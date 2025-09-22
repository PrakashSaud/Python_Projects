# PayScale College Salary Analysis

## Project Overview
This project explores a dataset of salaries by college major using Python and Pandas.  
The goal is to answer key questions about **college degree earnings**, including:

- Which degrees have the **highest starting salaries**?  
- Which majors have the **lowest earnings after graduation**?  
- Which degrees have the **highest earning potential**?  
- Which degrees are the **lowest risk** in terms of salary variation?  
- How do **STEM, Business, and HASS** (Humanities, Arts, Social Science) degrees compare?

The project demonstrates **data cleaning, exploration, and analysis** using Pandas in a Jupyter Notebook.

---

## Dataset
The dataset used is `salaries_by_college_major.csv` from PayScale, containing:

- Undergraduate Major  
- Starting Median Salary  
- Mid-Career Median Salary  
- 10th and 90th Percentile Salaries  
- Degree Group (STEM, Business, HASS)

---

## What We Did

1. **Data Loading & Exploration**
   - Loaded the dataset into a Pandas DataFrame.
   - Checked the number of rows and columns.
   - Inspected column names and first/last rows.
   - Detected and removed junk data or missing values (NaNs).

2. **Accessing Columns and Cells**
   - Extracted specific columns like `Starting Median Salary`.
   - Identified the major with the **highest starting salary**.
   - Found the majors with the **lowest starting and mid-career salaries**.

3. **Sorting & Adding Columns**
   - Calculated the **spread** between the 10th and 90th percentile salaries.
   - Sorted majors to identify:
     - **Lowest-risk majors** (smallest spread)
     - **Highest potential majors** (top 90th percentile salaries)
     - **Majors with greatest spread** (highest salary variation)

4. **Grouping Data**
   - Grouped majors by category (`STEM`, `Business`, `HASS`) using `.groupby()`.
   - Calculated **average salaries by group**.
   - Compared which degree groups earned more on average.

5. **Formatting & Presentation**
   - Formatted numbers with commas and 2 decimal places for readability.
   - Prepared the data for potential visualization (bar charts, etc.).

---

## Key Insights
- Some STEM majors like **Physics** and **Engineering** have the highest starting and mid-career salaries.  
- HASS majors generally have lower starting salaries, but some have good mid-career growth.  
- Majors with the **smallest spread** are low-risk in terms of salary uncertainty.  
- Degree groups comparison shows **STEM** typically earns more than **Business** or **HASS** on average.

---

## How to Run
1. Clone this repository:

```bash
git clone https://github.com/your-username/PayScale-Salary-Analysis.git