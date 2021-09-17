import requests, json, csv

def getCiData(sysparm_query, start, ci_sys_id_hardware_sysid):
    sysparm_field_list = ['fqdn','u_hardware.u_rack.name']
    sysparm_fields = '%2C'.join(sysparm_field_list)
    url = 'https://godaddy.service-now.com/api/now/table/cmdb_ci?sysparm_query=' + sysparm_query + '&sysparm_fields=' + sysparm_fields
    headers = {'Accept':'application/json'}
    response = requests.get(url, auth=(user, pwd), headers=headers)
    if response.status_code == 200:
        for ciData in response.json()["result"]:
            ci_sys_id_hardware_sysid[ciData['fqdn'].lower()] = ciData['u_hardware.u_rack.name']

ci_sys_id_hardware_sysid = {}
with open("config.json", "r") as config:
    credentials = json.load(config)
    user = credentials["USERNAME"]
    pwd = credentials["PASSWORD"]
    with open('data.csv', newline='') as csv_input:
        reader = csv.reader(csv_input, delimiter=';')
        test_data = list(reader)
        # print(test_data)
        sysparm_query = 'u_hardware.u_rack!=NULL^fqdnIN'
        start = True
        for datum in test_data:
            if start:
                sysparm_query += ',' + datum[0]
            else:
                sysparm_query += ',' + datum[0]
                start = False
            if len(sysparm_query) > 6000:
                getCiData(sysparm_query, start, ci_sys_id_hardware_sysid)
                sysparm_query = 'u_hardware.u_rack!=NULL^fqdnIN'
                start = True
        if sysparm_query != 'nameIN':
            getCiData(sysparm_query, start, ci_sys_id_hardware_sysid)
        # export to csv
        print('hostname, instantaneous, minimum, maximum, average, vms, rack')
        for thing in test_data:
            hostname = thing[0].lower()
            print(hostname + ', ', end='')
            print(thing[1] + ', ', end='')
            print(thing[2] + ', ', end='')
            print(thing[3] + ', ', end='')
            print(thing[4] + ', ', end='')
            print(thing[5] + ', ', end='')
            if hostname in ci_sys_id_hardware_sysid: 
                print(ci_sys_id_hardware_sysid[hostname])
            else:
                print('no rack')