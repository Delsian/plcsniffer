from plc import Plc
from content import Content
from database import Database

def init():
    global plc, cont, db, refresh
    db = Database()
    plc = Plc(db)
    cont = Content(plc)
    refresh = False