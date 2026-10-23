import streamlit as st
from utils.viz import bar_chart_qualite, bar_chart_top_substances, map_chart_sites


def show_deep_dives(df_filtre):
    st.markdown("## 3. Deep Dives: Geography, Ghost Pollutants, and Data Quality")

    st.markdown(
        "> **Key Insight:** *Regions with vineyards and large crops have the highest pollution levels. "
        "However, the most detected pesticide in France is Lindane, even though it was banned in 1998.*"
    )

    st.write(
        """
        Are cities protected from agricultural pesticides? What chemicals are we really breathing? 
        Looking at the map and the data, we can see two main things:

        1. The highest pesticide levels are found near intensive farming areas (like vineyards or large crop fields).
        2. Pesticides spread through the air to cities, and old banned chemicals still evaporate from the soil today.
        """
    )

    col_map, col_bar = st.columns([1.15, 1])

    with col_map:
        st.markdown("#### Map of Monitoring Stations")
        st.plotly_chart(map_chart_sites(df_filtre), use_container_width=True)
        st.caption(
            " The size of the bubble shows the average pesticide concentration ($\\text{ng/m}^3$). "
            "The color shows the main crop grown around the station."
        )

    with col_bar:
        st.markdown("#### Top Substances in the Ambient Air")
        top_n = st.slider(
            "Select the number of top substances to rank:",
            min_value=5,
            max_value=20,
            value=10,
        )
        st.plotly_chart(bar_chart_top_substances(df_filtre, top_n=top_n), use_container_width=True)
        st.caption(
            "Lindane was banned in 1998, but it is still the most frequently found substance "
            "(detected in ~75-80% of samples), although at low concentrations (blue bar). On the other hand, currently used pesticides "
            "like Prosulfocarbe and Folpel show much higher concentrations (yellow/orange bars) during spraying seasons."
        )

    st.divider()

    st.markdown("### Data Quality Audit & Limitations")
    st.write(
        """
        All samples were checked by the **LCSQA** (a national air quality laboratory). The chart below shows 
        how many samples were actually above the detection limits.
        """
    )

    col_q1, col_q2 = st.columns([1.3, 1])

    with col_q1:
        st.plotly_chart(bar_chart_qualite(df_filtre), use_container_width=True)

    with col_q2:
        nb_valeurs_manquantes = int(df_filtre["valeur brute"].isna().sum())
        nb_doublons = int(df_filtre.duplicated().sum())
        pct_sous_seuil = (1 - df_filtre["est_quantifie"].mean()) * 100 if len(df_filtre) > 0 else 0
        incertitude_moy = df_filtre["Incertitude de mesure (%)"].mean() if len(df_filtre) > 0 else 0
        rendement_moy = df_filtre["Rendement d'extraction (%)"].mean() if len(df_filtre) > 0 else 0

        st.info(
            f"**Data Quality Summary:**\n\n"
            f"- **Missing values (`NaN`):** `{nb_valeurs_manquantes}`\n"
            f"- **Duplicate rows:** `{nb_doublons}`\n"
            f"- **Values below detection limits (`< LD` or `< LQ`):** `{pct_sous_seuil:.1f} %` of total samples\n"
            f"- **Average lab extraction yield:** `{rendement_moy:.1f} %`\n"
            f"- **Average measurement uncertainty:** `± {incertitude_moy:.1f} %`\n\n"
            "**Note on our methodology:**\n"
            "By replacing `< LQ` values with `0.0 ng/m³`, we made a conservative choice (lower bound). "
            "If we used a higher value for these unknown numbers, the winter averages would look artificially high."
        )