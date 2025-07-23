import ee
import geemap
import pandas as pd

# Authenticate and initialize Earth Engine
try:
    ee.Initialize(project='part-1-461618')
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project='part-1-461618')

# Define the location and buffer (in meters)
point = ee.Geometry.Point([86.3529, 22.6560])
roi = point.buffer(1000)  # 1 km radius buffer

# Load the Hansen Global Forest Change dataset
gfc = ee.Image('UMD/hansen/global_forest_change_2024_v1_12')

# Select relevant bands
treecover2000 = gfc.select('treecover2000')
lossyear = gfc.select('lossyear')

# Apply forest mask for areas with >30% tree canopy cover in 2000
forest_mask = treecover2000.gte(30)

# Calculate annual forest loss from 2010 to 2023
years = list(range(2010, 2024))
loss_areas = []

for year in years:
    loss_mask = lossyear.eq(year - 2000).And(forest_mask)
    area_image = loss_mask.multiply(ee.Image.pixelArea()).divide(10000)  # hectares
    stats = area_image.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=roi,
        scale=30,
        maxPixels=1e9
    )
    loss_ha = stats.getInfo().get('lossyear', 0)
    loss_areas.append(loss_ha)

# Create a DataFrame for easier viewing
forest_loss_df = pd.DataFrame({'year': years, 'forest_loss_ha': loss_areas})
print(forest_loss_df)

# Optional visualization using geemap
Map = geemap.Map()
Map.centerObject(point, 13)
Map.addLayer(forest_mask.selfMask(), {'palette': 'green'}, 'Forest 2000')
Map.addLayer(lossyear.selfMask(), {'min': 10, 'max': 23, 'palette': ['yellow', 'red']}, 'Loss Year')
Map.addLayer(roi, {}, 'ROI')
# Display the map (in Jupyter environment this would show the map)
print(Map)
