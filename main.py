import json
import urllib.parse

import psutil
import time
import signal
import sys
import requests


api_key = 'JBD4RVHICAUEHAZY'
datuak = []

def cpu_ram():
    # KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
 while True:
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))

    #Eskaera egin
    uria = "https://api.thingspeak.com/update.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': datuak[1],
              'field1': cpu,
              'field2': ram}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.post(uria, data=edukia_encoded,
                              headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("Datuak bidali:")
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

    # 15 segunduko etenaldia
    time.sleep(15)


# Gertaera kudeatu
def handler(sig_num, frame):
    kanala_hustu()
    print('\nSignal handler called with signal ' + str(sig_num))
    print('\nExiting gracefully')
    sys.exit(0)

# Press the green button in the gutter to run the script.

def kanala_hustu():
    #metodoa = 'DELETE'
    #uria = "https://api.thingspeak.com/channels/" + str(datuak[0]) + ".json"
    uria = "https://api.thingspeak.com/channels/" + str(datuak[0]) + "/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': 'AUVWRRWOG71KF40S'}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.delete(uria, data=edukia_encoded,
                                headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("Kanala hustu:")
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)





def kanala_sortu():
   # POST / channels.json HTTP / 2
   # Host: api.thingspeak.com
   # Content - Type: application / x - www - form - urlencoded
   # Content - Length: 42
   #
   # api_key = 3
   # BTKMKD1XNWSF4ZS & name = MyNewChannel

    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': 'AUVWRRWOG71KF40S',
              'name': 'proba1.0',
              'field1': "%CPU",
              'field2': "%RAM"}

    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print("Kanala sortu :")
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)
    # Kanalaren ID-a eta Write API key-a erantzuna JSON atera
    hiztegia = json.loads(edukia)
    kanala_id = hiztegia['id']
    write_api_key = hiztegia['api_keys'][0]['api_key']

    return kanala_id, write_api_key



if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to exit.')
    datuak = kanala_sortu()
    cpu_ram()





