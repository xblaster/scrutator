@echo off
python -O -tt -c "import Pyro.wxnsc,sys; Pyro.wxnsc.main(sys.argv[1:])" %*
