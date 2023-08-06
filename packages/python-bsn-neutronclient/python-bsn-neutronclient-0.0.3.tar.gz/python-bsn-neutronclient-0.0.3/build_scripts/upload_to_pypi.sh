#!/bin/bash -eux

# RPM runs as root and doesn't like source files owned by a random UID
OUTER_UID=$(stat -c '%u' /python-bsn-neutronclient)
OUTER_GID=$(stat -c '%g' /python-bsn-neutronclient)
trap "chown -R $OUTER_UID:$OUTER_GID /python-bsn-neutronclient" EXIT
chown -R root:root /python-bsn-neutronclient

cd /python-bsn-neutronclient
git config --global user.name "Big Switch Networks"
git config --global user.email "support@bigswitch.com"

CURR_VERSION=$(awk '/^version/{print $3}' setup.cfg)

echo 'CURR_VERSION=' $CURR_VERSION
git tag -f -s $CURR_VERSION -m $CURR_VERSION -u "Big Switch Networks"

python setup.py sdist

# force success. but always check if pip install fails
twine upload dist/* -r pypi -s -i "Big Switch Networks" || true
# delay of 5 seconds
sleep 5
pip install --upgrade python-bsn-neutronclient==$CURR_VERSION
if [ "$?" -eq "0" ]
then
  echo "PYPI upload successful."
else
  echo "PYPI upload FAILED. Check the logs."
fi
# remove the package
pip uninstall -y python-bsn-neutronclient

# revert the permissions
chown -R $OUTER_UID:$OUTER_GID /python-bsn-neutronclient
