#!/bin/bash

baddeps=""
# check deps
rpm -qi python2-setuptools > /dev/null 2>&1 || baddeps="python2-setuptools"
rpm -qi python2-setuptools_git > /dev/null 2>&1 || baddeps="${baddeps} python2-setuptools_git"
rpm -qi python2-pypandoc > /dev/null 2>&1 || baddeps="${baddeps} python2-pypandoc"
rpm -qi python2-twine > /dev/null 2>&1 || rpm -qi twine > /dev/null 2>&1 || baddeps="${baddeps} python2-twine (F27 and earlier) or twine (F28 and later)"
if [ -n "${baddeps}" ]; then
    echo "${baddeps} must be installed!"
    exit 1
fi

if [ "$#" != "1" ]; then
    echo "Must pass release version!"
    exit 1
fi

version=$1
name=fedfind
sed -i -e "s,version=\".*\",version=\"${version}\", g" setup.py
sed -i -e "s,__version__ = \".*\",__version__ = \"${version}\", g" ${name}/__init__.py
git add setup.py ${name}/__init__.py
git commit -s -m "Release ${version}"
git push
git tag -a -m "Release ${version}" ${version}
git push origin ${version}
python ./setup.py sdist --formats=tar
gzip dist/${name}-${version}.tar
twine upload dist/${name}-${version}.tar.gz
