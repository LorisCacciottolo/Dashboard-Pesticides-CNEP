import streamlit as st


def show_conclusions(df_filtre):
    st.markdown("## 4. Policy Simulator, Key Takeaways & Implications")

    st.markdown(
        "> **Key Takeaway:** *To reduce pesticides in the air, we must control spraying during spring and create larger pesticide-free zones around homes.*"
    )

    st.write(
        """
        How many people live near these monitoring stations? And what would happen if new environmental rules successfully 
        reduced pesticide emissions?
        """
    )

    st.markdown("#### 'What-If' Simulator: Reducing Pesticide Emissions")

    col_slider, col_explanation = st.columns([1.2, 1])
    with col_slider:
        reduction_pct = st.slider(
            "Simulate a reduction in agricultural pesticide emissions (%):",
            min_value=0,
            max_value=80,
            value=30,
            step=5,
        )

    conc_actuelle = df_filtre["conc_reelle"].mean() if len(df_filtre) > 0 else 0
    conc_simulee = conc_actuelle * (1 - reduction_pct / 100)

    sites_uniques = df_filtre.drop_duplicates(subset=["code site"])
    pop_exposee = sites_uniques["pop_5km"].astype(float).sum() if len(sites_uniques) > 0 else 0
    dist_moyenne = sites_uniques["distance_parcelle_m"].astype(float).mean() if len(sites_uniques) > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Average", f"{conc_actuelle:.3f} ng/m³")
    c2.metric(
        "Simulated Average",
        f"{conc_simulee:.3f} ng/m³",
        delta=f"-{reduction_pct} %",
        delta_color="inverse",
    )
    c3.metric(
        "Resident Population (< 5 km)",
        f"{int(pop_exposee):,}".replace(",", " ") + " inhab.",
        help="Number of people living within 5 km of the selected stations.",
    )
    c4.metric(
        "Avg. Distance to Nearest Field",
        f"{dist_moyenne:.0f} m",
        help="Average distance between the sensors and the closest agricultural field.",
    )

    st.divider()

    col_ins, col_lim = st.columns(2)

    with col_ins:
        st.success(
            "**Summary & Policy Ideas**\n\n"
            "1. **Focus on Spring:** Since most pollution happens between April and August, the government should measure air quality more often during these months.\n"
            "2. **Stricter Weather Rules:** Some chemicals evaporate very easily. We need stricter rules to stop spraying on hot or windy days.\n"
            "3. **Cities are not immune:** Wind carries these molecules. People living in cities still breathe a mix of low-dose chemicals all year round."
        )

    with col_lim:
        st.warning(
            "**Scientific Limitations to keep in mind**\n\n"
            "- **Presence ≠ Danger:** Detecting a chemical does not mean it will immediately make you sick. We still lack official health safety limits for breathing most of these pesticides.\n"
            "- **The 'Cocktail Effect':** Our sensors measure chemicals one by one. But breathing a mix of several different pesticides at the same time might be more dangerous.\n"
            "- **Local Weather:** 50 stations is a good national start, but local winds and hills change how pesticides travel in real life."
        )