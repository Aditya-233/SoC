import pandas as pd
import matplotlib.pyplot as plt

# Load village data
df = pd.read_csv('village_data.csv')

# Define UCIL mine locations
ucil_mines = pd.DataFrame({
    'Mine': ['Jaduguda', 'Bhatin', 'Narwapahar', 'Turamdih', 'Banduhurang'],
    'Longitude': [86.346639, 86.350833, 86.271430, 86.190833, 86.180278],
    'Latitude': [22.653273, 22.645833, 22.696070, 22.739722, 22.778889]
})

# Plotting
plt.figure(figsize=(10, 8))
plt.scatter(df[df['Risk'] == 0]['Longitude'], df[df['Risk'] == 0]['Latitude'],
            c='green', label='Low Risk', alpha=0.6, s=20)
plt.scatter(df[df['Risk'] == 1]['Longitude'], df[df['Risk'] == 1]['Latitude'],
            c='red', label='High Risk', alpha=0.7, s=20)

# Add UCIL mines as blue stars
plt.scatter(ucil_mines['Longitude'], ucil_mines['Latitude'],
            c='blue', marker='*', s=100, label='UCIL Mines', edgecolors='black')

# Labels and legend
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Village Risk Map with UCIL Mines')
plt.legend()

# Save plot
plt.savefig('village_risk_map.png', dpi=300, bbox_inches='tight')
plt.show()



