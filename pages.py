from flask import render_template, request, redirect
import settings

def index():
    if "rec" in request.form:
        rec = request.form.get('rec')
        print(rec)
        if int(rec) == 1:
            settings.plc.recording(True)
        elif int(rec) == 0:
            settings.plc.recording(False)

    srec = request.args.get('startid')
    try:
        rec = int(srec)
    except:
        rec = -1 
    res = settings.cont.forIndex(rec)
    return render_template('index.html', rows=res, record=settings.plc.getRecording())

def showpkt():
    if "id" in request.form:
        id = request.form.get('id')
    else:
        id = request.args.get('id')

    # packet action
    if "action" in request.form:
        action = request.form.get('action')
    else:
        action = None

    try:
        newnote  = request.form.get('note')
    except:
        newnote = ' '

    if(action=='tx'):
        settings.plc.txbyId(id)
    elif(action=="store"):
        settings.cont.storePkt(id,newnote)
    elif(action=="update"):
        settings.cont.updatePkt(id,newnote)
    elif(action=="delete"):
        settings.cont.deletePkt(id)
        return redirect("/", code=302)
    elif(action=="back"):
        return redirect("/", code=302)
    packet = settings.cont.getNote(id)
    return render_template('pkt.html', id=id,
        packet=packet)

def stored():
    print(request.form)
    print(request.args)
    if "action" in request.form:
        action = request.form.get('action')
    elif "action" in request.args:
        action = request.args.get('action')
    else:
        action = None

    if(action and action[:4]=='add_'):
        print("add")
        for chkid in request.form.keys():
            if chkid[:4] == 'chk_':
                settings.cont.addToSeq(int(action[4:]),int(chkid[4:]))
            print(chkid)
    elif(action=="tx1"):
        print("tx1")
        for seqid in request.form.keys():
            print(seqid)
    elif(action=="loop"):
        print("loop")
    elif(action=="seqdel"):
        try:
            pktid = request.args.get('id')
            seqnum = request.args.get('seq')
            settings.cont.delFromSeq(seqnum, pktid)
        except:
            print(request.args)
            print("no id to del")

    res = settings.cont.getStored()
    seqs = settings.cont.getSeqs()
    print(seqs)
    return render_template('stored.html', rows=res, seqs=seqs)