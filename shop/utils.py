import requests
import json


euro_req = requests.get('https://www.nbrb.by/api/exrates/rates/451')
euro = json.loads(euro_req.text)['Cur_OfficialRate']
# print(euro)

usd_req = requests.get('https://www.nbrb.by/api/exrates/rates/431')
usd = json.loads(usd_req.text)['Cur_OfficialRate']
# print(usd)

currency = {'euro_ex_rate': euro, 'usd_ex_rate': usd}

# def currency(request):
#     return {'euro': euro, 'usd': usd}
#
# print(currency())