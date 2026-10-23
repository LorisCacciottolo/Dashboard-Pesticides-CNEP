# Surveillance of Pesticide Residues in Ambient Air (France)
**Streamlit Data Storytelling Dashboard — Individual Student Project**

## 1. Project Overview & Narrative Arc
Unlike drinking water or food products, there is currently no regulatory threshold for pesticide residues in ambient air in France. This interactive web application analyzes the **National Exploratory Campaign for Pesticides (CNEP 2018–2019)** conducted by **Anses**, **Ineris**, **LCSQA**, and the **Atmo France (AASQA)** network.

The dashboard follows the following points :
1. **Hook & Context:** Highlights the regulatory gap and explains the methodological challenge of laboratory thresholds (`< LD` and `< LQ`).
2. **Overview & Seasonality:** Tracks key performance indicators (KPIs) and demonstrates the strong spring/summer concentration surge (April–July) driven by agricultural spraying and volatilization.
3. **Deep Dives & Data Quality:** Compares regional/agricultural profiles via an interactive station map, ranks the most persistent molecules (such as banned historical pollutants like *Lindane*), and audits measurement quality.
4. **What-If Simulation & Implications:** Simulates the impact of emission reduction scenarios around residential areas (< 5 km radius) and provides actionable public health recommendations.

## 2. Dataset & License
* **Title:** Résultats de la campagne nationale exploratoire de mesure des résidus de pesticides dans l'air ambiant (CNEP 2018-2019)
* **Portals:** Green Data for Health (GD4H) / LCSQA / data.gouv.fr
* **File used:** `data/Diffusion_Données_Mesures_CNEP.xlsx` (2 relational sheets: `sites de mesures` and `Concentrations mesurées`)
* **License:** Open License / Licence Ouverte Etalab 2.0

## 3. Data Cleaning & Methodological Choices
* **Relational Join:** Merged weekly concentration measurements with station geographical and demographic metadata on `code site`.
* **Analytical Threshold Handling (`< LD` and `< LQ`):** Over 80% of raw laboratory entries fall below the Limit of Detection (`< LD`) or Limit of Quantification (`< LQ`), where raw values represent analytical noise. Following conservative scientific practice (lower-bound hypothesis), unquantified measurements are set to `0.0 ng/m³` in `conc_reelle` to prevent artificial inflation of averages.

## 4. Repository Structure
```text
StApp26_20230878_CACCIOTTOLO_DAI/
├── app.py                 
├── requirements.txt        
├── README.md
├── data/
│   └── Diffusion_Données_Mesures_CNEP.xlsx
├── utils/
│   ├── io.py               
│   ├── prep.py             
│   └── viz.py            
└── sections/
    ├── intro.py         
    ├── overview.py
    ├── deep_dives.py
    └── conclusions.py      