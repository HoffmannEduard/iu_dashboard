import streamlit as st


def render_dashboard_header(studium) -> None:
    """Rendert das erfasste Studium"""
    st.subheader(
        f"{studium.studiengang} {studium.studienabschluss.value} "
        f"({studium.gesamt_ects} ECTS)"
    )
    st.write(
        f"**{studium.zeitmodell.value}**: "
        f"Vom {studium.startdatum} bis {studium.enddatum}"
    )