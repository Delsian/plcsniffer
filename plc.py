import pyplc
from database import Database

class Plc(object):
    __pl = None

    def __init__(self):
        self.record = False
        self.db = Database()
        self.cur = self.db.getCursor()
        print("Init PLC")
        self.__pl = pyplc.PyPlc()
        self.__pl.setrxcb(self.rx_callback)
        self.__pl.speed=2000000
        self.__pl.open(0,0,8,20,1,22)

    def rx_callback(self, pkt):
        print(pkt.hex())
        if(self.record):
            add_p = "INSERT INTO packets (packet) VALUES ('{}')".format(pkt.hex())
            self.cur.execute(add_p)
            self.db.commit()

    def tx(self, pkt):
        print("tx ", pkt)
        #self.__pl.tx(pkt)

    def txbyId(self, id):
        q="SELECT packet FROM packets WHERE id={};".format(id)
        self.cur.execute(q)
        p= self.cur.fetchall()
        if len(p):
            pkt=p[0]['packet'].rstrip('\x00')
            print("Packet ",pkt)
            self.__pl.tx(bytearray.fromhex(pkt))

    def recording(self, state):
        print("Set recording ", state)
        self.record = state
    def getRecording(self):
        return self.record

    def close(self):
        print("Release PLC")
        self.__pl.close()