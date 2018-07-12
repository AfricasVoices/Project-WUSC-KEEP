#!/usr/bin/env bash

set -e

echo "Uploading to interface..."
scp -i ~/.ssh/Alexander.pem ../../data/interface_export/inbox interface.africasvoices.org:/www/unicef_somalia/data
scp -i ~/.ssh/Alexander.pem ../../data/interface_export/demo interface.africasvoices.org:/www/unicef_somalia/data

echo "Restarting server..."
ssh -t ubuntu@interface.africasvoices.org "sudo service uwsgi restart unicef"

echo "Done"
