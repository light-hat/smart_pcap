#!/bin/bash

read_value() {
  read -p "$1: " value
  echo $value
}

api_url=$(read_value "API URL")
api_port=$(read_value "API PORT")
postgres_host=$(read_value "POSTGRES HOST")
postgres_port=$(read_value "POSTGRES PORT")
postgres_user=$(read_value "POSTGRES USER")
postgres_password=$(read_value "POSTGRES PASSWORD")
postgres_db=$(read_value "POSTGRES DB")
gf_security_admin_password=$(read_value "GF SECURITY ADMIN PASSWORD")
gf_security_admin_user=$(read_value "GF SECURITY ADMIN USER")

content="API_URL=${api_url}
API_PORT=${api_port}
POSTGRES_HOST=${postgres_host}
POSTGRES_PORT=${postgres_port}
POSTGRES_USER=${postgres_user}
POSTGRES_PASSWORD=${postgres_password}
POSTGRES_DB=${postgres_db}
GF_SECURITY_ADMIN_PASSWORD=${gf_security_admin_password}
GF_SECURITY_ADMIN_USER=${gf_security_admin_user}"

echo "$content" > .env

echo "OK"
