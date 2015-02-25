==============================================
AWS Cloudformation Stack Updater - Python Boto
==============================================

This script allows updating AWS Cloudformation stack by specifiing region, stack name, template body and template parameters.

AWS Cloudformation Stack updater requires Python 2.7+ and was only tested on Ubuntu 14.04 and Mac OS X.

Prerequisites
=============

Install boto: 

.. code-block:: bash

    $ sudo pip install boto

Configure:

.. URL: http://boto.readthedocs.org/en/latest/boto_config_tut.html

Running
=======

.. code-block:: bash

     $ python cf_stack_updater.py --region ap-southeast-2 --stack_name TESTv01 --template_body template.json --template_params parameters.json

