from database import Database

class Content(object):
    def __init__(self, plc):
        self.db = Database()
        self.cur = self.db.getCursor()
        self.plc = plc

    def forIndex(self, pos):
        if(pos>0):
            adp = "WHERE packets.id<={}".format(pos)
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
        q=("SELECT storedpkt.id, storedpkt.note, packets.packet FROM packets "
            "INNER JOIN storedpkt ON packets.id = storedpkt.id ORDER BY storedpkt.id DESC;")
        self.cur.execute(q)
        result = self.cur.fetchall()
        for row in result:
            row['len'] = int(len(row['packet'].rstrip('\x00'))/2)
        return result

    def getPacket(self, id):
        q="SELECT id, packet FROM packets WHERE id={};".format(id)
        self.cur.execute(q)
        p= self.cur.fetchone()
        return p

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
        p2 = self.cur.fetchone()
        if p2:
            p1['note'] = p2['note']
            p1['stored'] = True
        else:
            p1['stored'] = False
        return p1

    def deletePkt(self, id):
        q="DELETE FROM packets WHERE id={};".format(id)
        self.cur.execute(q)
        q="DELETE FROM storedpkt WHERE id={};".format(id)
        self.cur.execute(q)
        q="SET SQL_SAFE_UPDATES=0;DELETE FROM seqpkt WHERE pktid={};".format(id)
        print (q)
        self.cur.execute(q,multi=True)
        self.db.commit()

    def getSeqs(self):
        q="SELECT * FROM sequences;"
        self.cur.execute(q)
        p= self.cur.fetchall()
        for s in p:
            q="SELECT pktnum, pktid FROM seqpkt WHERE seq={} ORDER BY pktnum ASC;".format(s['seqid'])
            self.cur.execute(q)
            p1= self.cur.fetchall()
            s['pkts']=p1
        return p

    def addSeqs(self):
        q="INSERT INTO sequences (delay) VALUES (10);"
        self.cur.execute(q)
        self.db.commit()

    def updateSeq(self,seq,field,val):
        q="UPDATE sequences SET {} = '{}' WHERE seqid = {};".format(field,val,seq)
        self.cur.execute(q)

    def addToSeq(self,seq,id):
        q=("INSERT INTO seqpkt (pktnum,seq,pktid) SELECT "
            "IFNULL(MAX(pktnum),0)+1, {}, {} FROM seqpkt WHERE seq={};".format(seq,id, seq))
        self.cur.execute(q)
        self.db.commit()

    def delFromSeq(self,seq,num):
        q="DELETE FROM seqpkt WHERE seq={} AND pktnum={};".format(seq,num)
        self.cur.execute(q)
        self.db.commit()

    def getTop(self):
        q = "SELECT MAX(id) FROM packets;"
        self.cur.execute(q)
        r = self.cur.fetchone()
        return r["MAX(id)"]