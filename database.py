import os
import psycopg2
import urlparse

# Setup connection
urlparse.uses_netloc.append("postgres")

# for deployment; make sure local and remote db are synced
#url = urlparse.urlparse(os.environ['DATABASE_URL'])

# local testing
url = urlparse.urlparse('postgresql://localhost/localdb')

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()
#--
def email_in_use(email):
    sql_string = "SELECT * FROM users WHERE email ='" + email + "'"
    cur.execute(sql_string)
    return not cur.fetchone() == None

# should never be passed an email in use, taken care of on frontend
def add_user(email, password):
    if email_in_use(email):
        return "Email in use"
    sql_string = "INSERT INTO users VALUES('"+email+"','"+password+"')"
    cur.execute(sql_string)
    conn.commit()

def del_user(email):
    sql_string = "DELETE FROM users WHERE email = '" + email + "'"
    cur.execute(sql_string)
    conn.commit()
    
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

"""
# Get data
cur.execute("SELECT * FROM users")
rows = cur.fetchall()
for row in rows:
    print row
"""
