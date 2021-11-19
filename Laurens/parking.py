#!/usr/bin/python

import time
from datetime import datetime
import MySQLdb

#Verbinden met de database
database = MySQLdb.connect(host="localhost", user="pi", passwd="raspberry", db="mydb")

plaats1 = "SELECT nummerplaat FROM parkeergarage where parkeerplaats = 1 ORDER BY aankomsttijd LIMIT 1"
plaats2 = "SELECT nummerplaat FROM parkeergarage where parkeerplaats = 2 ORDER BY aankomsttijd LIMIT 1"
plaats3 = "SELECT nummerplaat FROM parkeergarage where parkeerplaats = 3 ORDER BY aankomsttijd LIMIT 1"
plaats4 = "SELECT nummerplaat FROM parkeergarage where parkeerplaats = 4 ORDER BY aankomsttijd LIMIT 1"


print ("Content-type:text/html\n\n")
print ("<html lang=\"en\">")
print ("<head>")
#print ("<meta http-equiv=\"refresh\" content=\"5\">")
print ("<meta charset=\"UTF-8\">")
print ("<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta2/css/all.min.css\" integrity=\"sha512-YWzhKL2whUzgiheMoBFwW8CKV4qpHQAEuvilg9FAn5VJUDwKZZxkJNuGM4XkWuk94WCrrwslk8yWNGmY1EduTA==\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\" />")
print ("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">")
print ("<title>Parking</title>")
print ("<style>         body {             margin: 0;             padding: 0;             box-sizing: border-box;             display: flex;             flex-direction: column;             justify-content: center;             -ms-align-items: center;             align-items: center;             height: 100vh;         }          table,         td {             border: 7px solid black;             border-bottom: none;             border-collapse: collapse;         }          td {             width: 100px;             height: 150px;             text-align: center;             vertical-align: center;         }      #licenseplate {            font-family: Arial, sans-serif; color: #9b111e; border: 2px solid #9b111e; border-radius: 5px; padding: 3px;}</style>")
print ("<title>Parking</title>")
print ("</head>")
print ("<body>")
print ("<h2 style=\"margin-top: 0\">Waarden:</h2>")
print ("<table> <tr> <td>")
with database.cursor() as cursor1:
    cursor1.execute(plaats1)
    result = cursor1.fetchall()
    if result == ():
        print ("<i style=\"color: green\" class=\"fas fa-3x fa-check-circle\"></i>")
    else:
        for row in result:
            print ("<span id=licenseplate>" + row[0] + "</span>")
print ("</td> <td>")
with database.cursor() as cursor2:
    cursor2.execute(plaats2)
    result = cursor2.fetchall()
    if result == ():
        print ("<i class=\"fas fa-check-circle\"></i>")
    else:
        for row in result:
            print ("<span id=licenseplate>" + row[0] + "</span>")
print ("</td> <td>")
with database.cursor() as cursor3:
    cursor3.execute(plaats3)
    result = cursor3.fetchall()
    if result == ():
        print ("<i class=\"fas fa-check-circle\"></i>")
    else:
        for row in result:
            print ("<span id=licenseplate>" + row[0] + "</span>")
print ("</td> <td>")
with database.cursor() as cursor4:
    cursor4.execute(plaats4)
    result = cursor4.fetchall()
    if result == ():
        print ("<i class=\"fas fa-check-circle\"></i>")
    else:
        for row in result:
            print ("<span id=licenseplate>" + row[0] + "</span>")
print ("</td> </tr> </table>")
print ("</body>")
print ("</html>")