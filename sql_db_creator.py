import sqlite3
import csv

sqlite_file = 'SaginawDB.db'

# connect to database
conn = sqlite3.connect(sqlite_file)

# get cursor object
cur = conn.cursor()

#References
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# create table for nodes
cur.execute('''DROP TABLE IF EXISTS nodes''')
conn.commit()
cur.execute('''CREATE TABLE nodes(id INTEGER, lat INTEGER, lon INTEGER, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp DATE)''')
conn.commit

with open('nodes.csv','rt', encoding="utf8") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['lat'],i['lon'], i['user'],i['uid'], i['version'],i['changeset'], i['timestamp']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

# create table for nodes_tags
cur.execute('''DROP TABLE IF EXISTS nodes''')
conn.commit()
cur.execute('''CREATE TABLE nodes(id INTEGER, key TEXT, value TEXT, type TEXT)''')
conn.commit

with open('nodes_tags.csv','rt', encoding="utf8") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'],i['value'], i['type']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()



# create table for ways
cur.execute('''DROP TABLE IF EXISTS ways''')
conn.commit()
cur.execute('''CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp DATE)''')
conn.commit

with open('ways.csv','rt', encoding="utf8") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['user'],i['uid'], i['version'],i['changeset'], i['timestamp']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

# create table for ways_tags
cur.execute('''DROP TABLE IF EXISTS ways_tags''')
conn.commit()
cur.execute('''CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT, type TEXT)''')
conn.commit

with open('ways_tags.csv','rt', encoding="utf8") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'],i['value'], i['type']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO ways_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()


# create table for ways_nodes
cur.execute('''DROP TABLE IF EXISTS ways_nodes''')
conn.commit()
cur.execute('''CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)''')
conn.commit

with open('ways_nodes.csv','rt', encoding="utf8") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)
# commit the changes
conn.commit()

#Close connection
conn.close()