# Investigating Variation in Psychological Intervention Access for Early Psychosis in England

**An independent Health Data Science project using Python and the 2026 National Clinical Audit of Psychosis (NCAP).**

## Project Overview

This project investigates variation in the recorded achievement of psychological intervention standards across **49 NHS trusts in England**, focusing on Cognitive Behavioural Therapy for Psychosis (CBTp) and family intervention within Early Intervention in Psychosis (EIP) services.

Drawing on my background in Mental Health Nursing, I developed this project to apply Python, statistical analysis and clinical reasoning to routinely collected healthcare data. The findings describe **recorded audit performance**, not necessarily the full extent or quality of care delivered.

## Research Question

**How does recorded achievement of CBTp and family intervention standards vary across NHS trusts in England?**

The analysis aims to describe variation, compare trust-level and national summaries, explore associations with eligible audited record counts, and check the robustness and internal consistency of the reported data.

## Key Findings

### National and trust-level summaries

| Indicator | Mean across 49 trusts | National percentage | Trust-level range |
|---|---:|---:|---:|
| CBTp | 41.18% | 42.26% | 0% to 99.57% |
| Family intervention | 35.75% | 35.32% | 0% to 100% |

National percentages were calculated from summed numerators and denominators rather than by averaging trust percentages. The indicators have different eligible denominators, so they should not be treated as measurements of the same population.

### Correlations with eligible audited record counts

| Indicator | Pearson correlation | Spearman correlation |
|---|---:|---:|
| CBTp | 0.073 | 0.039 |
| Family intervention | -0.031 | 0.028 |

All four coefficients were close to zero, suggesting little observed linear or monotonic association in these **49 aggregated trust records**. Eligible audited record counts are not a direct measure of overall service size, and these exploratory correlations cannot establish causation.

### Sensitivity analysis and validation

Using an exploratory threshold of at least **100 eligible records**, 42 trusts remained in the CBTp analysis and 40 in the family intervention analysis. Extreme recorded percentages persisted, suggesting that small denominators alone do not explain the observed variation.

For the selected indicators, the script found **no duplicate trust IDs, missing numerical values, invalid numerator–denominator combinations or discrepancies greater than 0.1 percentage points** between recalculated and reported values. These checks establish internal consistency only; they cannot verify the completeness of underlying clinical documentation.

## Visualisations

### Distribution of recorded intervention percentages

![Box plots comparing CBTp and family intervention across NHS trusts](figures/intervention_variation.png)

### CBTp percentages and eligible audited records

![Scatter plot of CBTp percentage versus eligible audited records](figures/cbtp_scatter.png)

### Family intervention percentages and eligible audited records

![Scatter plot of family intervention percentage versus eligible audited records](figures/family_intervention_scatter.png)

## Methodology at a Glance

1. **Data preparation:** Imported the Excel workbook with Pandas, selected 49 trust records and excluded the national summary to avoid double counting.
2. **Descriptive analysis:** Calculated means, medians, quartiles, standard deviations and percentage ranges.
3. **National summaries:** Calculated intervention percentages from summed valid numerators and denominators.
4. **Exploratory association:** Used Pearson and Spearman correlations and scatter plots to examine relationships with eligible audited record counts.
5. **Trust comparisons:** Examined the highest and lowest recorded percentages alongside their numerators and denominators.
6. **Sensitivity analysis:** Repeated extreme-value checks for trusts with at least 100 eligible records; this is an exploratory threshold, not an official NCAP cutoff.
7. **Validation:** Checked duplicates, missing data, numerical validity and agreement with published percentages.

See [the full research report](report.md) for detailed methods, results, discussion and limitations.

## Data Source

**Dataset:** [National Clinical Audit of Psychosis (NCAP), England, 2026](https://www.data.gov.uk/dataset/4764dc2f-31b4-4713-92a9-d54260c0b65c/national-clinical-audit-of-psychosis-ncap-2026).

**Publisher:** Healthcare Quality Improvement Partnership (HQIP). **Audit delivery:** Royal College of Psychiatrists. The England audit uses routinely collected Mental Health Services Data Set (MHSDS) information.

The source workbook is not included in this repository. Readers can obtain it from the linked official dataset page.

## Tools

Python, Pandas, OpenPyXL, Matplotlib, SciPy, Git and GitHub.

## Reproduce the Analysis

1. Download or clone this repository.
2. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Download the England 2026 Excel workbook from the dataset link above and save it in the repository root as `ncap-son-2026---england-dataset.xlsx`.
4. Run:

   ```bash
   python analysis.py
   ```

The script saves three PNG charts to `figures/` and trust-level CSV results to `results/`.

## Limitations

This is an observational analysis of aggregated, routinely collected data. Reported percentages may be influenced by eligibility criteria, documentation completeness, variation in service provision and differences in the populations served. CBTp and family intervention use different denominators; their percentages are not directly comparable as patient outcomes. The results do not identify the causes of variation or establish that one trust provides better care than another.

## Project Status

**Core Python analysis complete.** Final academic reference checks and portfolio review are in progress.

## Attribution

Data originate from the 2026 National Clinical Audit of Psychosis, published by HQIP. This project is an independent secondary analysis and is not affiliated with or endorsed by the dataset publisher or the Royal College of Psychiatrists. Consult the official dataset listing for the applicable reuse terms.
