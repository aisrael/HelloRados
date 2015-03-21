#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2015, Alistair Israel <aisrael@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: ceph_osd_pool
short_description: Ceph OSD pools module for Ansible.
description:
 - Use this module to manage Ceph OSD pools
version_added: "1.8"
options:
  command:
    description:
     - A ceph command to be executed.
    required: true
requirements:
 - ceph
author: Alistair Israel
'''

EXAMPLES = '''
# Create an OSD pool
- ceph_osd_pool: state=present name=data pgnum=128 pgpnum=128
'''

import datetime
import json

import rados

def main():
    module = AnsibleModule(
        argument_spec = dict(
            state = dict(choices=['present','absent'], default='present'),
            name = dict(required=True),
            pgnum = dict(type='int'),
            pgpnum = dict(type='int')
        ),
        supports_check_mode = False
    )

    name = module.params['name']

    result = {}
    result['name'] = name

    changed = False

    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    cluster.connect()
    pools = cluster.list_pools()

    state = module.params['state']
    if state == 'present':
        if not name in pools:
            pgnum = module.params['pgnum']
            pgpnum = module.params['pgpnum']

            startd = datetime.datetime.now()
            cmd = 'ceph osd pool create {0} {1} {2}'.format(name, pgnum, pgpnum)
            rc, out, err = module.run_command(cmd)
            endd = datetime.datetime.now()
            delta = endd - startd

            result['cmd'] = cmd
            result['stdout'] = out.rstrip("\r\n")
            result['stderr'] = err.rstrip("\r\n")
            result['start'] = str(startd)
            result['end'] = str(endd)
            result['delta'] = str(delta)

            expected_stderr = "pool '{0}' created".format(name)
            changed = expected_stderr == result['stderr']
    else:
        if name in pools:
            startd = datetime.datetime.now()
            cmd = 'ceph osd pool delete {0} {0} --yes-i-really-really-mean-it'.format(name)
            rc, out, err = module.run_command(cmd)
            endd = datetime.datetime.now()
            delta = endd - startd

            result['cmd'] = cmd
            result['stdout'] = out.rstrip("\r\n")
            result['stderr'] = err.rstrip("\r\n")
            result['start'] = str(startd)
            result['end'] = str(endd)
            result['delta'] = str(delta)

            expected_stderr = "pool '{0}' removed".format(name)
            changed = expected_stderr == result['stderr']

    result['changed'] = changed
    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
