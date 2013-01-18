install:
	cp mountApplet.py	/usr/local/bin/
	cp mountApplet.server /usr/lib/matecomponent/servers/
	killall mate-panel
	sleep 3s

uninstall:
	rm -f /usr/local/bin/mountApplet.py
	rm -f /usr/lib/matecomponent/servers/mountApplet.server
	killall mate-panel
	sleep 3s


