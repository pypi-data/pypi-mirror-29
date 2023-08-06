
import os


class rdp(object):


	def __init__(self, address = '', file = '', port = 3389, width = 0, height = 0, fullscreen = False, colorbit = 32, multimon = False, audio = False, devices = False):
		super(rdp, self).__init__()
		self.address = address
		self.file = file
		self.port = port
		self.width = width
		self.height = height
		self.fullscreen = fullscreen
		self.colorbit = colorbit
		self.multimon = multimon
		self.audio = audio
		self.devices = devices
		

	def connect(self):
		connect_args = ''
		if self.file != '':
			connect_args = ' ' + self.file
		else:
			connect_args = ' /v ' + self.address + ':' + str(self.port)
		if self.multimon:
			connect_args = connect_args + ' /multimon'
		else:
			if self.width == 0 and self.height == 0 and self.fullscreen:
				connect_args = connect_args + ' /f'
			if self.width > 0 and self.height > 0:
				connect_args = connect_args + ' /w ' + str(self.width) + ' /h ' + str(self.height)
		os.system('mstsc.exe' + connect_args)


	def save_file(self, file_name):
		file = open(file_name + '.rdp', 'w')
		if self.width == 0 and self.height == 0 and self.fullscreen:
			file.write('screen mode id:i:2' + '\n')
		if self.width > 0 and self.height > 0:
			file.write('screen mode id:i:1' + '\n')
			file.write('desktopwidth:i:' + str(self.width) + '\n')
			file.write('desktopheight:i:720:i:' + str(self.height) + '\n')
		file.write('session bpp:i:' + str(self.colorbit))
		if self.multimon:
			file.write('use multimon:i:1\n')
		else:
			file.write('use multimon:i:0\n')
		file.write('winposstr:s:0,3,0,0,0,0\n')
		file.write('compression:i:1\n')
		if self.audio:
			file.write('audiocapturemode:i:1\n')
			file.write('audiomode:i:1\n')
		else:
			file.write('audiocapturemode:i:0\n')
			file.write('audiomode:i:0\n')
		file.write('videoplaybackmode:i:1\n')
		file.write('connection type:i:7\n')
		file.write('networkautodetect:i:1\n')
		file.write('bandwidthautodetect:i:1\n')
		file.write('displayconnectionbar:i:1\n')
		file.write('enableworkspacereconnect:i:0\n')
		file.write('disable wallpaper:i:0\n')
		file.write('allow font smoothing:i:0\n')
		file.write('allow desktop composition:i:0\n')
		file.write('disable full window drag:i:1\n')
		file.write('disable menu anims:i:1\n')
		file.write('disable themes:i:0\n')
		file.write('disable cursor setting:i:0\n')
		file.write('bitmapcachepersistenable:i:1\n')
		file.write('full addresss:s:' + self.address + ':' + str(self.port) + '\n')
		if self.devices:
			file.write('redirectprinters:i:1\n')
			file.write('redirectcomports:i:1\n')
			file.write('redirectsmartcards:i:1\n')
			file.write('redirectclipboard:i:1\n')
			file.write('redirectposdevices:i:1\n')
		else:
			file.write('redirectprinters:i:0\n')
			file.write('redirectcomports:i:0\n')
			file.write('redirectsmartcards:i:0\n')
			file.write('redirectclipboard:i:0\n')
			file.write('redirectposdevices:i:0\n')
		file.write('autoreconnection enabled:i:1\n')
		file.write('authentication level:i:0\n')
		file.write('prompt for credentials:i:1\n')
		file.write('negotiate security layer:i:1\n')
		file.write('remoteapplicationmode:i:0\n')
		file.write('alternate shell:s:\n')
		file.write('shell working directory:s:\n')
		file.write('gatewayhostname:s:\n')
		file.write('gatewayusagemethod:i:4\n')
		file.write('gatewaycredentialssource:i:4\n')
		file.write('gatewayprofileusagemethod:i:0\n')
		file.write('promptcredentialonce:i:0\n')
		file.write('gatewaybrokeringtype:i:0\n')
		file.write('use redirection server name:i:0\n')
		file.write('rdgiskdcproxy:i:0\n')
		file.write('kdcproxyname:s:\n')
		file.write('drivestoredirect:s:\n')

