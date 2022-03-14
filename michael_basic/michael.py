import requests, json
query_start = "https://godaddy.service-now.com/api/now/table/"
with open("config.json", "r") as config:
  credentials = json.load(config)
  user = credentials["USERNAME"]
  pwd = credentials["PASSWORD"]
  # query alm_hardware
  table = "alm_hardware"
  sysparm_query = "u_rack.nameSTARTSWITHp3sj01^u_hardware_sku!=NULL"
  sysparm_field_list = ['u_rack','u_hardware_sku', 'u_rack.name','u_hardware_sku.u_sku_name']
  sysparm_fields = '%2C'.join(sysparm_field_list)
  # build a query without restricting fields
  url = query_start + table + '?sysparm_query=' + sysparm_query
  # build a query without restricting fields if they exist
  if len(sysparm_field_list) > 0:
    url = query_start + table + '?sysparm_query=' + sysparm_query + '&sysparm_fields=' + sysparm_fields
  headers = {'Accept':'application/json'}
  response = requests.get(url, auth=(user, pwd), headers=headers)
  if response.status_code == 200:
    sku_sys_id_count = {}
    for hardware in response.json()["result"]:
      print("=============================")
      print(json.dumps(hardware, indent=4))
      print(hardware["u_hardware_sku.u_sku_name"])
      print(hardware["u_rack.name"])