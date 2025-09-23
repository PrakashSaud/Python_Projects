📊 Programming Language Popularity Analysis

This project explores the popularity of different programming languages over time using Stack Overflow data. Each post on Stack Overflow comes with tags, and many of these tags represent programming languages. By analyzing the number of posts tagged with each language, we can uncover which languages are the most widely discussed and how their popularity has changed over the years.

⸻

🚀 Project Overview
	•	The oldest programming language still in use is FORTRAN (1957), but many languages have been developed since then.
	•	Which one is the most popular today?
	•	To answer this, we use Stack Overflow posts with programming language tags and count them over time.
	•	The language with the most posts is considered the most “popular” (or at least the most talked about).

This project demonstrates:
	•	📈 Visualizing data and creating charts with Matplotlib
	•	🧮 Pivoting, grouping, and manipulating data with Pandas
	•	⏱️ Working with timestamps and time-series data
	•	🎨 Styling and customizing line charts

⸻

📂 Dataset

The dataset comes from Stack Overflow queries and is included as QueryResults.csv.
It contains:
	•	DATE → Timestamp of the post (monthly aggregation)
	•	TAG → Programming language tag
	•	POSTS → Number of posts with that tag in that month