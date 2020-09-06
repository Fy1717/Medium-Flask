#!/usr/bin/python

import mysql.connector
Host = "frknyldz.site"
Database = "frknyldz21_hwblog"
User = "frknyldz21_fy"
Password = "furkan123."

connect = mysql.connector.connect(host=Host, database=Database, user=User, password=Password, use_pure=True)

print("Baglandi", connect.get_server_info())