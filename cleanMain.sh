#!/bin/bash

rm -f "$PWD"/database/saber.db
rm -f "$PWD"/database/saber-server.db
rm -f "$PWD"/database/images/received/*

touch "$PWD"/database/saber-server.db
touch "$PWD"/database/saber.db

chmod 777 "$PWD"/database/saber-server.db
chmod 777 "$PWD"/database/saber.db
chown "$USER" "$PWD"/database/saber.db
chown "$USER" "$PWD"/database/saber-server.db
whoami