from os import path

# route search
folder = path.dirname(__file__)
action = 'http://efa.vor.at/wvb/XSLT_TRIP_REQUEST2'
hist_file = path.join(folder, '.wl_history')

# iTip

line_overview = 'http://www.wienerlinien.at/itip/linienwahl/'
stations = 'http://www.wienerlinien.at/itip/haltestelle?letter=%s'
