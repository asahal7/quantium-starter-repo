from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).parent
REPO = ROOT.parent
DATA = REPO / "data"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

# Step 1 — Load and combine
files = [DATA / f"daily_sales_data_{i}.csv" for i in range(3)]
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
print(f"Total rows loaded: {len(df)}")

# Step 2 — Clean
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["date"] = pd.to_datetime(df["date"])
df["sales"] = df["price"] * df["quantity"]

# Step 3 — Filter
pink = df[df["product"] == "pink morsel"].copy()
print(f"Date range: {pink['date'].min().date()} to {pink['date'].max().date()}")

# Step 3b — Output formatted CSV (sales, date, region)
output = pink[["sales", "date", "region"]].copy()
output["date"] = output["date"].dt.strftime("%Y-%m-%d")
output.to_csv(REPO / "task2" / "formatted_output.csv", index=False)
print(f"Formatted output saved: {len(output)} rows")

# Step 4 — Aggregate
daily = pink.groupby("date")["sales"].sum().reset_index()
before = pink[pink["date"] < PRICE_INCREASE_DATE]["sales"].sum()
after = pink[pink["date"] >= PRICE_INCREASE_DATE]["sales"].sum()
pct = (after - before) / before * 100
print(f"Sales before {PRICE_INCREASE_DATE.date()}: ${before:,.2f}")
print(f"Sales after  {PRICE_INCREASE_DATE.date()}: ${after:,.2f}  ({pct:+.1f}%)")

# Step 4b — Regional aggregate
regional = pink.groupby(["date", "region"])["sales"].sum().reset_index()

# Step 5 — Visualise
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
fig.suptitle("Pink Morsel Sales Over Time", fontsize=15, fontweight="bold")

# Main chart
ax1.plot(daily["date"], daily["sales"], linewidth=1.2, color="#e05c5c")
ax1.axvline(PRICE_INCREASE_DATE, color="red", linestyle="--", linewidth=1.5)
ax1.text(PRICE_INCREASE_DATE + pd.Timedelta(days=20), ax1.get_ylim()[1] * 0.95,
         "Price increase", color="red", fontsize=9, va="top")
ax1.set_ylabel("Sales ($)")
ax1.grid(axis="y", alpha=0.3)

# Regional breakdown
colours = {"north": "#4c72b0", "south": "#dd8452", "east": "#55a868", "west": "#c44e52"}
for region, grp in regional.groupby("region"):
    ax2.plot(grp["date"], grp["sales"], label=region.title(),
             linewidth=1.1, color=colours.get(region))
ax2.axvline(PRICE_INCREASE_DATE, color="red", linestyle="--", linewidth=1.5)
ax2.set_ylabel("Sales ($)")
ax2.legend(title="Region")
ax2.grid(axis="y", alpha=0.3)
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

plt.tight_layout()
fig.savefig(ROOT / "chart.png", dpi=150, bbox_inches="tight")  # saved in task1/
print("Chart saved to chart.png")
