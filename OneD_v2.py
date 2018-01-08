import psycopg2
import sys
import requests
import time
from lxml import html


dsn_database = "postgres"            # e.g. "compose"
dsn_hostname = "localhost" # e.g.: "aws-us-east-1-portal.4.dblayer.com"
dsn_port = "5433"                 # e.g. 11101 
dsn_uid = "postgres"        # e.g. "admin"
dsn_pwd = "polo_111"      # e.g. "xxx"
try:
    conn_string = "host="+dsn_hostname+" port="+dsn_port+" dbname="+dsn_database+" user="+dsn_uid+" password="+dsn_pwd
    print("Connecting to database\n  ->%s" % (conn_string))
    conn=psycopg2.connect(conn_string)
    print("Connected!\n")
except:
    print("Unable to connect to the database.")



cursor = conn.cursor()
#cursor.execute("""SELECT datname from pg_database""")
#rows = cursor.fetchall()

#cursor.execute("DROP TABLE IF EXISTS twitter_OD2")
cursor.execute("CREATE TABLE IF NOT EXISTS twitter_OD2 (Numero_mesure int, Nombre_de_follower int, Date date, Heure varchar(8))")
"""cursor.execute("votre_date date NOT NULL DEFAULT '0000-00-00'")
cursor.execute("heure time NOT NULL DEFAULT '00:00:00'")"""

try:
    cursor.execute("SELECT MAX(numero_mesure) FROM twitter_OD2")
    Nmesure = cursor.fetchall()[0][0] + 1
    print("Nmesure Suite")
except:
    Sample=1
    print("Nmesure à 0")


#cursor.execute("IF EXISTS (SELECT MAX(numero_mesure) FROM twitter_OD2)")
#cursor.execute("(SELECT MAX(numero_mesure) FROM twitter_OD2) IF EXISTS twitter_OD2")
#Nmesure = cursor.fetchall()[0][0] + 1


for i in range (5):
    website = requests.get('https://twitter.com/onedirection?lang=fr')
    tree=html.fromstring(website.content)
    followers=tree.xpath("//a[@data-nav='followers']/span/@data-count")[0]
        
    date = time.strftime("%d/%m/%Y")
    heure = time.strftime("%H:%M:%S")
    print(str(followers) + ' ' + date + ' ' + heure)
    

    #cursor.execute("INSERT INTO twitter_OD2 VALUES ('"+ Nmesure +"')")
    cursor.execute("INSERT INTO twitter_OD2 VALUES ('"+ str(Nmesure) +"','"+ str(followers) +"','"+ str(date) +"','"+ str(heure) +"')")

    conn.commit()
    Nmesure += 1
    time.sleep(5)

conn.close()