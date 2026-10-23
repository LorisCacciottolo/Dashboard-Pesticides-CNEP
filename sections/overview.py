import streamlit as st
from utils.viz import line_chart_saisonnalite


def show_overview(df_filtre):
    st.markdown("## 2. The Air Quality depends on the Agricultural Calendar")

    st.markdown(
        "> **Key Insight:** *Atmospheric pesticide contamination is not a constant, it follows a sharp "
        "seasonal wave that surges between April and July, driven by spring crop treatments and warmer temperatures.*"
    )

    st.write(
        """
        Notice the contrast between the Quantification Rate (how often a pesticide is present above laboratory 
        thresholds) and the Average Concentration (expressed in nanograms per cubic meter of air, $\\text{ng/m}^3$).
        """
    )

    nb_mesures = len(df_filtre)
    taux_quantif = df_filtre["est_quantifie"].mean() * 100 if nb_mesures > 0 else 0
    conc_moy = df_filtre["conc_reelle"].mean() if nb_mesures > 0 else 0
    conc_max = df_filtre["conc_reelle"].max() if nb_mesures > 0 else 0
    nb_sites = df_filtre["code site"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Analyzed Lab Samples",
        f"{nb_mesures:,}".replace(",", " "),
        help="Total number of weekly substance measurements.",
    )
    c2.metric(
        "Active Monitoring Sites",
        f"{nb_sites} stations",
        help="Number of distinct AASQA geographical stations included in the selection.",
    )
    c3.metric(
        "Quantification Rate (> LQ)",
        f"{taux_quantif:.1f} %",
        help="Percentage of samples where the pesticide concentration strictly exceeded the laboratory Limit of Quantification.",
    )
    c4.metric(
        "Mean Concentration ( Peak Max )",
        f"{conc_moy:.3f} ng/m³",
        delta=f"Max: {conc_max:.1f} ng/m³",
        delta_color="off",
        help="Conservative mean concentration (setting < LQ values to 0 ng/m³) alongside the highest single weekly spike observed.",
    )

    st.plotly_chart(line_chart_saisonnalite(df_filtre), use_container_width=True)

    # Narrative reading guide under the chart
    st.caption(
        "Each line tracks the monthly average concentration grouped by the dominant agricultural "
        "activity within a 5 km radius of the sensor. The orange band highlights the Spring–Summer spraying window (April–July). "
        "During winter, cold temperatures keep volatilization near zero, whereas late spring "
        "triggers simultaneous fungicide and herbicide peaks, especially around vineyards and large crops."
    )