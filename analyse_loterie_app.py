
import streamlit as st
from collections import Counter

st.set_page_config(page_title="Analyse Loterie", layout="centered")

st.title("🔢 Analyseur de Loterie (0 à 36)")

st.markdown("**Entrez vos suites de numéros, une par ligne, séparés par des virgules.**")
raw_input = st.text_area("Exemple :", "13,26,18,8,21,0,26\n17,22,11,6,6,15,34")

if st.button("Analyser"):
    try:
        suites = [[int(n) for n in line.split(",")] for line in raw_input.strip().split("\n")]
        all_numbers = [n for suite in suites for n in suite]
        counter = Counter(all_numbers)

        last_seen = {}
        gap_counter = {}
        for i, suite in enumerate(suites):
            for num in range(37):
                if num in suite:
                    last_seen[num] = i
        for num in range(37):
            if num in last_seen:
                gap_counter[num] = len(suites) - 1 - last_seen[num]
            else:
                gap_counter[num] = len(suites)

        duplicates_per_suite = [set([x for x, c in Counter(s).items() if c > 1]) for s in suites]
        doublon_set = set().union(*duplicates_per_suite)

        sorted_by_gap = sorted(gap_counter.items(), key=lambda x: -x[1])
        recommandations = [num for num, gap in sorted_by_gap if num not in doublon_set][:3]

        st.subheader("📊 Résultats")
        data = {
            "Numéro": list(range(37)),
            "Fréquence": [counter.get(i, 0) for i in range(37)],
            "Écart": [gap_counter.get(i, len(suites)) for i in range(37)],
            "Doublon": ["Oui" if i in doublon_set else "Non" for i in range(37)]
        }
        st.dataframe(data, use_container_width=True)

        st.success(f"🎯 Numéros recommandés : **{', '.join(map(str, recommandations))}**")
    except Exception as e:
        st.error(f"❌ Erreur de format ou de saisie : {e}")
