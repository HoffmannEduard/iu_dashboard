from datetime import date

from models.studium import Studium
from models.enums import Studienabschluss, Zeitmodell


class StudiumRepository:
    def __init__(self, conn):
        self.conn = conn

    def speichere(self, studium: Studium) -> Studium:
        cursor = self.conn.cursor()

        # Die Datenbank soll die ID vergeben.
        cursor.execute("""
            INSERT INTO studium (
                studiengang, studienabschluss, startdatum, zeitmodell, gesamt_ects
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            studium.studiengang,
            studium.studienabschluss.value,
            studium.startdatum.isoformat(),
            studium.zeitmodell.value,
            studium.gesamt_ects
        ))
        self.conn.commit()

        # Die von der Datenbank erzeugte ID wird zurück ins Objekt geschrieben.
        studium.id = cursor.lastrowid
        return studium

    def lade(self) -> Studium | None:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, studiengang, studienabschluss, startdatum, zeitmodell, gesamt_ects
            FROM studium
            LIMIT 1
        """)
        row = cursor.fetchone()

        if row is None:
            return None

        # Mapping in eigene Hilfsmethode ausgelagert
        return self._row_to_studium(row)

    def lade_nach_id(self, studium_id: int) -> Studium | None:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, studiengang, studienabschluss, startdatum, zeitmodell, gesamt_ects
            FROM studium
            WHERE id = ?
        """, (studium_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        # Notwendig für andere Repositories
        return self._row_to_studium(row)

    def aktualisiere(self, studium: Studium) -> None:
        # Schutz gegen Update ohne ID.
        if studium.id is None:
            raise ValueError("Studium kann ohne ID nicht aktualisiert werden.")

        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE studium
            SET studiengang = ?, studienabschluss = ?, startdatum = ?, zeitmodell = ?, gesamt_ects = ?
            WHERE id = ?
        """, (
            studium.studiengang,
            studium.studienabschluss.value,
            studium.startdatum.isoformat(),
            studium.zeitmodell.value,
            studium.gesamt_ects,
            studium.id
        ))
        self.conn.commit()

    def _row_to_studium(self, row) -> Studium:
        # Zentrale Mapping-Methode für DB-Zeile -> Domain-Objekt.
        return Studium(
            id=row[0],
            studiengang=row[1],
            studienabschluss=Studienabschluss(row[2]),
            startdatum=date.fromisoformat(row[3]),
            zeitmodell=Zeitmodell(row[4]),
            gesamt_ects=row[5]
        )