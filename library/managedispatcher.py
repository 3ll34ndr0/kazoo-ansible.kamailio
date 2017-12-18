from ansible.module_utils.basic import *
import sqlite3

def main():
    module = AnsibleModule(
        argument_spec=dict(
            freeswitch_hosts=dict(required=True, type='list'),
        ),
        supports_check_mode=True
    )
    
    freeswitch_hosts = module.params['freeswitch_hosts']
    
    with sqlite3.connect('/etc/kazoo/kamailio/db/kazoo.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT destination FROM dispatcher')
        existing_hosts = cursor.fetchall()
        existing_hosts = [get_hostname(destination[0]) \
            for destination in existing_hosts]

        new_hosts = [host for host in freeswitch_hosts \
            if host not in existing_hosts]

        extra_hosts = [ip for ip in existing_hosts \
            if host not in freeswitch_hosts]

        changed = len(new_hosts) + len(extra_hosts) != 0

        if module.check_mode:
            module.exit_json(changed=changed)

        for host in new_hosts:
            cursor.execute('INSERT INTO dispatcher (setid, destination) VALUES (?, ?)', \
                (1, 'sip:{}:11000'.format(host)))
        
        for host in extra_hosts:
            cursor.execute('DELETE FROM dispatcher WHERE destination LIKE ?', \
                ('%{}%'.format(host),))
        
        cursor.execute('DELETE FROM dispatcher WHERE destination LIKE \'%::%\'')
        
        conn.commit()

    module.exit_json(changed=changed)

def get_hostname(url):
    # Turns sip:192.168.1.1:11000 to 192.168.1.1
    pieces = url.split(':')
   
    if len(pieces) != 3:
        module.fail_json('{} is not a valid URL (Hint: sip:IP:PORT)'\
            .format(url))
   
    return pieces[1]

if __name__ == '__main__':
    main()

