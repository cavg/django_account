# Uninstall older versions
# TODO: check if djang-accounts is alread installed
# pip3 uninstall -y django-accounts &&

# Packing new version
cd package/django-accounts/ &&
python3 setup.py sdist &&

#Install new version
pip3 install --user dist/django-accounts-0.3.2.tar.gz &&
cd ../../
