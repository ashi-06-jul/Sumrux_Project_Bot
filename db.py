
import sqlite3


class DB:
    def __init__(self, dbname="details.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS INFO(Name text, City text, Locality text, Pincode integer, Modeofcontact text, MailID text, Phone_Number text, Requirements text, Board text, Standard integer, Medium text, Subjects text, Deal_Type text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, Name, City, Locality, Pincode, Modeofcontact, MailID, Phone_Number, Requirements, Board, Standard, Medium, Subjects, Deal_Type):
        stmt = "INSERT INTO INFO (Name, City, Locality, Pincode, Modeofcontact, MailID, Phone_Number, Requirements, Board, Standard, Medium, Subjects, Deal_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        args = ( Name, City, Locality, Pincode, Modeofcontact, MailID, Phone_Number, Requirements, Board, Standard, Medium, Subjects, Deal_Type)
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
