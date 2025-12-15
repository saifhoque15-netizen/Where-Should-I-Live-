import pandas as pd
import numpy as np

PARAMS = [
    "cost", "climate", "green", "nightlife",
    "job_market", "safety", "international",
    "walkability", "culture",
    "health", "air_quality"
]

def build_user_vector(answers):
    vec = dict.fromkeys(PARAMS, 0.0)

    # Weekend
    if answers["weekend"] == "Hiking or being in nature":
        vec["climate"] += 0.4
        vec["green"] += 0.8
        vec["air_quality"] += 0.6
        vec["nightlife"] -= 0.2
    elif answers["weekend"] == "Cafés, museums, slow walks":
        vec["walkability"] += 0.5
        vec["culture"] += 0.7
    else:  # Bars/Nightlife
        vec["nightlife"] += 0.7
        vec["international"] += 0.3
        vec["cost"] += 0.2

    # Home
    if answers["home"] == "Small but central":
        vec["walkability"] += 0.6
        vec["cost"] -= 0.3
    elif answers["home"] == "Spacious and quiet":
        vec["safety"] += 0.4
        vec["green"] += 0.4
        vec["nightlife"] -= 0.2
        vec["air_quality"] += 0.5

    # Social
    if answers["social"] == "Work and professional networks":
        vec["job_market"] += 0.7
    elif answers["social"] == "Community events and hobbies":
        vec["culture"] += 0.3
        vec["safety"] += 0.3
    else:  # Expat
        vec["international"] += 0.8

    # Rhythm
    if answers["rhythm"] == "Early mornings":
        vec["safety"] += 0.3
        vec["nightlife"] -= 0.4
    elif answers["rhythm"] == "Late nights":
        vec["nightlife"] += 0.6

    # Stability vs Adventure
    adventure_score = (answers["adventure"] - 5) / 5.0
    vec["international"] += adventure_score * 0.4
    vec["safety"] -= adventure_score * 0.3
    vec["health"] += (10 - answers["adventure"]) * 0.05

    # Normalize
    arr = np.array(list(vec.values()), dtype=float)
    vec = dict(zip(PARAMS, arr / (np.linalg.norm(arr) + 1e-6)))

    return vec

def build_city_vector(row):
    vec = {}
    vec["cost"] = -(row["Average Rent Price"] + row["Average Cost of Living"]) / 2
    vec["climate"] = -row["Days of Very Strong Heat Stress"]
    vec["green"] = row["Green Space Index"]
    vec["nightlife"] = np.log1p(row["Population Density"]) + (row["Youth Dependency Ratio"] * 0.5)
    vec["job_market"] = row["GDP per Capita"] - (row["Unemployment Rate"] * 500)
    vec["safety"] = row["GDP per Capita"] - (row["Unemployment Rate"] * 200)
    vec["international"] = 1.0 if "English" in str(row["Main Spoken Languages"]) else 0.0
    if row["GDP per Capita"] > 40000:
        vec["international"] += 0.5
    vec["walkability"] = np.sqrt(row["Population Density"])
    vec["culture"] = np.log1p(row["Population Density"]) + (row["GDP per Capita"] / 10000)
    vec["health"] = row["Health Care Index"] + (row["Life Expectancy (Years)"] * 0.5)
    vec["air_quality"] = row["Air Quality Index"] - (row["CO2 Emissions (per capita)"] * 2)
    return vec

def build_city_matrix(df):
    city_vectors = [build_city_vector(row) for _, row in df.iterrows()]
    city_df = pd.DataFrame(city_vectors)
    city_df.index = df["City"]
    return normalize(city_df)

def normalize(df):
    df_norm = df.copy()
    for c in df.columns:
        min_v, max_v = df[c].min(), df[c].max()
        df_norm[c] = (df[c] - min_v) / (max_v - min_v) if max_v - min_v != 0 else 0
    return df_norm

def recommend_cities(user_vc, city_df, top_n=3):
    params_order = city_df.columns.tolist()
    user_vec_arr = np.array([user_vc[p] for p in params_order])
    user_vec_arr /= (np.linalg.norm(user_vec_arr) + 1e-6)

    scores = {}
    for city in city_df.index:
        city_vec = city_df.loc[city].values
        city_vec /= (np.linalg.norm(city_vec) + 1e-6)
        scores[city] = np.dot(city_vec, user_vec_arr)

    sorted_cities = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [c for c, _ in sorted_cities[:top_n]], [s for _, s in sorted_cities[:top_n]]
