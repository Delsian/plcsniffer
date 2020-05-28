from flask import render_template, request, redirect
import settings

def index():
    print(request.form)
    action = None
    for key in request.form.keys():
        if(key[:4]=='del_'):
            id = int(key[4:])
            settings.cont.deletePkt(id)
        elif (key=='action'):
            action = request.form.get('action')

    if (action=="stored"):
        return redirect("/stored", code=302)
    elif (action=="rec"):
        settings.plc.recording(True)
        settings.refresh = True
    elif (action=="stop"):
        settings.plc.recording(False)
        settings.refresh = False
    elif (action=="pgdn"):
        print("ToDo")

    rec = -1 
    res = settings.cont.forIndex(rec)
    return render_template('index.html', rows=res, 
        record=settings.plc.getRecording(), refresh=settings.refresh)

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
        settings.cont.updatePkt(id,newnote.lstrip(' ').rstrip(' '))
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
    for key in request.form.keys():
        if(key[:6]=='delay_'):
            delay = request.form.get(key)
            seq = int(key[6:])
            settings.cont.updateSeq(seq,'delay',delay)
        elif(key[:8]=='seqname_'):
            name = request.form.get(key).lstrip(' ').rstrip(' ')
            seq = int(key[8:])
            settings.cont.updateSeq(seq,'seqname',name)

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
    elif(action=="tx1"):
        for seqid in request.form.keys():
            if(seqid[:3]=='tx_'):
                settings.plc.txSeqence(int(seqid[3:]))
                break
    elif(action=="loop"):
        for seqid in request.form.keys():
            if(seqid[:3]=='tx_'):
                settings.plc.txSeqence(int(seqid[3:]), True)
                break
    elif(action=="txstop"):
        settings.plc.txStop()
    elif(action=="seqdel"):
        try:
            pktnum = request.args.get('pos')
            seqnum = request.args.get('seq')
            settings.cont.delFromSeq(seqnum, pktnum)
        except:
            print(request.args)
            print("no id to del")
    elif(action=="newseq"):
        settings.cont.addSeqs()

    res = settings.cont.getStored()
    seqs = settings.cont.getSeqs()
    print(seqs)
    return render_template('stored.html', rows=res, seqs=seqs)