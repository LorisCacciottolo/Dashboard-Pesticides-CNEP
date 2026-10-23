from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EXCEL_PATH = ROOT / "data" / "Diffusion_Données_Mesures_CNEP.xlsx"


## We load the data of our excel file and we strip the column names.
def load_data():
    df_sites = pd.read_excel(EXCEL_PATH, sheet_name="sites de mesures", header=1)
    df_conc = pd.read_excel(EXCEL_PATH, sheet_name="Concentrations mesurées", header=1)

    df_sites.columns = df_sites.columns.str.strip()
    df_conc.columns = df_conc.columns.str.strip()

    return df_sites, df_conc