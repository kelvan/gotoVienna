#select name, lat, lon from stations where lat > 48.23739 and lat < 48.2424 and lon > 16.31106 and lon < 16.3203
import defaults
import sqlite3

def get_nearby_stations(lat, lon):
    conn = sqlite3.connect(defaults.sql_file)
    c = conn.cursor()
    c.execute(defaults.sql_gps_query, (lat - 0.004, lat + 0.004, lon - 0.005, lon + 0.005))
    return map(lambda x: x[0], list(set(c.fetchall())))
