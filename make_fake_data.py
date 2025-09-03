import numpy as np, pandas as pd
from pathlib import Path
rng = np.random.default_rng(42)
Path("data/raw").mkdir(parents=True, exist_ok=True)

sucursales = ["TALCA","CURICO","LINARES","PARRAL"]
segmentos = ["TRADICIONAL","MAYORISTA","OTROS"]
canales = ["MODERNO","KKAA","HORECA","TT_RESTO"]
meses = pd.period_range("2024-01", "2024-12", freq="M").astype(str)

rows = []
cliente_id = 100000
for mes in meses:
    for suc in sucursales:
        for seg in segmentos:
            for i in range(rng.integers(120, 180)):
                cliente_id += 1
                canal = rng.choice(canales, p=[0.25,0.15,0.2,0.4])
                hab = rng.choice([0,1], p=[0.35,0.65])
                total = max(0, rng.normal(250000, 100000))
                fact_b2b = total * (rng.uniform(0.15,0.55) if hab else rng.uniform(0.0,0.15))
                rows.append({
                    "Cliente ID": cliente_id,
                    "Sucursal": suc,
                    "Segmento": seg,
                    "Canal": canal,
                    "Mes": mes,
                    "$ TOTAL": round(total,2),
                    "Habilitado B2B": hab,
                    "$ FACT B2B": round(fact_b2b,2)
                })

df = pd.DataFrame(rows)
dup = df.sample(frac=0.01, random_state=1)
df_dirty = pd.concat([df, dup], ignore_index=True)
mask_nulos = df_dirty.sample(frac=0.02, random_state=2).index
df_dirty.loc[mask_nulos, "$ TOTAL"] = np.nan

df_dirty.to_csv("data/raw/ventas_ficticias.csv", index=False)
print("OK -> data/raw/ventas_ficticias.csv")
