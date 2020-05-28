from flask import Flask, render_template, request, redirect, url_for
import atexit
import threading
import pages
import settings

def close_running_threads():
    settings.db.commit()
    print ("Threads complete, ready to finish")
    settings.plc.close()

app = Flask(__name__)
app.add_url_rule('/pkt', view_func=pages.showpkt, methods=['POST', 'GET'])
app.add_url_rule('/', view_func=pages.index, methods=['POST', 'GET'])
app.add_url_rule('/stored', view_func=pages.stored, methods=['POST', 'GET'])

def flaskThread():
    app.run(debug=False, use_reloader=False, port=80, host='0.0.0.0')


if __name__ == '__main__':
    settings.init()

    atexit.register(close_running_threads)

    threading.Thread(target=flaskThread).start()