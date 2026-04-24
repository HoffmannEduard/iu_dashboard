from datetime import date, timedelta

from models.enums import Modulstatus
from repositories.modulbuchung_repository import ModulbuchungRepository


class DashboardMetrikenService:
    """Berechnet studienabhängige Kennzahlen für die Anzeige im Dashboard"""
    def __init__(self, modulbuchung_repository: ModulbuchungRepository):
        self.modulbuchung_repository = modulbuchung_repository

    def berechne_dashboard_metriken(self, studium) -> dict:
        """
        Berechnet alle relevanten Dashboard-Metriken für ein Studium.

        Args:
            studium: Studium, für das die Metriken berechnet werden sollen.

        Returns:
            Dictionary mit Notendurchschnitt, bestandenen ECTS, voraussichtlichem Enddatum
            und durchschnittlich erreichten ECTS pro Semester.

        Raises:
            -
        """
        abgeschlossene_buchungen = self.modulbuchung_repository.lade_nach_studium_und_status(
            studium_id=studium.id,
            status=Modulstatus.ABGESCHLOSSEN
        )

        # Erreichte ECTS
        gesamt_ects_bestanden = self._berechne_gesamt_ects_bestanden(abgeschlossene_buchungen)
        # Notendurchschnitt
        notendurchschnitt = self._berechne_notendurchschnitt(abgeschlossene_buchungen)
        # Vorraussichtliches Enddatrum
        voraussichtliches_enddatum = self._berechne_voraussichtliches_enddatum(
            startdatum=studium.startdatum,
            gesamt_ects=studium.gesamt_ects,
            bestandene_ects=gesamt_ects_bestanden,
        )
        # Berechnete ECTS pro Semester (inkl. laufendem Semester)
        ects_pro_semester = self._berechne_ects_pro_semester(
            startdatum=studium.startdatum,
            bestandene_ects=gesamt_ects_bestanden,
        )

        return {
            "notendurchschnitt": notendurchschnitt,
            "gesamt_ects_bestanden": gesamt_ects_bestanden,
            "voraussichtliches_enddatum": voraussichtliches_enddatum,
            "ects_pro_semester": ects_pro_semester,
        }

    def _berechne_notendurchschnitt(self, abgeschlossene_buchungen: list) -> float | None:
        """
        Berechnet den durchschnittlichen Notenwert abgeschlossener Modulbuchungen.

        Args:
            abgeschlossene_buchungen: Liste abgeschlossener Modulbuchungen.

        Returns:
            Gerundeter Notendurchschnitt oder None, wenn keine Noten vorhanden sind.

        """
        noten = [
            buchung.pruefungsleistung.note
            for buchung in abgeschlossene_buchungen
            if buchung.pruefungsleistung is not None
        ]

        if not noten:
            return None

        return round(sum(noten) / len(noten), 2)

    def _berechne_gesamt_ects_bestanden(self, abgeschlossene_buchungen: list) -> int:
        """
        Berechnet die Summe der bestandenen ECTS aus abgeschlossenen Modulbuchungen.

        Args:
            abgeschlossene_buchungen: Liste abgeschlossener Modulbuchungen.

        Returns:
            Summe der ECTS-Punkte aller abgeschlossenen Module.
        """
        return sum(
            buchung.modul.ects
            for buchung in abgeschlossene_buchungen
        )

    def _berechne_voraussichtliches_enddatum(
        self,
        startdatum: date,
        gesamt_ects: int,
        bestandene_ects: int
    ) -> date | None:
        """
        Berechnet anhand des bisherigen Studienfortschritts ein voraussichtliches Enddatum.

        Args:
            startdatum: Startdatum des Studiums.
            gesamt_ects: Gesamtzahl der für das Studium benötigten ECTS.
            bestandene_ects: Anzahl der bereits bestandenen ECTS.

        Returns:
            Voraussichtliches Enddatum oder None, wenn keine sinnvolle Prognose möglich ist.
        """
        if bestandene_ects <= 0:
            return None

        heute = date.today()
        vergangene_tage = (heute - startdatum).days

        # Schutz gegen ungültige/future Startdaten
        if vergangene_tage <= 0:
            return None

        rest_ects = max(gesamt_ects - bestandene_ects, 0)

        # Falls bereits fertig studiert, ist das prognostizierte Ende "heute"
        if rest_ects == 0:
            return heute

        tage_pro_ects = vergangene_tage / bestandene_ects
        rest_tage = round(rest_ects * tage_pro_ects)

        return heute + timedelta(days=rest_tage)

    def _berechne_ects_pro_semester(
        self,
        startdatum: date,
        bestandene_ects: int
    ) -> int | None:
        """
        Berechnet die durchschnittlich erreichten ECTS pro Semester.

        Args:
            startdatum: Startdatum des Studiums.
            bestandene_ects: Anzahl der bereits bestandenen ECTS.

        Returns:
            Durchschnittliche ECTS pro Semester oder None, wenn keine Berechnung möglich ist.
        """
        heute = date.today()
        vergangene_tage = (heute - startdatum).days

        # Schutz gegen ungültige/future Startdaten
        if vergangene_tage <= 0:
            return None

        # Laufendes Semester wird anteilig berücksichtigt
        vergangene_semester = vergangene_tage / 182.5  # 6 Monate ≈ 182.5 Tage

        if vergangene_semester <= 0:
            return None

        return round(bestandene_ects / vergangene_semester)