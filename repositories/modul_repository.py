from models.modul import Modul


class ModulRepository:
    def __init__(self, conn):
        self.conn = conn

    def speichere(self, modul: Modul) -> Modul:
        cursor = self.conn.cursor()

        # Die Datenbank soll die ID automatisch vergeben.
        cursor.execute("""
            INSERT INTO modul (
                modul_code, modul_titel, ects
            ) VALUES (?, ?, ?)
        """, (
            modul.modul_code,
            modul.modul_titel,
            modul.ects
        ))
        self.conn.commit()

        # Die von der Datenbank erzeugte ID wird zurück ins Objekt geschrieben.
        modul.id = cursor.lastrowid
        return modul

    def lade_alle_module(self) -> list[Modul]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, modul_code, modul_titel, ects
            FROM modul
        """)
        rows = cursor.fetchall()

        return [self._row_to_modul(row) for row in rows]

    def lade_nach_id(self, modul_id: int) -> Modul | None:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, modul_code, modul_titel, ects
            FROM modul
            WHERE id = ?
        """, (modul_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_modul(row)
    

    def loesche(self, modul_id: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM modul
            WHERE id = ?
        """, (modul_id,))
        self.conn.commit()

    def _row_to_modul(self, row) -> Modul:
        # Zentrale Mapping-Methode für DB-Zeile -> Domain-Objekt.
        return Modul(
            id=row[0],
            modul_code=row[1],
            modul_titel=row[2],
            ects=row[3]
        )