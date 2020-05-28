from plc import Plc
from content import Content
from database import Database

def init():
    global plc, cont, db
    db = Database()
    plc = Plc()
    cont = Content(plc)