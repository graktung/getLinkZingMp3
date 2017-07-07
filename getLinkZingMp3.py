try:
	import requests
except:
	print('[X] Module requests not found.')
	exit()

try:
	import re
except:
	print('[X] Module re not found.')
	exit()

try:
	import urllib.request as urRequest
except:
	print('[X] Module urrlib.request')
	exit()
	
from sys import argv

standardLenArgv = 3
if len(argv) == standardLenArgv:
	oriLink = argv[1]
	filenameToSave = argv[2]
	print('[+] LinkOfSong:', oriLink)
	print('[+] filenameToSave:', filenameToSave)
else:
	print("[X] run script by command:\n\
		==> python getLinkZingMp3.py linkOfSong filenameToSave")
	exit()

oriIDLink = oriLink.split('/')[-1].split('.')[0]
linkEmbed = 'http://mp3.zing.vn/embed/song/' + oriIDLink
print('[+] LinkEmbed:', linkEmbed)
print('[*] Sending request...')

try:
	requestEmbed = requests.get(linkEmbed)
	HTMLEmbed = requestEmbed.text
	print('[+] Got HTML Source from {} successfully!'.format(linkEmbed))
except:
	print('[X] Something went wrong when trying to send request to', linkEmbed)
	exit()

print('[*] Getting source ID...')
regexData_xml_get_source = r'data-xml="\/json\/song\/get-source\/\w+"'
data_xml_get_source = re.search(regexData_xml_get_source, HTMLEmbed)
sourceID = data_xml_get_source.group().rstrip('"').split('/')[-1]
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
regexSource = r'http:\/\/zmp3-mp3-s1-tr.zadn.vn\/\w+\/\w+\?key=\w+&expires=\d+'
matchSource = re.search(regexSource, HTMLXML)
linkSource = matchSource.group()

print('[*] Saving file...')
try:
	urRequest.urlretrieve(linkSource, filenameToSave)
	print('==> File is saved succesfully!')
except:
	print('XXXX Something went wrong when trying to save file')
