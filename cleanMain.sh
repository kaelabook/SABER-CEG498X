#!/bin/bash

rm -f "$PWD"/Database/saber.db
rm -f "$PWD"/Database/saber-server.db
rm -f "$PWD"/Database/images/received/*

touch "$PWD"/Database/saber-server.db
touch "$PWD"/Database/saber.db

chmod 777 "$PWD"/Database/saber-server.db
chmod 777 "$PWD"/Database/saber.db
chown "$USER" "$PWD"/Database/saber.db
chown "$USER" "$PWD"/Database/saber-server.db
whoami