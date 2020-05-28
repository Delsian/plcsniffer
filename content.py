from database import Database

class Content(object):
    def __init__(self, plc):
        self.db = Database()
        self.cur = self.db.getCursor()
        self.plc = plc

    def forIndex(self, pos):
        if(pos>0):
            adp = "WHERE packets.id>{} AND packets.id<={}".format(pos-15,pos)
        else:
            adp = " "
        q=("SELECT packets.id, packets.packet, packets.time, storedpkt.note "
            "FROM packets left join storedpkt on packets.id=storedpkt.id "
            "{} ORDER BY packets.id DESC LIMIT 16".format(adp))
        self.cur.execute(q)
        result = self.cur.fetchall()
        for row in result:
            row['len'] = int(len(row['packet'].rstrip('\x00'))/2)
        return result

    def getStored(self):
        q="SELECT storedpkt.id, storedpkt.note, packets.packet FROM packets INNER JOIN storedpkt ON packets.id = storedpkt.id;"
        self.cur.execute(q)
        result = self.cur.fetchall()
        for row in result:
            row['len'] = int(len(row['packet'].rstrip('\x00'))/2)
        return result

    def getPacket(self, id):
        q="SELECT id, packet FROM packets WHERE id={};".format(id)
        self.cur.execute(q)
        p= self.cur.fetchall()
        if len(p):
            return p[0]
        return None

    def storePkt(self, id, note):
        q="INSERT INTO storedpkt (id,note) VALUES ({},'{}');".format(id,note)
        self.cur.execute(q)
        self.db.commit()

    def updatePkt(self, id, note):
        q="UPDATE storedpkt SET note = '{}' WHERE id = {};".format(note,id)
        self.cur.execute(q)
        self.db.commit()

    def getNote(self, id):
        p1 = self.getPacket(id)
        q="SELECT note, id FROM storedpkt WHERE id={};".format(id)
        self.cur.execute(q)
        p2 = self.cur.fetchall()
        if len(p2):
            p1['note'] = p2[0]['note']
            p1['stored'] = True
        else:
            p1['stored'] = False
        return p1

    def deletePkt(self, id):
        q="DELETE FROM packets WHERE id={};".format(id)
        self.cur.execute(q)
        q="DELETE FROM storedpkt WHERE id={};".format(id)
        self.cur.execute(q)
        self.db.commit()

    def getSeqs(self):
        q="SELECT * FROM sequences;"
        self.cur.execute(q)
        p= self.cur.fetchall()
        for s in p:
            q="SELECT seqord, pktid FROM seqpkt WHERE seqid={};".format(s['seqid'])
            self.cur.execute(q)
            p1= self.cur.fetchall()
            s['pkts']=p1
        return p

    def addToSeq(self,seq,id):
        q="INSERT INTO seqpkt (seqid,seqord,pktid) VALUES ({},{},{});".format(seq,10,id)
        self.cur.execute(q)
        self.db.commit()

    def delFromSeq(self,seq,id):
        q="DELETE FROM seqpkt WHERE seqid={} AND pktid={};".format(seq,id)
        self.cur.execute(q)
        self.db.commit()
