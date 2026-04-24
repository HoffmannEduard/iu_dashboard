import streamlit as st

from models.studium import Studium


def render_dashboard_metriken(
    studium: Studium,
    notendurchschnitt: float | None,
    gesamt_ects_bestanden: int,
    voraussichtliches_enddatum,
    ects_pro_semester: int | None,
) -> None:
    """Rendert die zentralen Kennzahlen des Studiums im Dashboard"""
    gesamt_ects = studium.gesamt_ects or 0

    if gesamt_ects > 0:
        fortschritt = gesamt_ects_bestanden / gesamt_ects
        fortschritt = max(0.0, min(fortschritt, 1.0))
    else:
        fortschritt = 0.0

    fortschritt_prozent = round(fortschritt * 100)

    col1, col2, col3, col4 = st.columns(4)

    # Notendurchschnitt
    with col1:
        with st.container(border=True):
            st.caption("Notendurchschnitt")
            if notendurchschnitt is None:
                st.subheader("-")
            else:
                st.subheader(f"{notendurchschnitt:.2f}")

    # Studienfortschritt
    with col2:
        with st.container(border=True):
            st.caption("Studienfortschritt")

            st.subheader(f"{gesamt_ects_bestanden} / {gesamt_ects} ECTS")
            st.caption(f"{fortschritt_prozent} % erreicht")

            st.progress(fortschritt)

    # Berechnetes, vorraussichtliches Enddatum
    with col3:
        with st.container(border=True):
            st.caption("Voraussichtliches Enddatum")

            if voraussichtliches_enddatum is None:
                st.subheader("-")
                st.caption("Noch nicht berechenbar")
            else:
                st.subheader(voraussichtliches_enddatum.strftime("%d.%m.%Y"))

    # Durchschnittliche ECTS pro Semester
    with col4:
        with st.container(border=True):
            st.caption("Ø ECTS / Semester")

            if ects_pro_semester is None:
                st.subheader("-")
                st.caption("Noch nicht berechenbar")
            else:
                st.subheader(f"{ects_pro_semester}")