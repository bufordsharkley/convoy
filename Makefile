freeze:
	    source env/bin/activate && python freeze.py

server: freeze
	    cd build && python -m SimpleHTTPServer
