
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. PROJECT SETUP

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "ncap-son-2026---england-dataset.xlsx"
FIGURES = ROOT / "figures"
RESULTS = ROOT / "results"

FIGURES.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)

INDICATORS = {
    "CBTp": {
        "numerator": "2.1 Numerator",
        "denominator": "2.1 Denominator",
        "reported": "2.1 Percentage standard met"
    },
    "Family Intervention": {
        "numerator": "2.3 Numerator",
        "denominator": "2.3 Denominator",
        "reported": "2.3 Percentage standard met"
    }
}


# 2. LOAD AND PREPARE DATA

df = pd.read_excel(DATA_FILE, header=1)

trusts = df[
    df["ORGID"].astype(str).str.fullmatch(r"ORG\d+")
].copy()

print("NHS trusts:", len(trusts))
print("Duplicate IDs:", trusts["ORGID"].duplicated().sum())

if trusts["ORGID"].duplicated().any():
    raise ValueError("Duplicate NHS trust IDs detected.")

plot_data = {}


# 3. ANALYSE EACH INTERVENTION

for treatment, columns in INDICATORS.items():

    print(f"\n{'=' * 45}")
    print(treatment.upper())
    print("=" * 45)

    data = trusts[
        [
            "ORGID",
            columns["numerator"],
            columns["denominator"],
            columns["reported"]
        ]
    ].copy()

    data.columns = [
        "ORGID",
        "Numerator",
        "Denominator",
        "Reported"
    ]

    for col in ["Numerator", "Denominator", "Reported"]:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

    # DATA VALIDATION

    valid = (
        data[["Numerator", "Denominator", "Reported"]]
        .notna().all(axis=1)
        & (data["Denominator"] > 0)
        & (data["Numerator"] >= 0)
        & (data["Numerator"] <= data["Denominator"])
    )

    print("Invalid records:", (~valid).sum())

    data = data.loc[valid].copy()

    data["Percentage"] = (
        data["Numerator"] /
        data["Denominator"] * 100
    )

    mismatches = (
        (data["Percentage"] - data["Reported"]).abs() > 0.1
    ).sum()

    print("Percentage mismatches:", mismatches)

    # DESCRIPTIVE STATISTICS

    print("\nDescriptive Statistics:")
    print(data["Reported"].describe().round(2))

    # NATIONAL PERCENTAGE

    total_num = data["Numerator"].sum()
    total_den = data["Denominator"].sum()

    national_pct = total_num / total_den * 100

    print(f"\nNational percentage: {national_pct:.2f}%")
    print(f"Numerator: {total_num:.0f}")
    print(f"Denominator: {total_den:.0f}")

    # CORRELATION ANALYSIS

    pearson = data["Denominator"].corr(
        data["Percentage"], method="pearson"
    )

    spearman = data["Denominator"].corr(
        data["Percentage"], method="spearman"
    )

    print(f"\nPearson correlation: {pearson:.3f}")
    print(f"Spearman correlation: {spearman:.3f}")

    # TRUST COMPARISONS

    ranked = data.sort_values(
        "Percentage", ascending=False
    )

    print("\nHighest five:")
    print(
        ranked[
            ["ORGID", "Numerator", "Denominator", "Percentage"]
        ].head(5).round(2).to_string(index=False)
    )

    print("\nLowest five:")
    print(
        ranked[
            ["ORGID", "Numerator", "Denominator", "Percentage"]
        ].tail(5).round(2).to_string(index=False)
    )

    # SENSITIVITY ANALYSIS

    sample_100 = data[data["Denominator"] >= 100]

    print("\nSensitivity Analysis:")
    print("Trusts with 100+ records:", len(sample_100))
    print(
        "Zero percentage trusts:",
        (sample_100["Percentage"] == 0).sum()
    )
    print(
        "Minimum percentage:",
        round(sample_100["Percentage"].min(), 2)
    )
    print(
        "Maximum percentage:",
        round(sample_100["Percentage"].max(), 2)
    )

    # SAVE CSV RESULTS

    filename = treatment.lower().replace(" ", "_")

    ranked.to_csv(
        RESULTS / f"{filename}_trust_results.csv",
        index=False
    )

    # SAVE SCATTER PLOT

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        data["Denominator"],
        data["Percentage"],
        alpha=0.7
    )

    ax.axhline(
        national_pct,
        linestyle="--",
        label=f"National percentage: {national_pct:.1f}%"
    )

    ax.set_title(f"{treatment}: NHS Trust Variation")
    ax.set_xlabel("Number of eligible audited records")
    ax.set_ylabel("Percentage meeting standard (%)")
    ax.set_ylim(0, 105)
    ax.legend()

    fig.tight_layout()

    fig.savefig(
        FIGURES / f"{filename}_scatter.png",
        dpi=300
    )

    plt.close(fig)

    plot_data[treatment] = data["Reported"].reset_index(
        drop=True
    )


# 4. CREATE COMPARATIVE BOX PLOT

fig, ax = plt.subplots(figsize=(8, 5))

pd.DataFrame(plot_data).boxplot(ax=ax)

ax.set_title("Variation in Psychological Intervention Uptake")
ax.set_ylabel("Percentage meeting standard (%)")
ax.set_ylim(0, 105)

fig.tight_layout()

fig.savefig(
    FIGURES / "intervention_variation.png",
    dpi=300
)

plt.close(fig)

print("\nANALYSIS COMPLETED SUCCESSFULLY")
print("Figures saved to:", FIGURES)
print("CSV results saved to:", RESULTS)


