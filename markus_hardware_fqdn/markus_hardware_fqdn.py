import requests, json
with open("config.json", "r") as config:
    credentials = json.load(config)
    user = credentials["USERNAME"]
    pwd = credentials["PASSWORD"]
    # alm_hardware query
    sysparm_field_list = ['ci.fqdn','ci.name','u_rack.name','u_rack.sys_id','location.name','sys_id']
    sysparm_fields = '%2C'.join(sysparm_field_list)
    sysparm_limit = '&sysparm_limit=100'
    sysparm_query = 'install_status!=7^model.u_device_category=6dc12117dbfd10541093f40c0c9619a9^ORmodel.u_device_category=69656ee9db6e4c9ce670d48a489619b0^location=8540336c37c8c78cce4fb15ec3990e1e^u_rackSTARTSWITHsxb1sa'
    url = 'https://godaddydev.service-now.com/api/now/table/alm_hardware?sysparm_query=' + sysparm_query + '&sysparm_fields=' + sysparm_fields
    #  + sysparm_limit
    headers = {'Accept':'application/json'}
    response = requests.get(url, auth=(user, pwd), headers=headers)
    if response.status_code == 200:
        output = {}
        rack_sys_id_unique = {}
        for hardware in response.json()["result"]:
            alm_hardware_sysid = ''
            ci_name = ''
            fqdn = ''
            location = ''
            rack = ''
            rack_sys_id = ''
            # alm_hardware_sysid
            if 'sys_id' in hardware:
                alm_hardware_sysid = hardware['sys_id']
            # ci_name
            if 'ci.name' in hardware:
                ci_name = hardware['ci.name']
            # fqdn
            if 'ci.fqdn' in hardware:
                if (hardware['ci.fqdn'] != ''):
                    fqdn = hardware['ci.fqdn']
            # location
            if 'location.name' in hardware:
                location = hardware['location.name']
            # rack name
            if 'u_rack.name' in hardware:
                rack = hardware['u_rack.name']
            # rack sysid
            if 'u_rack.sys_id' in hardware:
                rack_sys_id = hardware['u_rack.sys_id']
                rack_sys_id_unique[rack_sys_id] = True
            # store data
            output[alm_hardware_sysid] = {
                'ci_name': ci_name,
                'fqdn': fqdn,
                'location': location,
                'rack': rack,
                'rack_sys_id': rack_sys_id
            }
        # cmdb_ci query for parent rows
        sysparm_field_list = ['parent','child']
        sysparm_fields = '%2C'.join(sysparm_field_list)
        sysparm_query = 'child.sys_idIN' + ','.join(list(rack_sys_id_unique.keys()))
        url = 'https://godaddydev.service-now.com/api/now/table/cmdb_rel_ci?sysparm_query=' + sysparm_query + '&sysparm_fields=' + sysparm_fields
        headers = {'Accept':'application/json'}
        response = requests.get(url, auth=(user, pwd), headers=headers)
        if response.status_code == 200:
            rack_sys_id_row_sys_id = {}
            row_sys_id_list = []
            for rack_row_relation in response.json()["result"]:
                child_sys_id = ''
                parent_sys_id = ''
                if 'child' in rack_row_relation:
                    if (isinstance(rack_row_relation['child'], dict)):
                        child_sys_id = rack_row_relation['child']['value']
                if 'parent' in rack_row_relation:
                    if (isinstance(rack_row_relation['parent'], dict)):
                        parent_sys_id = rack_row_relation['parent']['value']
                if child_sys_id != '' and parent_sys_id != '':
                    rack_sys_id_row_sys_id[child_sys_id] = parent_sys_id
                    row_sys_id_list.append(parent_sys_id)
            # cmdb_ci query for parent rooms
            sysparm_field_list = ['parent','child']
            sysparm_fields = '%2C'.join(sysparm_field_list)
            sysparm_query = 'child.sys_idIN' + ','.join(row_sys_id_list)
            url = 'https://godaddydev.service-now.com/api/now/table/cmdb_rel_ci?sysparm_query=' + sysparm_query + '&sysparm_fields=' + sysparm_fields
            headers = {'Accept':'application/json'}
            response = requests.get(url, auth=(user, pwd), headers=headers)
            if response.status_code == 200:
                row_sys_id_room_sys_id = {}
                room_sys_id_list = []
                for row_room_relation in response.json()["result"]:
                    child_sys_id = ''
                    parent_sys_id = ''
                    if 'child' in row_room_relation:
                        if (isinstance(row_room_relation['child'], dict)):
                            child_sys_id = row_room_relation['child']['value']
                    if 'parent' in row_room_relation:
                        if (isinstance(row_room_relation['parent'], dict)):
                            parent_sys_id = row_room_relation['parent']['value']
                    if child_sys_id != '' and parent_sys_id != '':
                        row_sys_id_room_sys_id[child_sys_id] = parent_sys_id
                        room_sys_id_list.append(parent_sys_id)
                # cmdb_ci_computer room query for room names
                sysparm_field_list = ['sys_id','name']
                sysparm_fields = '%2C'.join(sysparm_field_list)
                sysparm_query = 'sys_idIN' + ','.join(room_sys_id_list)
                url = 'https://godaddydev.service-now.com/api/now/table/cmdb_ci_computer_room?sysparm_query=' + sysparm_query + '&sysparm_fields=' + sysparm_fields
                headers = {'Accept':'application/json'}
                response = requests.get(url, auth=(user, pwd), headers=headers)
                if response.status_code == 200:
                    room_sys_id_room_name = {}
                    room_sys_id_list = []
                    for room in response.json()["result"]:
                        room_sys_id = ''
                        room_name = ''
                        if 'sys_id' in room:
                            room_sys_id = room['sys_id']
                        if 'name' in room:
                            room_name = room['name']
                        if room_sys_id != '' and room_name != '':
                            room_sys_id_room_name[room_sys_id] = room_name
                    # output data
                    print('alm_hardware_sysid, rack, room, location, ci_name, fqdn')
                    for alm_hardware_sys_id in output:
                        print(alm_hardware_sys_id, end =",")
                        print(output[alm_hardware_sys_id]['rack'], end =",")
                        room_name = 'missing'
                        rack_sys_id = output[alm_hardware_sys_id]['rack_sys_id']
                        if rack_sys_id in rack_sys_id_row_sys_id:
                            row_sys_id = rack_sys_id_row_sys_id[rack_sys_id]
                            if row_sys_id in row_sys_id_room_sys_id:
                                room_sys_id = row_sys_id_room_sys_id[row_sys_id]
                                if room_sys_id in room_sys_id_room_name:
                                    room_name = room_sys_id_room_name[room_sys_id]
                        print(room_name, end =",")
                        print(output[alm_hardware_sys_id]['location'], end =",")
                        print(output[alm_hardware_sys_id]['ci_name'], end =",")
                        print(output[alm_hardware_sys_id]['fqdn'])






