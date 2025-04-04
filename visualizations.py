import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("/home/miq/analysis_of_states_exc.csv")

df_clean = df.copy()

df_clean["state"] = df_clean["key_row"].str.title()
df_clean = df_clean.dropna(subset=["median_sale_price", "house_affordability_ratio"])

# 1. Bar Charts - Top 10 states by Median Household Income
top_income_states = df_clean.nlargest(10, "median_household_income")
plt.figure(figsize=(10, 6))
plt.barh(top_income_states["state"], top_income_states["median_household_income"], color="teal")
plt.xlabel("Median Household Income ($)")
plt.title("Top 10 States by Median Household Income")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 2. Scatter Plot - Income vs. Median Sale Price
plt.figure(figsize=(8, 6))
plt.scatter(df_clean["median_household_income"], df_clean["median_sale_price"], alpha=0.7, color="darkorange")
plt.xlabel("Median Household Income ($)")
plt.ylabel("Median Sale Price ($)")
plt.title("Income vs. Median Sale Price")
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Line Chart - States Ranked by House Affordability Ratio 
ranked_affordability = df_clean.sort_values("house_affordability_ratio")
plt.figure(figsize=(12, 6))
plt.plot(ranked_affordability["state"], ranked_affordability["house_affordability_ratio"], marker='o', color='purple')
plt.xticks(rotation=90)
plt.xlabel("State")
plt.ylabel("House Affordability Ratio")
plt.title("States Ranked by House Affordability (Lower is Better)")
plt.tight_layout()
plt.show()

# 4. Bar Chart - State vs Pop Ranks
pop_ranks = df_clean.sort_values("population_rank")
plt.figure(figsize=(12, 6))
plt.bar(pop_ranks["state"], pop_ranks["population_rank"], color='blue')
plt.xticks(rotation=90)  
plt.xlabel("State")
plt.ylabel("Population Rank (Lower is Better)")
plt.title("States by Population Rank")
plt.gca()
plt.tight_layout()
plt.show()


