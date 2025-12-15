import numpy as np
import pandas as pd

def find_matching(df, user_language, pref):

    constraints = (
        (df["Average Rent Price"] <= pref["Average Rent Price"]) &
        (df["Average Cost of Living"] <= pref["Average Cost of Living"]) &
        (df["Average Monthly Salary"] >= pref["Average Monthly Salary"])
    )

    filtered = df[constraints].copy()

    if not filtered.empty:
        if user_language != "Any":
            filtered = filtered[
                filtered["Main Spoken Languages"]
                .astype(str)
                .str.split(",")
                .apply(lambda x: user_language in [s.strip() for s in x])
        ]
        
        filtered["score"] = (
            filtered["GDP per Capita"].rank(pct=True) +
            filtered["Average Monthly Salary"].rank(pct=True) -
            filtered["Unemployment Rate"].rank(pct=True)
        )

        filtered  = filtered.sort_values("score", ascending=False)

    if "score" in filtered.columns:
        return filtered.drop(columns="score")
    return filtered



