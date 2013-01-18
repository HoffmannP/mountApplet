#!/usr/bin/env python

import pygtk
import sys
pygtk.require('2.0')

import mateapplet
import gtk

import subprocess

class switchButton:
	state = 'offline'
	image = None
	button = None
	applet = None

	def __init__(self, applet):
		self.image = gtk.Image()
		self.set_image()
		self.button = gtk.Button()
		self.button.set_relief(gtk.RELIEF_NONE)
		self.button.set_image(self.image)
		self.button.connect('button-press-event', self.clicked)
		self.applet = applet
		self.applet.add(self.button)

	def mount(self):
		return 'online'
	def umount(self):
		return 'offline'

	def clicked(self, widget, event):
		widget.emit_stop_by_name("button_press_event")
		return {
			1:	self.leftClick,
			3:	self.rightClick
		}[event.button]()

	def leftClick(self):
		self.state = {
			'offline': self.mount,
			'online':   self.umount
		}[self.state]()
		self.set_image()
		return True

	def rightClick(self):
		propxml="""
			<popup name="button3">
			<menuitem name="Item 3" verb="Preferences" label="Preferences" pixtype="stock" pixname="gtk-preferences"/>
			</popup>"""
		verbs = [("Preferences", self.editPreferences)]
		self.applet.setup_menu(propxml, verbs, None)
		return False

	def editPreferences(self, widget, menuentry):
		window = gtk.Window()
		window.connect("delete-event", gtk.main_quit)
		window.set_border_width(10)
		// gconf
		button = gtk.Button("Hello World")
		window.add(button)

		window.show_all()
		gtk.main()

	def set_image(self):
		self.image.set_from_file('/home/ber/Code/mate-panel-python-applet-example/' + self.state + '.png')

def start(applet, iid):
	sw = switchButton(applet)
	sw.applet.show_all()
	return

# If applet is run directly from the command line with the -d debug option we create a window to host it
if len(sys.argv) == 2:
	if sys.argv[1] == "-d":
		mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		mainWindow.set_title("System Panel")
		mainWindow.connect("destroy", gtk.main_quit)
		applet = mateapplet.Applet()
		start(applet, None)
		applet.reparent(mainWindow)
		mainWindow.show_all()
		gtk.main()
		sys.exit()

if __name__ == '__main__':
	print "Starting factory"
	mateapplet.matecomponent_factory("OAFIID:Mount_Applet_Factory", mateapplet.Applet.__gtype__, "Simple mount applet", "1.0", start)
