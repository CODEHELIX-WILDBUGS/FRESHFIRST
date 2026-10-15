import json, os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # fixed seed so results repeat
os.makedirs("data", exist_ok=True)

# commodity: (base price Rs/kg, max shelf-life days)
COMM = {"Tomato": (25, 6), "Banana": (40, 8), "Spinach": (30, 4), "Mango": (80, 7)}
names = list(COMM)

# 12 inventory batches
batches = []
for i in range(12):
    c = names[i % 4]
    batches.append({
        "batch_id": f"B{i+1:02d}",
        "commodity": c,
        "quantity_kg": int(rng.integers(4, 17)) * 50,
        "shelf_life_days": int(rng.integers(2, COMM[c][1] + 1)),
    })
pd.DataFrame(batches).to_csv("data/batches.csv", index=False)

# 4 destination markets
dest = pd.DataFrame([
    {"dest_id": "MarketA", "transport_days": 1, "cost_per_kg": 2.0, "capacity_kg": 1500},
    {"dest_id": "MarketB", "transport_days": 2, "cost_per_kg": 3.0, "capacity_kg": 1500},
    {"dest_id": "MarketC", "transport_days": 3, "cost_per_kg": 4.5, "capacity_kg": 1200},
    {"dest_id": "MarketD", "transport_days": 1, "cost_per_kg": 2.5, "capacity_kg": 800},
])
dest.to_csv("data/destinations.csv", index=False)

# demand and price per destination and commodity
rows = []
for d in dest["dest_id"]:
    for c in names:
        rows.append({
            "dest_id": d,
            "commodity": c,
            "demand_kg": int(rng.integers(2, 11)) * 50,
            "price_per_kg": round(COMM[c][0] * rng.uniform(0.9, 1.2), 1),
        })
pd.DataFrame(rows).to_csv("data/demand.csv", index=False)

# cost model: same rules for baseline and our plan (assumptions, synthetic)
cost = {"handling_cost_per_kg": 1.0, "spoilage_disposal_cost_per_kg": 2.0,
        "discount_rate": 0.15}
with open("data/cost_model.json", "w") as f:
    json.dump(cost, f, indent=2)

print(pd.read_csv("data/batches.csv"))
print("Total stock (kg):", sum(b["quantity_kg"] for b in batches))
