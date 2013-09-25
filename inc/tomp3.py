
import sys, ConfigParser, os, inspect, subprocess

# just in case the file has spaces and ughhhhh:
inFile = ' '.join(sys.argv[1:])

scriptPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

config = ConfigParser.ConfigParser()
config.read('%s/../config/ffmpeg.ini' % scriptPath)

if not config.has_section('Paths') :
	sys.exit('Invalid config/ffmpeg.ini')

if config.has_option('Paths', 'out') :
	outDir = config.get('Paths', 'out')
else :
	print 'no out dir!'
	sys.exit(1)
#

outFile = '%s/%s.mp3' % (outDir, os.path.splitext(inFile)[0])
subprocess.call([('%s/ffmpeg.exe' % scriptPath), '-i', inFile, outFile])






