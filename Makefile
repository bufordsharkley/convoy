freeze:
	    env/bin/python freeze.py

server: freeze
	    cd build && python -m SimpleHTTPServer
