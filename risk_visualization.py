import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import seaborn as sns
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# --- Load Data ---

# Adjust the path to your shapefile
shapefile_path = 'in_district.shp'
gdf = gpd.read_file(shapefile_path)

# Adjust the path to your CSV
village_csv = 'village_data.csv'
df = pd.read_csv(village_csv)

# Convert village DataFrame to GeoDataFrame
villages = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']),
    crs='EPSG:4326'
)

# Project to Web Mercator for basemap compatibility
gdf = gdf.to_crs(epsg=3857)
villages = villages.to_crs(epsg=3857)

# UCIL mine locations (add more as needed)
ucil_mines = pd.DataFrame({
    'Mine': ['Jaduguda', 'Bhatin', 'Narwapahar', 'Turamdih', 'Banduhurang'],
    'Longitude': [86.346639, 86.350833, 86.271430, 86.190833, 86.180278],
    'Latitude': [22.653273, 22.645833, 22.696070, 22.739722, 22.778889]
})

ucil_gdf = gpd.GeoDataFrame(
    ucil_mines,
    geometry=gpd.points_from_xy(ucil_mines['Longitude'], ucil_mines['Latitude']),
    crs='EPSG:4326'
).to_crs(epsg=3857)

# --- Plot Full Map ---

fig, ax = plt.subplots(figsize=(12, 12))
gdf.plot(ax=ax, color='white', edgecolor='gray', linewidth=0.7, zorder=1)
villages[villages['Risk'] == 0].plot(ax=ax, color='green', markersize=15, label='Low Risk', alpha=0.6, zorder=2)
villages[villages['Risk'] == 1].plot(ax=ax, color='red', markersize=15, label='High Risk', alpha=0.7, zorder=3)
ucil_gdf.plot(ax=ax, marker='*', color='blue', markersize=200, label='UCIL Mine', zorder=4)
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=7)
plt.legend()
plt.title('Village Risk Map with District Boundaries and UCIL Mines', fontsize=16)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('village_risk_map_full.png', dpi=300)
plt.show()

# --- Zoomed Inset for High-Risk Cluster ---

fig, ax = plt.subplots(figsize=(12, 12))
gdf.plot(ax=ax, color='white', edgecolor='gray', linewidth=0.7, zorder=1)
villages[villages['Risk'] == 0].plot(ax=ax, color='green', markersize=15, label='Low Risk', alpha=0.6, zorder=2)
villages[villages['Risk'] == 1].plot(ax=ax, color='red', markersize=15, label='High Risk', alpha=0.7, zorder=3)
ucil_gdf.plot(ax=ax, marker='*', color='blue', markersize=200, label='UCIL Mine', zorder=4)
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=7)

# Define zoom region (adjust these limits to your cluster)
x1, x2 = 9600000, 9700000
y1, y2 = 2500000, 2600000

axins = inset_axes(ax, width="40%", height="40%", loc='lower left')
gdf.plot(ax=axins, color='white', edgecolor='gray', linewidth=0.7)
villages[villages['Risk'] == 0].plot(ax=axins, color='green', markersize=15, alpha=0.6)
villages[villages['Risk'] == 1].plot(ax=axins, color='red', markersize=15, alpha=0.7)
ucil_gdf.plot(ax=axins, marker='*', color='blue', markersize=200)
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
ctx.add_basemap(axins, source=ctx.providers.CartoDB.Positron, zoom=10)
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

plt.savefig('village_risk_map_inset.png', dpi=300)
plt.show()

# --- Density/Heatmap of High-Risk Villages ---

high_risk = villages[villages['Risk'] == 1]
x = high_risk.geometry.x
y = high_risk.geometry.y

# Add these print statements for debugging:
print("Number of high-risk villages:", len(high_risk))
print("Sample high-risk villages:")
print(high_risk.head())
print("X range:", x.min(), "to", x.max())
print("Y range:", y.min(), "to", y.max())

fig, ax = plt.subplots(figsize=(12, 12))
gdf.plot(ax=ax, color='white', edgecolor='gray', linewidth=0.7, zorder=1)
sns.kdeplot(x=x, y=y, cmap="Reds", fill=True, alpha=0.5, ax=ax, zorder=2, bw_adjust=2, thresh=0.01)
ax.scatter(x, y, color='red', s=10, alpha=0.6, label='High Risk Villages')  # Overlay points
ucil_gdf.plot(ax=ax, marker='*', color='blue', markersize=200, label='UCIL Mine', zorder=3)
plt.title('High-Risk Village Density Map')
plt.legend()
plt.savefig('village_risk_density.png', dpi=300)
plt.show()
