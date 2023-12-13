#!/usr/bin/env bash
set -e
CPUC=$(getconf _NPROCESSORS_ONLN)

mkdir -p /home/firebird
cd /home/firebird
curl -L -o firebird-source.tar.bz2 -L "${FBURL}"
tar --strip=1 -xf firebird-source.tar.bz2
./configure \
    --prefix="${PREFIX}"/ --with-fbbin="${PREFIX}"/bin/ --with-fbsbin="${PREFIX}"/bin/ --with-fblib="${PREFIX}"/lib/ \
    --with-fbinclude="${PREFIX}"/include/ --with-fbdoc="${PREFIX}"/doc/ --with-fbudf="${PREFIX}"/UDF/ \
    --with-fbsample="${PREFIX}"/examples/ --with-fbsample-db="${PREFIX}"/examples/empbuild/ --with-fbhelp="${PREFIX}"/help/ \
    --with-fbintl="${PREFIX}"/intl/ --with-fbmisc="${PREFIX}"/misc/ --with-fbplugins="${PREFIX}"/ \
    --with-fbconf="${VOLUME}/etc/" --with-fbmsg="${PREFIX}"/ \
    --with-fblog="${VOLUME}/log/" --with-fbglock=/var/firebird/run/ \
    --with-fbsecure-db="${VOLUME}/system"
make -j"${CPUC}"
make silent_install
cd /
rm -rf /home/firebird

find "${PREFIX}" -name .debug -prune -exec rm -rf {} \;
apt-get purge -qy --auto-remove bzip2 ca-certificates curl file g++ gcc libicu-dev libncurses-dev libtommath-dev make zlib1g-dev
rm -rf /var/lib/apt/lists/*

mkdir -p "${PREFIX}/skel/"
mv "${VOLUME}/system/security3.fdb" "${PREFIX}/skel/security3.fdb"

sed -i 's/^#DatabaseAccess/DatabaseAccess/g' "${VOLUME}/etc/firebird.conf"
sed -i "s~^\(DatabaseAccess\s*=\s*\).*$~\1Restrict ${DBPATH}~" "${VOLUME}/etc/firebird.conf"

sed -i 's/^#RemoteAccess = true/RemoteAccess = false/g' "${VOLUME}/etc/firebird.conf"

mv "${VOLUME}/etc" "${PREFIX}/skel"
