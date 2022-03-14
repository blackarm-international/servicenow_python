import requests, json
with open("config.json", "r") as config:
    credentials = json.load(config)
    user = credentials["USERNAME"]
    pwd = credentials["PASSWORD"]
    url = 'https://godaddydev.service-now.com/alm_hardware_list.do?sysparm_query=u_rack.nameSTARTSWITHp3sj01&sysparm_view='
    headers = {'Accept':'application/json'}
    response = requests.get(url, auth=(user, pwd), headers=headers)
    if response.status_code == 200:
      for hardware in response.json()["result"]:
        print(hardware)




