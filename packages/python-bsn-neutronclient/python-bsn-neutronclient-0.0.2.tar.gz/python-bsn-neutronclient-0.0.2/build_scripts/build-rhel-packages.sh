#!/bin/bash -eux

cd /python-bsn-neutronclient
python setup.py bdist_rpm \
--release=1 \
--distribution-name=el7.centos \
--requires=python-neutronclient \
--build-requires=python-pbr 

# copy RPM and tar pkgs to hierarchical format in pkg directory
BUILD_OS=centos7-x86_64
CURR_VERSION=$(awk '/^version/{print $3}' setup.cfg)

# Copy built RPMs to pkg/
OUTDIR=$(readlink -m "pkg/$BUILD_OS/$GIT_BRANCH/$CURR_VERSION")
rm -rf "$OUTDIR" && mkdir -p "$OUTDIR"
cp dist/*.rpm "$OUTDIR"
cp dist/*.tar.gz "$OUTDIR"
git log > "$OUTDIR/gitlog.txt"
touch "$OUTDIR/build-$CURR_VERSION"
ln -snf $(basename $OUTDIR) $OUTDIR/../latest

rm -rf "$BUILDDIR"
