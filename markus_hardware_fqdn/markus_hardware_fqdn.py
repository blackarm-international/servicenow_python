import requests, json
with open("config.json", "r") as config:
    credentials = json.load(config)
    user = credentials["USERNAME"]
    pwd = credentials["PASSWORD"]
    # query parameters
    sysparm_field_list = ['sys_id','ci','ci.fqdn']
    sysparm_fields = '%2C'.join(sysparm_field_list)
    sysparm_limit = '100'
    sysparm_query = 'install_status!=7^model.u_device_category=6dc12117dbfd10541093f40c0c9619a9^ORmodel.u_device_category=69656ee9db6e4c9ce670d48a489619b0^location=8540336c37c8c78cce4fb15ec3990e1e^u_rackSTARTSWITHsxb1sa'
    url = 'https://godaddydev.service-now.com/api/now/table/alm_hardware?sysparm_query=' + sysparm_query + '&sysparm_limit=' + sysparm_limit + '&sysparm_fields=' + sysparm_fields
    headers = {'Accept':'application/json'}
    response = requests.get(url, auth=(user, pwd), headers=headers)
    if response.status_code == 200:
        output = {}
        for hardware in response.json()["result"]:
            alm_hardware_sysid = ''
            ci_sys_id = ''
            fqdn = ''
            # hardware sys_id
            if (hardware['sys_id'] != ''):
                alm_hardware_sysid = hardware['sys_id']
            # ci sys_id
            if (isinstance(hardware['ci'], dict)):
                ci_sys_id = hardware['ci']['value']
            # fqdn
            if (hardware['ci.fqdn'] != ''):
                fqdn = hardware['ci.fqdn']
            output[alm_hardware_sysid] = {
                'ci_sys_id': ci_sys_id,
                'fqdn': fqdn
            }
        print(json.dumps(output, indent=4))
