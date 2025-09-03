import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
Path("data/clean").mkdir(parents=True, exist_ok=True)

df = pd.read_csv("data/raw/ventas_ficticias.csv")
print("Original:", df.shape)

# 1) Remover duplicados exactos
df = df.drop_duplicates()

# 2) Imputar nulos de $ TOTAL con mediana por Sucursal+Mes
df["$ TOTAL"] = df.groupby(["Sucursal","Mes"])["$ TOTAL"].transform(
    lambda s: s.fillna(s.median())
)

# 3) Reglas básicas
df = df[df["$ TOTAL"] >= 0]
df["% FACT B2B"] = (df["$ FACT B2B"] / df["$ TOTAL"]).clip(0,1)

df.to_csv("data/clean/ventas_ficticias_clean.csv", index=False)
print("Clean:", df.shape)

# Mini EDA
eda = (df.groupby(["Sucursal","Mes"])
         .agg(habilitados=("Habilitado B2B","mean"),
              fact_b2b_pct=("% FACT B2B","mean"),
              total=("$ TOTAL","sum"))
         .reset_index())

# Gráfico rápido (por sucursal)
for suc in df["Sucursal"].unique():
    aux = eda[eda["Sucursal"]==suc].sort_values("Mes")
    plt.figure()
    plt.plot(aux["Mes"], aux["habilitados"])
    plt.title(f"Tasa Habilitados B2B - {suc}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"data/clean/habilitados_{suc}.png")
    plt.close()
print("EDA PNGs en data/clean/")
