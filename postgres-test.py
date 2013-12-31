import os
import psycopg2
import urlparse

# Postgresql reference
# http://zetcode.com/db/postgresqlpythontutorial/

# Setup connection
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()
#--

"""
# Create new Table
# change table_name and column_info accordingly
new_table_name = 'users'
column_info = '(id INT PRIMARY KEY, username VARCHAR(20), password VARCHAR(20), name VARCHAR(100))'
cur.execute("CREATE TABLE " + new_table_name + column_info)
conn.commit()
"""

"""
# Delete Table
table_to_delete = "users"
cur.execute("DROP TABLE IF EXISTS " + table_to_delete)
conn.commit()
"""

"""
# Insert Row
cur.execute("INSERT INTO users VALUES(1,'admin','admin','Admin')")
conn.commit()
"""


# Get data
cur.execute("SELECT * FROM users")
rows = cur.fetchall()
for row in rows:
    print row

conn.close()
    
