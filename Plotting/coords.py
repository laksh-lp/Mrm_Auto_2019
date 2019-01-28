from position import pos_update

def coordinates():
	startlat,startlon = pos_update()

	endlat = 13.3504603   
	endlon = 74.7915926
	
	waylat1 = 13.3505011
	waylon1 = 74.7913021

	waylat2 = 0
	waylon2 = 0

	waylat3 = 0
	waylon3 = 0

	waylat4 = 0
	waylon4 = 0

	waylat5 = 0
	waylon5 = 0

	waylat6 = 0
	waylon6 = 0

	return [startlat,startlon,endlat,endlon,waylat1,waylon1,waylat2,waylon2,waylat3,waylon3,waylat4,waylon4,waylat5,waylon5,waylat6,waylon6]
