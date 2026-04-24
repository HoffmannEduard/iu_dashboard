from models.enums import Modulstatus, Pruefungsart
from models.modulbuchung import Modulbuchung
from models.pruefungsleistung import Pruefungsleistung
from repositories.modul_repository import ModulRepository
from repositories.modulbuchung_repository import ModulbuchungRepository


class ModulVerwaltungsService:
    """Verwaltet den Lebenszyklus von Modulen und lädt Module nach ihrem Status"""
    def __init__(
        self,
        modul_repository: ModulRepository,
        modulbuchung_repository: ModulbuchungRepository
    ):
        self.modul_repository = modul_repository
        self.modulbuchung_repository = modulbuchung_repository


    # Lebenszyklus der Module (starten, abschließen, löschen)
    def modul_starten(self, studium, modul_id: int) -> Modulbuchung:
        """
        Startet ein Modul für ein Studium und legt dafür eine neue Modulbuchung an.

        Args:
            studium: Studium, für das das Modul gestartet werden soll.
            modul_id: Id des Moduls, das gestartet werden soll.

        Returns:
            Neu gespeicherte Modulbuchung.

        Raises:
            ValueError: Falls das Modul nicht existiert.
            ValueError: Falls das Modul für dieses Studium bereits gebucht wurde.
        """
        modul = self.modul_repository.lade_nach_id(modul_id)

        if modul is None:
            raise ValueError("Das ausgewählte Modul existiert nicht.")

        alle_buchungen = self.modulbuchung_repository.lade_alle()

        buchung_existiert_bereits = any(
            buchung.studium.id == studium.id and buchung.modul.id == modul_id
            for buchung in alle_buchungen
        )

        if buchung_existiert_bereits:
            raise ValueError("Dieses Modul wurde für das Studium bereits gebucht.")

        modulbuchung = Modulbuchung(
            id=None,
            studium=studium,
            modul=modul,
            status=Modulstatus.IN_BEARBEITUNG,
            pruefungsleistung=None
        )

        return self.modulbuchung_repository.speichere(modulbuchung)


    def modul_abschliessen(
        self,
        modulbuchung_id: int,
        pruefungsart: Pruefungsart,
        note: float
    ) -> None:
        """
        Schließt eine Modulbuchung mit einer Prüfungsleistung ab.

        Args:
            modulbuchung_id: Id der Modulbuchung, die abgeschlossen werden soll.
            pruefungsart: Art der Prüfungsleistung.
            note: Note der Prüfungsleistung.

        Raises:
            ValueError: Falls die Modulbuchung nicht existiert.
            ValueError: Falls die Modulbuchung nicht abgeschlossen werden darf.
        """
        modulbuchung = self.modulbuchung_repository.lade_nach_id(modulbuchung_id)

        if modulbuchung is None:
            raise ValueError("Die Modulbuchung existiert nicht.")

        pruefungsleistung = Pruefungsleistung(
            pruefungsart=pruefungsart,
            note=note
        )

        modulbuchung.abschliessen(pruefungsleistung)

        self.modulbuchung_repository.aktualisiere(modulbuchung)


    def modul_loeschen(self, modul_id: int) -> None:
        """
        Löscht ein Modul, wenn es noch nicht gebucht wurde.

        Args:
            modul_id: Id des Moduls, das gelöscht werden soll.

        Raises:
            ValueError: Falls das Modul bereits gestartet wurde.
        """
        alle_buchungen = self.modulbuchung_repository.lade_alle()

        modul_wurde_bereits_gebucht = any(
            buchung.modul.id == modul_id
            for buchung in alle_buchungen
        )

        if modul_wurde_bereits_gebucht:
            raise ValueError(
                "Modul wurde bereits gestartet. Löschen nicht mehr möglich"
            )
        self.modul_repository.loesche(modul_id=modul_id)

    # Module als Listen laden
    def lade_offene_module(self, studium) -> list:
        """
        Lädt alle Module, die für ein Studium noch nicht gebucht wurden.

        Args:
            studium: Studium, für das offene Module geladen werden sollen.

        Returns:
            Liste aller noch offenen Module.
        """
        alle_module = self.modul_repository.lade_alle_module()
        alle_buchungen = self.modulbuchung_repository.lade_alle()

        gebuchte_modul_ids = {
            buchung.modul.id
            for buchung in alle_buchungen
            if buchung.studium.id == studium.id
        }

        return [
            modul for modul in alle_module
            if modul.id not in gebuchte_modul_ids
        ]


    def lade_module_in_bearbeitung(self, studium) -> list[Modulbuchung]:
        """
        Lädt alle Modulbuchungen eines Studiums, die sich in Bearbeitung befinden.

        Args:
            studium: Studium, für das Modulbuchungen in Bearbeitung geladen werden sollen.

        Returns:
            Liste aller Modulbuchungen mit dem Status IN_BEARBEITUNG.
        """
        return self.modulbuchung_repository.lade_nach_studium_und_status(
            studium.id,
            Modulstatus.IN_BEARBEITUNG,
        )


    def lade_abgeschlossene_module(self, studium) -> list[Modulbuchung]:
        """
        Lädt alle abgeschlossenen Modulbuchungen eines Studiums.

        Args:
            studium: Studium, für das abgeschlossene Modulbuchungen geladen werden sollen.

        Returns:
            Liste aller Modulbuchungen mit dem Status ABGESCHLOSSEN.
        """
        return self.modulbuchung_repository.lade_nach_studium_und_status(
            studium.id,
            Modulstatus.ABGESCHLOSSEN,
        )
    