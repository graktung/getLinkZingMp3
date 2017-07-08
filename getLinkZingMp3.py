try:
	import requests
except ModuleNotFoundError:
	print('[X] Module {} not found.'.format("'requests'"))
	exit()	
except:
	print('[X] Something went wrong when trying to import module', "'requests'")
	exit()

try:
	import re
except ModuleNotFoundError:
	print('[X] Module {} not found.'.format("'re'"))
	exit()
except:	
	print('[X] Something went wrong when trying to import module', "'re'")
	exit()

try:
	import urllib.request as urRequest
except ModuleNotFoundError:
	print('[X] Module {} not found.'.format("'urllib.request'"))
	exit()
except:
	print('[X] Something went wrong when trying to import module', "'urllib.request'")
	exit()

from sys import argv

standardLenArgv = 2
if len(argv) == standardLenArgv:
	oriLink = argv[1]
	print('[+] LinkOfSong:', oriLink)
else:
	if len(argv) == 1:
		oriLink = input('Enter the link of song: ')
	else:
		print("[X] run script by command:\n\
			==> python getLinkZingMp3.py linkOfSong")
		exit()

try:
	requestOri = requests.get(oriLink)
	HTMLOri = requestOri.text
	regexTitle = r'<title>.+\|'
	matchTitle = re.search(regexTitle, HTMLOri)
	if matchTitle is not None:
		filenameToSave = matchTitle.group().rstrip(' |').replace('<title>', '') + '.mp3'
		filenameToSave = filenameToSave.replace('/', ' - ')
		filenameToSave = filenameToSave.replace('\\', ' - ')
		if len(filenameToSave) > 100:
			filenameToSave = 'filenameTooLong.mp3'
	else:
		filenameToSave = 'Unknowed.mp3'
except:
	print('[X] Something went wrong when trying to get source from', oriLink)
	exit()

print('[*] Getting source ID...')
regexData_xml_get_source = r'data-xml="\/json\/song\/get-source\/\w+"'
data_xml_get_source = re.search(regexData_xml_get_source, HTMLOri)
if data_xml_get_source is not None:
	sourceID = data_xml_get_source.group().rstrip('"').split('/')[-1]
else:
	print('[X] Cannot find the {}'.format("'data_xml'"))
	exit()

print('[+] Source ID:', sourceID)

print('[*] Sending request to get XML Data...')
try:
	linkXML = 'http://mp3.zing.vn/xml/song-xml/' + sourceID
	requestXML = requests.get(linkXML)
	HTMLXML = requestXML.text
	print('[+] Got HTML Source from {} successfully!'.format(linkXML))
except:
	print('[X] Something went wrong when trying to send request to', linkXML)
	exit()

print('[*] Get link source...')
regexSource = r'http:\/\/zmp3-mp3-s1-tr\.zadn\.vn\/.+\/.+\?key=.+&expires=\d+'
matchSource = re.search(regexSource, HTMLXML)

if matchSource is not None:
	linkSource = matchSource.group()
	print('[+] Link Source:', linkSource)
else:
	print('[X] Cannot find {}'.format("'Link Source'"))
	exit()

print('[*] Saving %r...' % filenameToSave)
try:
	urRequest.urlretrieve(linkSource, filenameToSave)
	print('==> File is saved succesfully!')
except:
	print('XXXX Something went wrong when trying to save file')
