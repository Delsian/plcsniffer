import pyplc
import threading, time

class Plc(object):
    __pl = None

    def __init__(self, db):
        self.record = False
        self.db = db
        self.cur = self.db.getCursor()
        print("Init PLC")
        self.__pl = pyplc.PyPlc()
        self.__pl.setrxcb(self.rx_callback)
        self.__pl.speed=2000000
        self.__pl.open(0,0,8,20,1,22)
        self.__seqid = None
        self.__threadrun = False
        self.__threadloop = False
        self.__txarray = []
        self.__delay = 10

    def rx_callback(self, pkt):
        print(pkt.hex())
        if(self.record):
            add_p = "INSERT INTO packets (packet) VALUES ('{}')".format(pkt.hex())
            self.cur.execute(add_p)
            self.db.commit()

    def getPkt(self, id):
        q="SELECT packet FROM packets WHERE id={};".format(id)
        self.cur.execute(q)
        p= self.cur.fetchall()
        if len(p):
            pkt=bytearray.fromhex(p[0]['packet'].rstrip('\x00'))
            return pkt
        return []

    def txbyId(self, id):
        self.__pl.tx(self.getPkt(pkt))

    def recording(self, state):
        print("Set recording ", state)
        self.record = state
    def getRecording(self):
        return self.record

    def txthread(self):
        while(self.__threadrun):
            for pkt in self.__txarray:
                time.sleep(self.__delay/1000)
                self.__pl.tx(pkt)
                if not self.__threadrun:
                    break
            if not self.__threadloop:
                self.__threadrun = False
        print("Thread done")


    def txSeqence(self, seqid, loop=False):
        self.__threadloop = loop
        self.__threadrun = True
        self.__seqid = seqid
        q="SELECT pktid FROM seqpkt WHERE seq={} ORDER BY pktnum ASC;".format(self.__seqid)
        self.cur.execute(q)
        p= self.cur.fetchall()
        print(p)
        q="SELECT * FROM sequences WHERE seqid={};".format(self.__seqid)
        self.cur.execute(q)
        d= self.cur.fetchall()[0]
        self.__delay = int(d['delay'])
        print(self.__delay)
        self.__txarray = []
        for pk in p:
            print(pk)
            pktbytes = self.getPkt(pk["pktid"])
            self.__txarray.append(pktbytes)
        threading.Thread(target=self.txthread).start()

    def txStop(self):
        self.__threadrun = False
        print("Tx stop")

    def close(self):
        print("Release PLC")
        self.__pl.close()