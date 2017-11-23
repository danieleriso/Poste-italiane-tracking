#!/usr/bin/python
import requests
import datetime

class PosteItaliane(object):
    trackingURL = "https://www.poste.it/online/dovequando/DQ-REST/ricercamultipla"
        
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Referer': 'https://www.poste.it/cerca/index.html',
        'Origin': 'https://www.poste.it'
        }

    payload = {
        'tipoRichiedente': 'WEB',
        'listaCodici': []
        }


    def __init__(self):
        self.shipments = []


    def __str__(self):     
        shipStr = ""

        for shipment in self.shipments:
            shipStr += "%s: %s\n" % (shipment["trackingNumber"], shipment["lastStatus"])
            for status in shipment["statusList"]:
                shipStr += "%s - %s (%s)\n" % (status["time"], status["statusDescription"], status["place"])
            shipStr += "\n"
        
        return shipStr.encode("utf-8")


    def track (self, trackingNumbers):
        self.payload["listaCodici"] = trackingNumbers

        r = requests.post(self.trackingURL, json=self.payload, headers=self.headers)
        response = r.json()
        
        for shipment in response:
            statusList = []
            
            if "descrizioneErrore" not in shipment:
                error = False

                if "listaMovimenti" in shipment:
                    lastStatus = shipment["sintesiStato"]

                    for status in shipment["listaMovimenti"]:
                        time = datetime.datetime.fromtimestamp(int(status["dataOra"])/1000).strftime('%d-%m-%Y %H:%M:%S')
                        statusList.append({"time": time, "statusDescription": status["statoLavorazione"], "place": status["luogo"]})
                else:
                    lastStatus = "Nessuna informazione di spedizione"
            else:
                lastStatus = "Errore"
                error = True
                        
            self.shipments.append({"trackingNumber": shipment["idTracciatura"], "lastStatus": lastStatus, "statusList": statusList, "error": error})    
        
        return self.shipments


if __name__ == "__main__":
    trackingNumbers = ["AB01234CD", "EF56789GH"]
    poste = PosteItaliane()
    shipments = poste.track(trackingNumbers)

    print poste