import sqlite3

conn = sqlite3.connect("latestDatabase.db")
print("Opened database successfully")

conn.execute(
    "CREATE TABLE NEXUS_LATEST_RESULTS (row_id INTEGER PRIMARY KEY ASC, \
                                    create_date DATE, \
                                    docker_tag varchar2(20), \
                                    service_name VARCHAR2(30), \
                                    jenkins_url VARCHAR2(200), \
                                    nexusiq_url  VARCHAR2(200), \
                                    yarn_log  VARCHAR2(4000))"
)
print("Table created successfully")
conn.close()

####
## This needs refactored - stop-gap for transitioning old nexus-dashboard.
## This only creates the 'latestDatabase.db' the 'main' (app.db) is created and handled by SqlAlchemy
## Will refactor lator to include a 'latest' table within app.db, and query it for the two nexus calls.
