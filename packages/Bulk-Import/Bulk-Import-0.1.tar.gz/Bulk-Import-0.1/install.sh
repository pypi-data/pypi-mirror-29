#!/bin/bash

if [[ $(id -u) -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

yum install -y libxslt python-pip
pip install --upgrade pip
pip install virtualenv wheel
virtualenv -p python /opt/bulk-import
source /opt/bulk-import/bin/activate
cp Bulk-Import.py /opt/bulk-import/bin/