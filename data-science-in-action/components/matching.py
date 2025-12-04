import numpy as np
import pandas as pd

def find_matching(df, user_language, weights):
    # GDP per Capita
    w = weights['GDP per Capita']
    weights['GDP per Capita'] = df['GDP per Capita'].quantile(w / 10)


    cond = (
    (df["Unemployment Rate"] <= weights["Unemployment Rate"]) &
    (df["GDP per Capita"] >= weights["GDP per Capita"]) &
    (df["Average Monthly Salary"] <= weights["Average Monthly Salary"]) &
    (df["Average Rent Price"] <= weights["Average Rent Price"]) &
    (df["Average Cost of Living"] <= weights["Average Cost of Living"]))

    filtered = df[cond]

    if user_language != 'Any':
        filtered = filtered[
            filtered['Main Spoken Languages']
            .astype(str)
            .str.split(',')
            .apply(lambda x: user_language in [s.strip() for s in x])
    ]

    
    if not filtered.empty:
        filtered = filtered.sort_values(
            ['Average Monthly Salary', 'GDP per Capita', 'Average Rent Price', 'Average Cost of Living', 'Unemployment Rate'],
            ascending=[False, False, True, True, True]
        )


    return filtered


