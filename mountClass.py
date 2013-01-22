#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import subprocess

class mountClass:
	"""A simple class that handles network mounts and receives information from /etc/fstab"""
	mountName = None
	mountPoint = None
	mountLine = None
	mountFrom = None
	mountList = {}
	
	def __init__(self):
		self.readMounts()

	def select(self, mP):
		fstab = open("/etc/fstab", "r")
		line = fstab.readline()
		if mP not in self.readMounts().mountList:
			print "Mount %s not found!" % mP
			sys.exit(1)
		theMount = self.mountList[mP]
		self.mountName = mP
		self.mountPoint = theMount["mount"]
		self.mountLine = theMount["line"]
		self.mountFrom = theMount["share"]
		self.mountServer = theMount["server"]
		return self.status()

	def status_mount(self):
		if self.mountName is None:
			return False
		proc_mounts = open("/proc/mounts", "r")
		mounted = False
		line = proc_mounts.readline()
		while len(line) != 0:
			fields = line.split()
			if fields[1] == self.mountPoint:
				mounted = True
				break
			line = proc_mounts.readline()
		proc_mounts.close()
		return mounted
	
	def status_network(self):
		if self.mountServer is None:
			return False
		return False if subprocess.call(["/bin/ping", "-c 1", "%s" % self.mountServer], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0 else True

	def status(self):
		if self.mountName is None:
			return False
		if self.status_network():
			if self.status_mount():
				return 'mounted'
			else:
				return 'online'
		else:
			return 'offline'
		
	def mount(self):
		if self.mountName is None:
			return False
		if (self.status_mount()):
			return True
		print "mounting %s" % self.mountPoint
		return False if subprocess.call(["mount", "%s" % self.mountPoint]) != 0 else True

	def umount(self):
		if self.mountName is None:
			return False
		if not self.status_mount():
			return True
		print "umounting %s" % self.mountPoint
		return False if subprocess.call(["umount", "%s" % self.mountPoint]) != 0 else True

	def getServer(self, share, fstype):
		return {
			'cifs': lambda x: x.split('/')[2],
			'fuse': lambda x: x.split(':')[0].split('@')[1],
		}[fstype](share)

	def readMounts(self, reread = False):
		if len(self.mountList) > 0 and not reread:
			return self
		f = open('/etc/fstab')
		line = f.readline()
		while line != '':
			parts = line.split()
			if len(parts) > 2 and (parts[2] in ['fuse', 'cifs']):
				self.mountList['/'.join(parts[1].split('/')[2:])] = {
					'line':	line,
					'share': parts[0],
					'server':  self.getServer(parts[0], parts[2]),
					'mount': parts[1],
					'options': parts[3]
					}
			line = f.readline()
		f.close()
		return self

	def mounts(self):
		return [key for key in self.readMounts().mountList.keys()]

if __name__ == '__main__':
	mc = mountClass()
	print mc.mounts()
	print mc.mountList
	
