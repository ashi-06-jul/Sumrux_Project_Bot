
import sqlite3


class DB:
    def __init__(self, dbname="details.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS INFO(city text, locality text, pincode integer, modeofcontact text, email text, contact text, req text, board text, standard integer, subjects text, Deal text, confirm text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, Locality, City, Pincode, Modeofcontact, Email, Contact,  Req, Board, Standard, Subjects, Deal, Confirm):
        stmt = "INSERT INTO INFO (Locality, City, Pincode, Email, Contact, Modeofcontact, Req, Board, Standard, Subjects, Deal, Confirm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        args = (Locality, City, Pincode, Modeofcontact, Email, Contact, Req, Board, Standard, Subjects, Deal, Confirm)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT Locality, City, Pincode, Email, mode_of_contact, Req, Board, Standard, Subjects, Deal, Confirm FROM INFO"
        return [x for x in self.conn.execute(stmt)]
