Kamailio
========

Kamailio Role for Kazoo Ansible

Requirements
------------

None

Role Variables
--------------

User Variables
- kazoo_kamailio_version - The Kazoo Kamailio version to install 
from the 2600hz repo. kazoo-ansible manages the version by default.

Dependencies
------------

None

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: kazoo-ansible.kamailio }

License
-------

MIT

