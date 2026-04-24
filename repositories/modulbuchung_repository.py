from models.modulbuchung import Modulbuchung
from models.pruefungsleistung import Pruefungsleistung
from models.enums import Modulstatus, Pruefungsart


class ModulbuchungRepository:
    def __init__(self, conn, studium_repository, modul_repository):
        self.conn = conn
        # Weitere Repositories werden übergeben,
        # damit beim Laden aus DB-IDs echte Objekte gebaut werden können.
        self.studium_repository = studium_repository
        self.modul_repository = modul_repository

    def speichere(self, modulbuchung: Modulbuchung) -> Modulbuchung:
        cursor = self.conn.cursor()

        pruefungsart = None
        note = None

        if modulbuchung.pruefungsleistung is not None:
            pruefungsart = modulbuchung.pruefungsleistung.pruefungsart.value
            note = modulbuchung.pruefungsleistung.note

        cursor.execute("""
            INSERT INTO modulbuchung (
                studium_id, modul_id, status, pruefungsart, note
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            modulbuchung.studium.id,
            modulbuchung.modul.id,
            modulbuchung.status.value,
            pruefungsart,
            note
        ))
        self.conn.commit()

        # Die von SQLite erzeugte ID wird ins Objekt zurückgeschrieben.
        modulbuchung.id = cursor.lastrowid
        return modulbuchung

    def aktualisiere(self, modulbuchung: Modulbuchung) -> Modulbuchung:
        cursor = self.conn.cursor()

        pruefungsart = None
        note = None

        if modulbuchung.pruefungsleistung is not None:
            pruefungsart = modulbuchung.pruefungsleistung.pruefungsart.value
            note = modulbuchung.pruefungsleistung.note

        cursor.execute("""
            UPDATE modulbuchung
            SET status = ?, pruefungsart = ?, note = ?
            WHERE id = ?
        """, (
            modulbuchung.status.value,
            pruefungsart,
            note,
            modulbuchung.id
        ))
        self.conn.commit()

        return modulbuchung

    def lade_alle(self) -> list[Modulbuchung]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, studium_id, modul_id, status, pruefungsart, note
            FROM modulbuchung
        """)
        rows = cursor.fetchall()

        # Gemeinsame Mapping-Methode nutzen, um Dopplung zu vermeiden.
        return [self._row_to_modulbuchung(row) for row in rows]

    def lade_nach_id(self, modulbuchung_id: int) -> Modulbuchung | None:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, studium_id, modul_id, status, pruefungsart, note
            FROM modulbuchung
            WHERE id = ?
        """, (modulbuchung_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_modulbuchung(row)

    def lade_nach_studium_und_status(
        self,
        studium_id: int,
        status: Modulstatus
    ) -> list[Modulbuchung]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, studium_id, modul_id, status, pruefungsart, note
            FROM modulbuchung
            WHERE studium_id = ? AND status = ?
        """, (studium_id, status.value))
        rows = cursor.fetchall()

        return [self._row_to_modulbuchung(row) for row in rows]

    def _row_to_modulbuchung(self, row) -> Modulbuchung:
        pruefungsleistung = None

        if row[4] is not None:
            pruefungsleistung = Pruefungsleistung(
                pruefungsart=Pruefungsart(row[4]),
                note=row[5]
            )

        # IDs aus der Datenbank werden in Domain-Objekte aufgelöst.
        studium = self.studium_repository.lade_nach_id(row[1])
        modul = self.modul_repository.lade_nach_id(row[2])

        return Modulbuchung(
            id=row[0],
            studium=studium,
            modul=modul,
            status=Modulstatus(row[3]),
            pruefungsleistung=pruefungsleistung
        )