#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess

class mountApp:
	"""A simple class that handles network mounts and receives information from /etc/fstab"""
	mountPoint = None
	mountLine = None
	mountFrom = None
	
	def __init__(self, mP):
		self.mountPoint = mP

		fstab = open("/etc/fstab", "r")
		line = fstab.readline()
		while len(line) != 0:
			fields = line.split()
			if len(fields) > 1 and fields[1] == self.mountPoint:
				self.mounted = True
				break
			line = fstab.readline()
		fstab.close()
		self.mountLine = line
		self.mountFrom = fields[0]
		self.status()

	def status_mount(self):
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
		fields = self.mountFrom.split('/')
		for server in fields:
			if server != '':
				break
		if server == '':
			return False
		devNull = open("/dev/null", "w")
		status = False if subprocess.call(["/bin/ping", "-c 1", "%s" % server], stdout=devNull, stderr=devNull) else True
		return status

	def status(self):
		print "Mounted:   %s" % ("yes" if self.status_mount() else "no")
		print "Available: %s" % ("yes" if self.status_network() else "no")

	def mount(self):
		if (self.status_mount()):
			return True
		devNull = open("/dev/null", "w")
		retval = subprocess.call(["mount", "%s" % self.mountPoint], stdout=devNull, stderr=devNull)
		return False if retval else True

	def umount(self):
		if not self.status_mount():
			return True
		devNull = open("/dev/null", "w")
		retval = subprocess.call(["umount", "%s" % self.mountPoint], stdout=devNull, stderr=devNull)
		return False if retval else True

if __name__ == '__main__':
	ma = mountApp('/mnt/Projekt')
	# print "Status now mounted" if ma.mount() else ("Error mounting %s" % ma.mountPoint)
	print "Status now unmounted" if ma.umount() else ("Error unmounting %s" % ma.mountPoint)
	ma.status()
