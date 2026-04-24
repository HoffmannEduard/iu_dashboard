from datetime import date

from models.enums import Studienabschluss, Zeitmodell
from repositories.modul_repository import ModulRepository
from repositories.studium_repository import StudiumRepository
from services.validierungs_service import ValidierungsService



class EingabeController:
    """Koordiniert die Eingabeprozesse für Studium und Module"""
    def __init__(
        self,
        studium_repository: StudiumRepository,
        modul_repository: ModulRepository,
        validierungsservice: ValidierungsService
    ):
        self.studium_repository = studium_repository
        self.modul_repository = modul_repository
        self.validierungsservice = validierungsservice

    def speichere_studium(
        self,
        studiengang: str,
        studienabschluss: Studienabschluss,
        startdatum: date,
        zeitmodell: Zeitmodell,
        gesamt_ects: int
    ) -> None:
        """
        Falls noch kein Studium-Objekt gespeichert ist, wird eins erstellt, validiert und gespeichert.
        Falls eins vorhanden ist, wird es überschrieben.

        Args: 
            Benutzereingaben zum Domain-Objekt Studium
        Returns:
             None
        Raises:
            ValueError: Wenn Validierung fehlschlägt
        """
        vorhandenes_studium = self.studium_repository.lade()

        studium = self.validierungsservice.validiere_und_erstelle_studium(
            studiengang=studiengang,
            studienabschluss=studienabschluss,
            startdatum=startdatum,
            zeitmodell=zeitmodell,
            gesamt_ects=gesamt_ects,
            studium_id=vorhandenes_studium.id if vorhandenes_studium else None
        )

        if vorhandenes_studium is None:
            self.studium_repository.speichere(studium)
        else:
            self.studium_repository.aktualisiere(studium)

    def speichere_modul(
        self,
        modul_code: str,
        modul_titel: str,
        ects: int
    ) -> None:
        """
        Erstellt, validiert und speichert ein Modul aus Eingabedaten. 

        Args:
            Alle Eingaben zum Domain-Objekt Modul.
        Returns:
            None
        Raises:
            ValueError: Wenn Validierung fehl schlägt. 
        """
        modul = self.validierungsservice.validiere_und_erstelle_modul(
            modul_code=modul_code,
            modul_titel=modul_titel,
            ects=ects
        )

        self.modul_repository.speichere(modul)