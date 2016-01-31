#!/usr/bin/env bash

echo "$(date '+%Y-%m-%d %H-%M-%S') Starting ..."


function execute_tests {

  if [ -f /var/log/mysql/mysql.log ]; then
    rm /var/log/mysql/mysql.log
  fi
  if [ -f /var/log/mysql/mysql-slow.log ]; then
    rm /var/log/mysql/mysql-slow.log
  fi
  echo -n "" > /var/log/apache2/access.log

  echo "$(date '+%Y-%m-%d %H-%M-%S') Re-setup MySQL ..."
  mysql -e "DROP DATABASE owncloud; CREATE DATABASE owncloud; SET GLOBAL general_log = $1;"
  rm -rf /var/www/owncloud/config/config.php /var/www/owncloud/data/*

  echo "$(date '+%Y-%m-%d %H-%M-%S') Checkout commit $2 ..."
  cd /var/www/owncloud
  git fetch
  git checkout -q $2 || exit 1
  git submodule update

  echo "$(date '+%Y-%m-%d %H-%M-%S') Install owncloud ..."
  sudo -u www-data php occ maintenance:install --admin-pass=admin --database=mysql --database-name=owncloud --database-user=owncloud --database-pass=owncloud

  mkdir -p /tmp/performance-tests
  currentTime=$(date +%Y-%m-%d.%H-%M-%S)
  echo "$(date '+%Y-%m-%d %H-%M-%S') Running performance test ..."
  DAV_USER=admin DAV_PASS=admin /root/administration/performance-tests-c++/webdav-benchmark http://localhost/remote.php/webdav/ -csv > /tmp/performance-tests/$currentTime.csv

  if [ -f /var/log/mysql/mysql.log ]; then
    mv /var/log/mysql/mysql.log /tmp/performance-tests/mysql-general-query-$currentTime.log
  fi
  if [ -f /var/log/mysql/mysql-slow.log ]; then
    mv /var/log/mysql/mysql-slow.log /tmp/performance-tests/mysql-slow-query-$currentTime.log
  fi

  cp /var/log/apache2/access.log /tmp/performance-tests/access-$currentTime.log
}

if [ -z "$1" ]; then
    echo "Please specify the commit to test"
    exit 1;
fi

echo "$(date '+%Y-%m-%d %H-%M-%S') Running WITHOUT general query logger ... "
execute_tests 0 $1
echo "$(date '+%Y-%m-%d %H-%M-%S') Running WITH general query logger ... "
execute_tests 1 $1

echo "$(date '+%Y-%m-%d %H-%M-%S') Finished"
