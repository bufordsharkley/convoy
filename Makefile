freeze_cocktail:
	    env/bin/python freeze.py cocktail

freeze_convoy:
	    env/bin/python freeze.py convoy

server_cocktail: freeze_cocktail
	    cd cocktail_build && python -m SimpleHTTPServer

server_convoy: freeze_convoy
	    cd convoy_build && python -m SimpleHTTPServer
