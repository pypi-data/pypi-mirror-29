import urllib
import urllib2
import json
import sys


class pyaweminapi:

    __url = ''

    def __init__(self, url):
        self.__url = url

    def getminers(self):
        endpoint = self.__url + '/webapi/miners?system_id=1'
        headers = {
            'User-agent': 'Mozilla/4.0 (compatible; pyaweminerapi; ' +
                          str(sys.platform) + '; ' + str(sys.version).replace('\n', '') + ')'
        }
        req = urllib2.Request(endpoint, None, headers)
        page = urllib2.urlopen(req).read()
        return json.loads(page)["groupList"][0]["minerList"]

    def getGpusTemp(self):
        temps = {}
        _temps = []
        data = self.getminers()
        for miner in data:
            if miner["statusInfo"]["statusDisplay"]!="Disabled":
                for gpu in miner["gpuList"]:
                    _temps.append(gpu["deviceInfo"]["temperature"])
                temps[miner["name"]]=_temps
                _temps = []
        return temps

    def getMinersBriefing(self):
        hr = {}
        _hr = []
        _temps = []
        _review = []
        _fans = []
        data = self.getminers()
        for miner in data:
            if miner["statusInfo"]["statusDisplay"] != "Disabled":
                for gpu in miner["gpuList"]:
                    _hr.append(gpu["speedInfo"]["hashrate"])
                    _temps.append(gpu["deviceInfo"]["temperature"])
                    _fans.append(gpu["deviceInfo"]["fanPercent"])
                hr["name"]=miner["name"]
                hr["gpuhashrates"]=_hr
                hr["totalhashrate"]=miner["speedInfo"]["hashrate"]
                hr["totalhashratesecondary"]=miner["speedInfo"]["line2"]
                hr["mainpool"]=miner["poolList"][0]["additionalInfo"]["displayUrl"]
                hr["dualpool"]=miner["poolList"][1]["additionalInfo"]["displayUrl"]
                hr["timerunning"]=miner["statusInfo"]["statusLine3"]
                hr["temps"]=_temps
                hr["fans"]=_fans
                _review.append(hr)
                _hr = []
                _fans = []
                _temps = []
                hr = {}
        return _review