from datetime import date

from models.enums import Studienabschluss, Zeitmodell
from models.modul import Modul
from models.studium import Studium


class ValidierungsService:
    """Service zur Validierung und Erstellung von Domain-Objekten aus Benutzereingaben"""

    def validiere_und_erstelle_studium(
        self,
        studiengang: str,
        studienabschluss: Studienabschluss,
        startdatum: date,
        zeitmodell: Zeitmodell,
        gesamt_ects: int,
        studium_id: int | None = None
    ) -> Studium:
        """
        Validiert Eingabedaten und erstellt ein Studium-Objekt
        Args:
            Alle Attribute der Domain-Klasse Studium (außer ID)
        Returns:
            Ein validiertes Studium-Objekt
        Raises:
            ValueError: Wenn Eingaben ungültig sind
        """
        fehler = []

        bereinigter_studiengang = studiengang.strip() if studiengang else ""

        if not bereinigter_studiengang:
            fehler.append("Studiengang darf nicht leer sein.")

        if studienabschluss is None:
            fehler.append("Studienabschluss muss ausgewählt werden.")

        if startdatum is None:
            fehler.append("Startdatum muss gesetzt sein.")

        if zeitmodell is None:
            fehler.append("Zeitmodell muss ausgewählt werden.")

        if not isinstance(gesamt_ects, int):
            fehler.append("Gesamt-ECTS muss eine ganze Zahl sein.")
        elif gesamt_ects <= 0:
            fehler.append("Gesamt-ECTS muss größer als 0 sein.")

        if fehler:
            raise ValueError("\n".join(fehler))

        return Studium(
            id=studium_id,
            studiengang=bereinigter_studiengang,
            studienabschluss=studienabschluss,
            startdatum=startdatum,
            zeitmodell=zeitmodell,
            gesamt_ects=gesamt_ects
        )
    
    def validiere_und_erstelle_modul(
        self,
        modul_code: str,
        modul_titel: str,
        ects: int,
    ) -> Modul:
        """
        Validiert Eingabedaten und erstellt ein Modul-Objekt
        Args:
            Alle Attribute der Domain-Klasse Modul (außer ID)
        Returns:
            Ein validiertes Modul-Objekt
        Raises:
            ValueError: Wenn Eingaben ungültig sind
        """
        fehler = []

        bereinigter_modul_code = modul_code.strip() if modul_code else ""
        bereinigter_modul_titel = modul_titel.strip() if modul_titel else ""

        if not bereinigter_modul_code:
            fehler.append("Modulcode darf nicht leer sein.")

        if not bereinigter_modul_titel:
            fehler.append("Modultitel darf nicht leer sein.")

        if not isinstance(ects, int):
            fehler.append("ECTS muss eine ganze Zahl sein.")
        elif ects <= 0:
            fehler.append("ECTS muss größer als 0 sein.")

        if fehler:
            raise ValueError("\n".join(fehler))

        return Modul(
            id=None,
            modul_code=bereinigter_modul_code,
            modul_titel=bereinigter_modul_titel,
            ects=ects
        )