
import sys, ConfigParser, os, inspect, subprocess

scriptPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

config = ConfigParser.ConfigParser()
config.read('%s/../config/youtube.ini' % scriptPath)

if (not config.has_section('Users')) or (not config.has_section('Other')):
	sys.exit('Invalid config/youtube.ini')

items = config.items('Users')
rate = config.get('Other', 'rate')

for i in items :
	archiveFile = '%s/../meta/youtube/%s_downloaded.txt' % (scriptPath, i[0])
	if not os.path.isfile(archiveFile) :
		open(archiveFile, 'a').close()
	outDir = '%s%s' % (config.get('Other', 'outDir'), i[0])
	url = 'http://www.youtube.com/user/%s/videos' % i[0]
	dateAfter = i[1]
	
	subprocess.call([('%s/youtube-dl.exe' % scriptPath), '--download-archive', archiveFile, '-o', ('%s/%s' % (outDir, '%(title)s-%(id)s.%(ext)s')), '--console-title', '--rate-limit', rate, '--restrict-filenames', '--reject-title', config.get('Other', 'rejectRegex'), '--dateafter', dateAfter, url ])