freeze_ygm_local:
	    uv run freeze.py jumper 

freeze_jumper_local:
	    uv run freeze.py ygm

freeze_cocktail_local:
	    uv run freeze.py cocktail

freeze_convoy_local:
	    uv run freeze.py convoy

server_jumper_local: freeze_jumper_local
	    cd jumper_build && python -m SimpleHTTPServer

server_ygm_local: freeze_ygm_local
	    cd ygm_build && python -m SimpleHTTPServer

server_cocktail_local: freeze_cocktail_local
	    cd cocktail_build && python -m SimpleHTTPServer

server_convoy_local: freeze_convoy_local
	    cd convoy_build && python -m SimpleHTTPServer


freeze_jumper:
	    uv run freeze.py jumper

freeze_ygm:
	    uv run freeze.py ygm

freeze_cocktail:
	    uv run freeze.py cocktail

freeze_convoy:
	    uv run freeze.py convoy

server_jumper: freeze_jumper
	    cd jumper_build && python2.7 -m SimpleHTTPServer

server_ygm: freeze_ygm
	    cd ygm_build && python2.7 -m SimpleHTTPServer

server_cocktail: freeze_cocktail
	    cd cocktail_build && python -m SimpleHTTPServer

server_convoy: freeze_convoy
	    cd convoy_build && python -m SimpleHTTPServer
