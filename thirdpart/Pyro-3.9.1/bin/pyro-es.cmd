@echo off
python -O -tt -c "from Pyro.EventService import Server; import sys; Server.start(sys.argv[1:])" %*
