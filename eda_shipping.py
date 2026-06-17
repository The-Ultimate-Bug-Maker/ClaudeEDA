import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
os.makedirs("eda_outputs", exist_ok=True)

df = pd.read_excel("shipping_data.xlsx", parse_dates=["Ship Date", "Delivery Date"])

# ── 1. BASIC INFO ────────────────────────────────────────────────────────────
print("=" * 60)
print("SHAPE:", df.shape)
print("\nDTYPES:\n", df.dtypes)
print("\nMISSING VALUES:\n", df.isnull().sum())

# ── 2. SUMMARY STATISTICS ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY STATISTICS (numeric):")
print(df[["Transit Days", "Weight (lbs)", "Shipping Cost ($)"]].describe().round(2))

print("\nCATEGORICAL COUNTS:")
for col in ["Carrier", "Status", "Category", "On Time"]:
    print(f"\n{col}:\n{df[col].value_counts()}")

# ── 3. ON-TIME RATE BY CARRIER ───────────────────────────────────────────────
on_time_rate = (
    df.groupby("Carrier")["On Time"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .reset_index()
    .rename(columns={"On Time": "On Time Rate (%)"})
    .sort_values("On Time Rate (%)", ascending=False)
)
print("\nON-TIME RATE BY CARRIER:\n", on_time_rate)

# ── 4. AVG SHIPPING COST BY CARRIER ─────────────────────────────────────────
avg_cost = df.groupby("Carrier")["Shipping Cost ($)"].mean().sort_values(ascending=False)
print("\nAVG SHIPPING COST BY CARRIER:\n", avg_cost.round(2))

# ── 5. AVG TRANSIT DAYS BY CARRIER ──────────────────────────────────────────
avg_transit = df.groupby("Carrier")["Transit Days"].mean().sort_values()
print("\nAVG TRANSIT DAYS BY CARRIER:\n", avg_transit.round(2))

# ════════════════════════════════════════════════════════════════════════════
# PLOTS
# ════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle("Shipping Data EDA", fontsize=18, fontweight="bold", y=1.01)

# Plot 1 — Shipments by Carrier
carrier_counts = df["Carrier"].value_counts()
axes[0, 0].bar(carrier_counts.index, carrier_counts.values, color=sns.color_palette("tab10"))
axes[0, 0].set_title("Shipments by Carrier")
axes[0, 0].set_xlabel("Carrier")
axes[0, 0].set_ylabel("Count")
axes[0, 0].tick_params(axis="x", rotation=20)

# Plot 2 — Shipment Status Distribution
status_counts = df["Status"].value_counts()
axes[0, 1].pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%", startangle=140)
axes[0, 1].set_title("Shipment Status Distribution")

# Plot 3 — On-Time Rate by Carrier
axes[0, 2].barh(on_time_rate["Carrier"], on_time_rate["On Time Rate (%)"], color="steelblue")
axes[0, 2].set_title("On-Time Rate by Carrier (%)")
axes[0, 2].set_xlabel("On-Time Rate (%)")
axes[0, 2].axvline(75, color="red", linestyle="--", label="Overall avg")
axes[0, 2].legend()

# Plot 4 — Shipping Cost Distribution
axes[1, 0].hist(df["Shipping Cost ($)"], bins=30, color="coral", edgecolor="white")
axes[1, 0].set_title("Shipping Cost Distribution")
axes[1, 0].set_xlabel("Cost ($)")
axes[1, 0].set_ylabel("Frequency")

# Plot 5 — Weight vs Shipping Cost
axes[1, 1].scatter(df["Weight (lbs)"], df["Shipping Cost ($)"], alpha=0.4, color="mediumseagreen")
axes[1, 1].set_title("Weight vs Shipping Cost")
axes[1, 1].set_xlabel("Weight (lbs)")
axes[1, 1].set_ylabel("Shipping Cost ($)")

# Plot 6 — Transit Days Distribution
axes[1, 2].hist(df["Transit Days"], bins=14, color="mediumpurple", edgecolor="white", rwidth=0.8)
axes[1, 2].set_title("Transit Days Distribution")
axes[1, 2].set_xlabel("Transit Days")
axes[1, 2].set_ylabel("Frequency")
axes[1, 2].xaxis.set_major_locator(mticker.MultipleLocator(1))

# Plot 7 — Avg Shipping Cost by Category
avg_cost_cat = df.groupby("Category")["Shipping Cost ($)"].mean().sort_values(ascending=False)
axes[2, 0].bar(avg_cost_cat.index, avg_cost_cat.values, color=sns.color_palette("pastel"))
axes[2, 0].set_title("Avg Shipping Cost by Category")
axes[2, 0].set_xlabel("Category")
axes[2, 0].set_ylabel("Avg Cost ($)")
axes[2, 0].tick_params(axis="x", rotation=20)

# Plot 8 — Shipments by Origin
origin_counts = df["Origin"].value_counts()
axes[2, 1].barh(origin_counts.index, origin_counts.values, color="sandybrown")
axes[2, 1].set_title("Shipments by Origin City")
axes[2, 1].set_xlabel("Count")

# Plot 9 — Avg Cost by Carrier
axes[2, 2].bar(avg_cost.index, avg_cost.values, color=sns.color_palette("muted"))
axes[2, 2].set_title("Avg Shipping Cost by Carrier")
axes[2, 2].set_xlabel("Carrier")
axes[2, 2].set_ylabel("Avg Cost ($)")
axes[2, 2].tick_params(axis="x", rotation=20)

plt.tight_layout()
plt.savefig("eda_outputs/eda_shipping.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nPlots saved to eda_outputs/eda_shipping.png")
