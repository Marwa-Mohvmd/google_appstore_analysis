import pandas as pd
import plotly.express as px
import os

# =========================
# Working Directory
# =========================
print("Current working directory:", os.getcwd())

# =========================
# Load Dataset
# =========================
df = pd.read_csv("google_play_store_dataset.csv")

# =========================
# Data Cleaning
# =========================
df = df.dropna(subset=['Rating'])

df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

df['Price'] = df['Price'].str.replace('$', '', regex=False)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

df = df.dropna(subset=['Installs'])

print(df.info())
print("\nDataset cleaned successfully ✔")

# =========================
#  Create Charts Folder
# =========================
base_dir = os.path.dirname(os.path.abspath(__file__))
charts_dir = os.path.join(base_dir, "charts")

os.makedirs(charts_dir, exist_ok=True)

# =========================
# .Top Categories
# =========================
top_categories = df['Category'].value_counts().head(10)

fig1 = px.bar(
    x=top_categories.index,
    y=top_categories.values,
    title="Top 10 App Categories",
    labels={'x': 'Category', 'y': 'Count'}
)
fig1.write_html(os.path.join(charts_dir, "top_categories.html"))
fig1.show()

# =========================
#  Highest Rated Categories
# =========================
highest_rated = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(10)

fig2 = px.bar(
    x=highest_rated.index,
    y=highest_rated.values,
    title="Top Rated Categories",
    labels={'x': 'Category', 'y': 'Average Rating'}
)
fig2.write_html(os.path.join(charts_dir, "top_rated.html"))
fig2.show()

# =========================
#  Rating vs Installs
# =========================
fig3 = px.scatter(
    df,
    x='Installs',
    y='Rating',
    title="Rating vs Installs",
    opacity=0.5
)
fig3.write_html(os.path.join(charts_dir, "rating_vs_installs.html"))
fig3.show()

# =========================
#  Price vs Rating
# =========================
fig4 = px.scatter(
    df,
    x='Price',
    y='Rating',
    title="Price vs Rating",
    opacity=0.5
)
fig4.write_html(os.path.join(charts_dir, "price_vs_rating.html"))
fig4.show()

# ========================
# Reviews vs Rating
# =========================
fig5 = px.scatter(
    df,
    x='Reviews',
    y='Rating',
    title="Reviews vs Rating",
    opacity=0.5
)
fig5.write_html(os.path.join(charts_dir, "reviews_vs_rating.html"))
fig5.show()

# =========================
#  Rating Distribution
# =========================
fig6 = px.histogram(
    df,
    x='Rating',
    nbins=20,
    title="Rating Distribution"
)
fig6.write_html(os.path.join(charts_dir, "rating_distribution.html"))
fig6.show()

# =========================
#  Top Apps by Installs
# 
top_apps = df.sort_values('Installs', ascending=False).head(10)

fig7 = px.bar(
    top_apps,
    x='App',
    y='Installs',
    title="Top Apps by Installs"
)
fig7.write_html(os.path.join(charts_dir, "top_apps_installs.html"))
fig7.show()


corr_df = df[['Rating', 'Reviews', 'Installs', 'Price']]

corr_matrix = corr_df.corr()

fig8 = px.imshow(
    corr_matrix,
    text_auto=True,
    title="Correlation Heatmap (Numeric Features)",
    color_continuous_scale='RdBu',
    aspect="auto"
)

fig8.write_html(os.path.join(charts_dir, "correlation_heatmap.html"))
fig8.show()


