#!/bin/zsh

rm -f /home/smullins/PycharmProjects/SABER-CEG498X/database/saber.db
rm -f /home/smullins/PycharmProjects/SABER-CEG498X/database/saber-server.db
touch saber.db

touch saber-server.db

rm -f /home/smullins/PycharmProjects/SABER-CEG498X/transmission/prep/received_images/*

#/home/smullins/PycharmProjects/SABER-CEG498X/.venv/bin/python /home/smullins/PycharmProjects/SABER-CEG498X/main.py