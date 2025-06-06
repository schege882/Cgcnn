from mp_api.client import MPRester
import pandas as pd
import os

# Replace this with your Materials Project API key
API_KEY = ''

# # Query for materials
with MPRester(API_KEY) as mpr:
  docs = mpr.materials.summary.search(
      elements=["Si", "O"],
      band_gap=(0.5,1.0),
      fields=["material_id", "formula_pretty", "formation_energy_per_atom", "structure"]
  )

# Another example query
# filepath = '/home/vosti/MachineLearning/materialScience/cgcnn/data/material-data/mp-ids-3402.csv'
# mat_id_df = pd.read_csv(filepath)
# mat_ids = mat_id_df.iloc[0:1000, 0].tolist()

# with MPRester(API_KEY) as mpr:
#   docs = mpr.materials.summary.search(
#      material_ids=mat_ids,
#       fields=["material_id", "formula_pretty", "formation_energy_per_atom", "structure"]
#   )


data = []
idprop = [] # material_id, target_property

# Loop for saving and organizing data
for doc in docs:
    material_id = doc.material_id
    formula = doc.formula_pretty
    structure = doc.structure
    formation_energy = doc.formation_energy_per_atom

    if structure is None or formation_energy is None:
        continue

    # Record material properties in a list
    data.append([material_id, formula, formation_energy])

    material_id_trimmed = material_id[3:]

    # Record material_id, property(id_prop.csv) to idprop list
    idprop.append([material_id_trimmed, formation_energy])

    # Save CIF files
    cif_path = f"./{material_id_trimmed}.cif"
    structure.to(fmt="cif", filename=cif_path)

# Save full dataset CSV
df = pd.DataFrame(data, columns=["material_id", "formula", "formation_energy"])
df.to_csv("full_dataset.csv", index=False)
print(f"Saved {len(df)} materials with CIFs and the full dataset.")

# Save id-property data
idprop_df = pd.DataFrame(idprop, columns=["material_id_trimmed", "formation_energy"])
idprop_df.to_csv("id_prop.csv", index=False)
print("id_prop.csv created successfully")

