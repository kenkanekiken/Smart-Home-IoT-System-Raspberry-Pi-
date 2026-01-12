from mfrc522 import SimpleMFRC522
import threading
import time

#CARD ID: 283513489777
#CARD ID: 495169682925
reader = None
latest_id = None
latest_text = None

_last_trigger_id = None
_last_trigger_time = 0

def _worker():
    global latest_id, latest_text, _last_trigger_id, _last_trigger_time
    while True:
        now = time.time()
        cid, text = reader.read()      
        if cid == _last_trigger_id and (now - _last_trigger_time) < 2.0:
            continue
        _last_trigger_id = cid
        _last_trigger_time = now
        
        latest_id = cid              
        latest_text = text

def start():
    global reader
    if reader is None:
        reader = SimpleMFRC522()
    threading.Thread(target=_worker, daemon=True).start()
