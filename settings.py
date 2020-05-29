from plc import Plc
from content import Content
from database import Database

def init():
    global plc, cont, db, refresh, maxpos, showpos
    db = Database()
    plc = Plc(db)
    cont = Content(plc)
    refresh = False
    maxpos = 999999
    showpos = maxpos
    