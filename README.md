# COVID‑19 Global Data Tracker

A Jupyter Notebook project that fetches, cleans, and visualizes up‑to‑date COVID‑19 data for global and country‑level trends.

---

## 🎯 Objectives

1. **Fetch** daily COVID‑19 case and death counts from a trusted public API.  
2. **Clean** and merge multi‑source data into a unified pandas DataFrame.  
3. **Analyze** trends over time, compare regions, and highlight hotspots.  
4. **Visualize** results with clear, interactive charts (Plotly/Matplotlib).  
5. **Reflect** on data challenges and key insights.

---

## 🛠 Tools & Libraries

- **Python 3.9+** – core language  
- **pandas** – data manipulation  
- **requests** – API calls  
- **plotly** – interactive plots  
- **matplotlib** – static charts  
- **Jupyter Notebook** – development environment  

---

## 🚀 How to Run

How to run it end‑to‑end:

Paste into a Jupyter cell or save as e.g. covid19_global_tracker.py.

If in Jupyter, just “Run All.”

If as a script:

pip install pandas plotly
python covid19_global_tracker.py

---

## 📊 Key Insights & Reflections
Data Lag & Gaps: Some countries publish with multi‑day delays, leading to “staircase” plots in their time series.

Variants & Waves: Clear second/third waves in Europe (Oct ’20, Mar ’21) versus single sustained wave in many African nations.

API Rate Limits: Caching responses locally helped avoid exceeding free‑tier limits.

“Aha” Moment: Switching from cumulative counts to 7‑day rolling averages smoothed out reporting artifacts and made trends crystal clear.

---

**Thank you for checking out my project! Any questions or feedback are welcome—feel free to open an issue or drop me a line.**

---
