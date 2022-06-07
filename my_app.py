import json
import requests

#
Url = "http://127.0.0.1:8000/list/"
# data = {
#     'name': 'sajil',
#     'email': 'sajo@gmail.com',
#     'age': 4
# }
# json_data = json.dumps(data)
# r = requests.post(url=Url,data=json_data)
# data = r.json()


def studentdata(id=None):
    if id is not None:
        data = {'id': id}
    json_data = json.dumps(data)
    r = requests.get(url=Url, data=json_data)
    data = r.json()
    print(data)


studentdata(1)
