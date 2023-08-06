****************
xldeploy-py
****************
Python SDK for XL-Deploy_.

.. _XL-Deploy: https://xebialabs.com/products/xl-deploy


Usage
=======

.. code:: python

    import xldeploy

    config = xldeploy.Config(protocol="http", host="localhost", port="4516", context_path="deployit", username="admin", password="admin")

    # If you are using url
    config = xldeploy.Config.initialize(url="http://localhost:4516/deployit", username="admin", password="admin")

    # If you are using proxies
    config = xldeploy.Config(protocol="http", host="localhost", port="4516", context_path="deployit", username="admin", password="admin",  proxy_host="localhost", proxy_port=8080, proxy_username="proxyUsername", proxy_password="proxyPassword")

    # or
    config = xldeploy.Config()
    client = xldeploy.Client(config)

    # repository
    repository = client.repository
    print(repository.exists("Applications/EC2/1.0/ec2"))
    print(repository.exists("Applications/EC2/1.0/wrong"))
    ci = repository.read("Applications/EC2/1.0/ec2")
    print(ci.amiId)

    # deployment
    deployment = client.deployment
    deploymentRef = deployment.prepare_initial("Applications/NIApp/1.0", "Environments/awsEnv")
    depl = deployment.prepare_auto_deployeds(deploymentRef)
    task = deployment.create_task(depl)
    task.start()
    print(task.task_id)

    # Deployfile

    ## Apply Deployfile script.

    import re
    from os import path

    deployfile = client.deployfile
    deploy_file = open('deploy_file_path', 'rb').read()
    file_names = re.findall('upload\([\'|"](.*)[\'|"]\)', deploy_file.decode("utf-8"))
    files_to_upload = [path.abspath(path.join(path.abspath(path.join(file_path, "..")), name)) for name in file_names]

    deployfile.apply('deploy_file_path',files_to_upload)

    ## POST of multiple multipart-encoded binary files  

    Based on Python [requests](https://pypi.python.org/pypi/requests) module, see [docs](http://docs.python-requests.org/en/master/user/advanced/#advanced) 

    ## Generate Deployfile script.

    deployfile = client.deployfile
    deployfile.generate([Environments/directory1,Environments/directory1])

Installing from the PyPi repository
===================================
::

    $ pip install xldeploy-py

Installing package directly from source
=======================================
::

    $ cd xldeploy-py
    $ pip install --editable .
