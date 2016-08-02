#!/bin/bash

# config
LDAP_NAME=OpenLDAP
LDAP_LOCAL_PORT=300
PHPLDAPADMIN_LOCAL_PORT=8300
LDAP_DOMAIN=owncloud.com
LDAP_ORGANISATION=ownCloud
LDAP_ROOTPASS=admin
LDAP_MEMBEROF=false

LDAP_BASE_DN=dc=owncloud,dc=com
LDAP_LOGIN_DN=cn=admin,dc=owncloud,dc=com

docker pull dinkel/openldap > /dev/null

# start containers
if (LDAP_MEMBEROF)
{
    docker run -p $LDAP_LOCAL_PORT:389 \
        -e SLAPD_DOMAIN=$LDAP_DOMAIN \
        -e SLAPD_ORGANISATION="$LDAP_ORGANISATION" \
        -e SLAPD_PASSWORD=$LDAP_ROOTPASS \
        --name $LDAP_NAME \
        -d dinkel/openldap || exit 1
}
{
    docker run -p $LDAP_LOCAL_PORT:389 \
        -e SLAPD_DOMAIN=$LDAP_DOMAIN \
        -e SLAPD_ORGANISATION="$LDAP_ORGANISATION" \
        -e SLAPD_PASSWORD=$LDAP_ROOTPASS \
        -e SLAPD_ADDITIONAL_MODULES=memberof \
        --name $LDAP_NAME \
        -d dinkel/openldap || exit 1
}
docker pull osixia/phpldapadmin > /dev/null

#docker inspect docker-slapd | grep IP
SLAPD_CONTAINER_IP=$(docker inspect -f "{{ .NetworkSettings.IPAddress }}" $LDAP_NAME)
docker run -p $PHPLDAPADMIN_LOCAL_PORT:443 \
	--name docker-phpldapadmin-$LDAP_NAME \
	-e PHPLDAPADMIN_LDAP_HOSTS=$SLAPD_CONTAINER_IP \
	-e LDAP_BASE_DN=$LDAP_BASE_DN \
	-e LDAP_LOGIN_DN=$LDAP_LOGIN_DN \
	-d osixia/phpldapadmin || exit 2

docker ps
echo
echo "LDAP server now available under 127.0.0.1:$LDAP_LOCAL_PORT (internal IP is $SLAPD_CONTAINER_IP)"
echo "phpldapadmin now available under https://127.0.0.1:$PHPLDAPADMIN_LOCAL_PORT"
echo