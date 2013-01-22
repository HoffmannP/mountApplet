#!/usr/bin/env python

import pygtk
import sys

import mateapplet
import gtk

import subprocess
import os.path
import gconf
		
import mountClass

class switchButton:
	state = 'offline'
	image = None
	button = None
	applet = None
	mount = None
	window = None
	mu = None

	def __init__(self, applet):
		self.image = gtk.Image()
		self.set_image()
		self.button = gtk.Button()
		self.button.set_relief(gtk.RELIEF_NONE)
		self.button.set_image(self.image)
		self.button.connect('button-press-event', self.clicked)
		self.applet = applet
		self.applet.add(self.button)
		self.mount = mountClass.mountClass()

	def do_mount(self):
		if not self.mount.mount():
			print "Failed!"
		print self.mount.status()
		return self.mount.status()
	def do_umount(self):
		if not self.mount.umount():
			print "Failed!"
		print self.mount.status()
		return self.mount.status()
	def connectInfo(self):
		dg = gtk.Dialog(
			title = "No connection found",
			flags = gtk.DIALOG_DESTROY_WITH_PARENT,
			buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK)
		)
		text = 'Upon mounting %s you need to establish a connection to %s' % (self.mount.mountName, self.mount.mountServer)
		print text
		label = gtk.Label(text)
		dg.vbox.pack_start(label)
		label.show()
		dg.run()
		dg.destroy()
		return self.mount.status()

	def clicked(self, widget, event):
		widget.emit_stop_by_name('button-press-event')
		return {
			1:	self.leftClick,
			3:	self.rightClick
		}[event.button]()

	def leftClick(self):
		self.state = {
			'offline': self.connectInfo,
			'online':  self.do_mount,
			'mounted': self.do_umount
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

	def selectPreferences(self, widget, event):
		self.state = self.mount.status()
		print self.state
		self.set_image()
		self.button.set_tooltip_text(self.mount.mountName)
		self.window.destroy()

	def setPref(self, item):
		self.mount.select(item.get_label())

	def editPreferences(self, widget, event):
		self.window = gtk.Window()
		
		box = gtk.HBox()
		self.window.add(box)

		ic = gtk.Image()
		ic.set_from_stock(stock_id=gtk.STOCK_CONNECT, size=gtk.ICON_SIZE_BUTTON)
		box.add(ic)
		
		tx = gtk.Label(" Select Server: ")
		box.add(tx)

		mu = gtk.Menu()
		for server in self.mount.mounts():
			mi = gtk.MenuItem(server, use_underline=False)
			mi.connect('activate', self.setPref)
			mu.append(mi)
		om = gtk.OptionMenu()
		om.set_menu(mu)
		box.add(om)

		ok = gtk.Button(stock=gtk.STOCK_OK)
		ok.connect('button-press-event', self.selectPreferences)
		box.add(ok)
		
		self.window.show_all()
		gtk.main()

	def set_image(self):
		self.image.set_from_file(os.path.dirname(__file__) + '/' + self.state + '.png')

def start(applet, iid):
	sw = switchButton(applet)
	sw.applet.show_all()
	# sw.editPreferences(None, None)
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
