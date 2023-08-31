freeze_ygm_local:
	    python3 freeze.py jumper 

freeze_jumper_local:
	    python3 freeze.py ygm

freeze_cocktail_local:
	    python3 freeze.py cocktail

freeze_convoy_local:
	    python3 freeze.py convoy

server_jumper_local: freeze_jumper_local
	    cd jumper_build && python -m SimpleHTTPServer

server_ygm_local: freeze_ygm_local
	    cd ygm_build && python -m SimpleHTTPServer

server_cocktail_local: freeze_cocktail_local
	    cd cocktail_build && python -m SimpleHTTPServer

server_convoy_local: freeze_convoy_local
	    cd convoy_build && python -m SimpleHTTPServer


freeze_jumper:
	    env/bin/python freeze.py jumper

freeze_ygm:
	    env/bin/python freeze.py ygm

freeze_cocktail:
	    env/bin/python freeze.py cocktail

freeze_convoy:
	    env/bin/python freeze.py convoy

server_jumper: freeze_jumper
	    cd jumper_build && python2.7 -m SimpleHTTPServer

server_ygm: freeze_ygm
	    cd ygm_build && python2.7 -m SimpleHTTPServer

server_cocktail: freeze_cocktail
	    cd cocktail_build && python -m SimpleHTTPServer

server_convoy: freeze_convoy
	    cd convoy_build && python -m SimpleHTTPServer
