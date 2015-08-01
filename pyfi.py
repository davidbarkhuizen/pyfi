from wifi import Cell, Scheme

cells = Cell.all('wlan0')

for cell in cells:

	print('ssid %s', cell.ssid)
	print('signal %s', cell.signal)
	print('quality %s', cell.quality)
	print('frequency %s', cell.frequency)
	print('bitrates %s', cell.bitrates)
	print('encrypted %s', cell.encrypted)
	if cell.encrypted == True:
		print('encryption_type %s', cell.encryption_type)
	print('channel %s', cell.channel)
	print('address %s', cell.address)
	print('mode %s', cell.mode)


'''
cell = Cell.all('wlan0')[0]
>>> scheme = Scheme.for_cell('wlan0', 'home', cell)
>>> scheme.save()
>>> scheme.activate()

Once you have a scheme saved, you can retrieve it using Scheme.find().

>>> scheme = Scheme.find('wlan0', 'home')
>>> scheme.activate()
'''
