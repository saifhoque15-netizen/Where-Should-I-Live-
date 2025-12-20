# 🌍 Where Should I Live? (Group 22)

## PDS Project 2025/2026

This data science application helps users find their ideal living location based on lifestyle preferences. It utilizes a Recommendation System and Comparative Analysis tools to visualize and match users with cities.

## 📂 Project Structure

```text
├── requirements.txt           # Python dependencies
├── Group22_PDS_2526.ipynb     # Exploratory Data Analysis Notebook
├── data-science-in-action/    # Data Science in Action
│   ├── components/            # Helper scripts (Wiki, matching logic, etc.)
│   ├── images/                # Assets
│   └── pages/                 # Application Pages
│       ├── Comparative Analysis.py
│       ├── Life Style Match.py
│       ├── Recommendation System.py
│       └── Where Should I Live.py
```
## 🛠️ Installation & Setup Guide

1. Open a terminal in the main directory.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install the requirments
```bash
pip install -r requirements.txt
```
4. Run the application using Streamlit:
```bash
streamlit run '.\data-science-in-action\Where Should I Live.py'
```
## Application Prviews
![Welcome Page](./data-science-in-action/images/first-page.png)

![Compare Two European Cities](./data-science-in-action/images/comparative-analysis.png)

![The Best European City Based On Your Lifestyle](./data-science-in-action/images/life-style-match.png)

![European City Recommendation](./data-science-in-action/images/recommendation-system.png)

## Authors
Group 22
