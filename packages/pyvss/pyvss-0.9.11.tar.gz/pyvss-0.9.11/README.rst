Python client to the ITS Private Cloud API
==========================================

.. image:: https://gitlab-ee.eis.utoronto.ca/vss/py-vss/badges/master/build.svg
   :target: https://gitlab-ee.eis.utoronto.ca/vss/py-vss/commits/master

.. image:: https://gitlab-ee.eis.utoronto.ca/vss/py-vss/badges/master/coverage.svg
   :target: https://gitlab-ee.eis.utoronto.ca/vss/py-vss/commits/master

.. image:: https://img.shields.io/pypi/v/pyvss.svg
    :target: https://pypi.python.org/pypi/pyvss

.. image:: https://img.shields.io/pypi/pyversions/pyvss.svg
    :target: https://pypi.python.org/pypi/pyvss

.. image:: https://img.shields.io/docker/pulls/uofteis/pyvss.svg
    :target: https://hub.docker.com/r/uofteis/pyvss/
   
Inspired by `dop <https://github.com/ahmontero/dop>`_ 
and `dopy <https://github.com/Wiredcraft/dopy>`_

Features
========

Will support all methods listed in the official 
`API documentation <https://vss-wiki.eis.utoronto.ca/display/API>`_.

Installation
============

Installing the library is quite simple. Either clone the GitLab﻿
repository or download the source code or use pip to do everything for you:

Installation
------------

From PyPI:

.. code-block:: bash

   pip install pyvss

From source via HTTPS or SSH:

.. code-block:: bash

   git clone https://gitlab-ee.eis.utoronto.ca/vss/py-vss
   cd py-vss
   python setup.py install

.. note:: To be able to fetch from gitlab-ee.eis.utoronto.ca via SSH,
  first make sure to add your client account's SSH pub key in
  gitlab's "Settings > SSH Keys".


.. code-block:: bash

   git clone git@gitlab-ee.eis.utoronto.ca:vss/py-vss
   cd py-vss
   python setup.py install

macOS
~~~~~

XCode is required if you are planning to interact with VSKEY-STOR via
`WebdavClient <http://designerror.github.io/webdav-client-python/>`_.

.. code-block:: bash

   xcode-select --install
   curl https://bootstrap.pypa.io/ez_setup.py -o - | python
   python setup.py install --prefix=/opt/setuptools
   sudo easy_install pyvss
   sudo easy_install webdavclient


Linux
~~~~~

Additional libraries are required iif you are planning to interact with VSKEY-STOR via
`WebdavClient <http://designerror.github.io/webdav-client-python/>`_.

.. code-block:: bash

   sudo apt-get install libxml2-dev libxslt-dev python-dev
   sudo apt-get install libcurl4-openssl-dev python-pycurl
   sudo easy_install pyvss
   sudo easy_install webdavclient


Windows
~~~~~~~

Microsoft Visual Studio Express or Microsoft Visual C++ is required if you are planning
to interact with VSKEY-STOR via `WebdavClient <http://designerror.github.io/webdav-client-python/>`_.

.. code-block:: bash

   easy_install.exe pyvss
   easy_install.exe webdavclient


Upgrade
-------

.. code-block:: bash

   pip install --upgrade pyvss

   # or
   easy_install -U pyvss


Docker
======

.. image:: https://img.shields.io/docker/pulls/uofteis/pyvss.svg
    :target: https://hub.docker.com/r/uofteis/pyvss/

Docker image based on the official Python image on `Alpine Linux <https://hub.docker.com/_/alpine/>`_
and `PyVSS <https://pypi.python.org/pypi/pyvss>`_ in its latest version.

- Python 2.7 Alpine `uofteis/pyvss:py27 <https://hub.docker.com/r/uofteis/pyvss/>`_
- Python 3.5 Alpine `uofteis/pyvss:py35 <https://hub.docker.com/r/uofteis/pyvss/>`_
- Python 3.6 Alpine `uofteis/pyvss:py36 <https://hub.docker.com/r/uofteis/pyvss/>`_

.. code-block:: bash

    # with access token and python 3.5
    docker run -it -v `pwd`:/data -e VSS_API_TOKEN=token_here uofteis/pyvss:py35

    # user and pass and python 2.7
    docker run -it -v `pwd`:/data -e VSS_API_USER=user_here -e VSS_API_USER_PASS=user_pass_here uofteis/pyvss:py27

    # env file containing either VSS_API_USER and VSS_API_USER_PASS or VSS_API_TOKEN
    docker run -it -v `pwd`:/data --env-file vss.env uofteis/pyvss:py36


Use
===

Create an instance of ``VssManager`` passing your **ITS Private Cloud API access token**
and your are all set to start calling any of the self-descriptive methods included:

.. code-block:: py

    from pyvss.manager import VssManager
    vss = VssManager(tk='api_token')
    
    # list vms
    vms = vss.get_vms()
    
    # list folders
    folders = vss.get_folders()
    
    # networks
    networks = vss.get_networks()
    
    # domains
    domains = vss.get_domains()
    
    # power cycle vm
    vss.power_cycle_vm(uuid='<uuid>')
       
    # create vm
    req = vss.create_vm(os='ubuntu64Guest', built='os_install', 
                        description='Testing python wrapper', 
                        folder='group-v6736', bill_dept='EIS', disks=[100, 100])
    uuid = vss.wait_for_request(req['_links']['request'], 'vm_uuid', 'Processed')
    
    # creating multiple vms
    reqs = vss.create_vms(count=3, name='python', os='ubuntu64Guest', bill_dept='EIS', 
            description='Testing multiple deployment from python wrapper',
            folder='group-v6736', built='os_install')
    uuids = [vss.wait_for_request(r['_links']['request'], 'vm_uuid', 'Processed') for r in reqs]
    
    # power on recently created vms
    for uuid in uuids:
       vss.power_on_vm(uuid)
            
    # create snapshot
    req = vss.create_vm_snapshot(uuid='5012abcb-a9f3-e112-c1ea-de2fa9dab90a',
                                 desc='Snapshot description',
                                 date_time='2016-08-04 15:30',
                                 valid=1)
    snap_id = vss.wait_for_request(req['_links']['request'], 'snap_id', 'Processed')
    
    # revert to snapshot
    req = vss.revert_vm_snapshot(uuid, snap_id)


An alternative is to generate a token from within the ``VssManager`` class and this can be done
by setting the following environment variables

.. code-block:: bash

    export VSS_API_USER='username'
    export VSS_API_USER_PASS='username_password'


Then, from the ``VssManager`` call the ``get_token`` method as follows:

.. code-block:: py

    from pyvss.manager import VssManager
    vss = VssManager()
    vss.get_token()
    

It also supports command line execution by setting the ``VSS_API_TOKEN`` environment variable
with the **EIS Virtual Cloud REST API access token**

.. code-block:: bash
    
    python pyvss/manager.py get_vms 'summary=1&name=pm'
    [{u'_links': {u'self': u'https://vss-api.eis.utoronto.ca/v2/vm/<vm_uuid>'},
      u'cpuCount': 2,
      u'folder': {u'_links': {u'self': u'https://vss-api.eis.utoronto.ca/v2/folder/group-v519'},
                  u'moref': u'group-v519',
                  u'name': u'Public',
                  u'parent': u'API'},
      u'guestFullName': u'Ubuntu Linux (64-bit)',
      u'ipAddress': u'<ip_addr>',
      u'memoryMB': 4096,
      u'name': u'1502P-pm',
      u'overallStatus': u'green',
      u'powerState': u'poweredOn',
      u'storageB': 96637166467,
      u'uuid': u'<vm_uuid>'}]
      
    python pyvss/manager.py get_vm_console <vm_uuid>
    {u'value': u'https://vctr5-1.dcb.eis.utoronto.ca:7343/console/?vmId=vm-4766
    &vmName=1502P-pm&host=vctr5-1.dcb.eis.utoronto.ca:443&sessionTicket=<really-long-string>'}
      

Tests
=====

Required environment variables:

- ``VSS_API_TOKEN``: If set, will be used to execute tests.
- ``VSS_API_USER``: If ``VSS_API_TOKEN`` not set, test script will try to use this along with ``VSS_API_USER_PASS``.
- ``VSS_API_USER_PASS``: API user password. Used only when no ``VSS_API_TOKEN`` is set.
- ``VSS_API_TEST_FOLDER``: Target folder where VMs will be created during tests.

.. code-block:: bash

    pip install pep8 nose coverage pytz
    nosetests -v --with-coverage --cover-package=pyvss \
    --cover-branches --cover-erase --cover-html --cover-html-dir=cover

Questions
=========
Create an issue in the official repository `here <https://gitlab-ee.eis.utoronto.ca/vss/py-vss/issues>`_