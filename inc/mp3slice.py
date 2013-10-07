
# helps you crop off the beginning and end of an mp3 with sound previews
# todo: fix timelength being wrong after encoding. this might be bit rate stuff?

import sys, os, winsound, re, ntpath, ConfigParser, inspect, subprocess, shlex

def timecodeToTime(timecode):
	timeData = timecode.split(':')
	sec = float(re.split(',', timeData[2])[0])
	return float(timeData[0]) * 3600 + float(timeData[1]) * 60 + sec
	return timeData
#
inDir = sys.argv[1]

# just in case the file has spaces and ughhhhh:
filename = ' '.join(sys.argv[2:])

scriptsPath = os.path.dirname(os.path.abspath('%s/../' % inspect.getfile(inspect.currentframe())))

config = ConfigParser.ConfigParser()
config.read('%s/config/ffmpeg.ini' % scriptsPath)

if not config.has_section('Paths') :
	sys.exit('Invalid config/ffmpeg.ini')

if config.has_option('Paths', 'out') :
	outDir = config.get('Paths', 'out')
else :
	print 'no out dir!'
	sys.exit(1)
#

outFilename = ntpath.basename(os.path.splitext(filename)[0])

good = 0
startTime = 0
endTime = -1

while(good != 1) :
	if(good == 0) :
		startTime = input("Start time?");
	else :
		startTime = good
	subprocess.call(['%s/inc/ffmpeg.exe' % scriptsPath, '-t', '5', '-y', '-i', filename, '-ss', ('%f' % startTime), "%s/temp/temp.mp3" % scriptsPath])
	subprocess.call(["%s/inc/ffmpeg.exe" % scriptsPath, '-y', '-i', "%s/temp/temp.mp3" % scriptsPath, "%s/temp/temp.wav" % scriptsPath])

	print "\n\nPlaying starting at %s" % (startTime)

	# winsound.PlaySound("inc/ding.wav", winsound.SND_FILENAME) # too delayed...
	winsound.PlaySound(("%s/temp/temp.wav" % scriptsPath), winsound.SND_FILENAME)
	good = input("%f is good? (1/0)?" % (startTime))
#

cmd = '%s/inc/ffmpeg.exe -i "%s" 2>&1' % (scriptsPath, filename)
ffmpegInfo = os.popen(cmd).read();
durationStr = (re.search(r".*?Duration: (\d+:\d+:\d+\.\d+),", ffmpegInfo, re.MULTILINE)).group(1)

duration = timecodeToTime(durationStr)

good = 0
while (good != 1) :
	if(good == 0) :
		endTime = input("End time? currently %f sec  (%s" % (duration, durationStr))
	else :
		endTime = good
	if(endTime > duration) :
		endTime = duration
	if(endTime <= startTime) :
		print "Invalid time"
		good = 0
		continue
	subprocess.call([("%s/inc/ffmpeg.exe" % scriptsPath), '-y', '-i', filename, '-ss', ('%f' % max(endTime - 5, 0)), '-t', '5', ("%s/temp/temp.mp3" % scriptsPath)])
	subprocess.call([("%s/inc/ffmpeg.exe" % scriptsPath), '-y', '-i', ('%s/temp/temp.mp3' % scriptsPath), ("%s/temp/temp.wav" % scriptsPath)])
	print "\n\nPlaying ending at %s" % (endTime)
	winsound.PlaySound(("%s/temp/temp.wav" % scriptsPath), winsound.SND_FILENAME)
	winsound.PlaySound(("%s/inc/ding.wav" % scriptsPath), winsound.SND_FILENAME)
	good = input("%f is good? (1/0)?" % (endTime))
#
subprocess.call([("%s/inc/ffmpeg.exe" % scriptsPath), '-ss', ('%f' % startTime), '-t', ('%f' % (endTime - startTime)), '-i', filename, '-y', ("%s/%s_sliced.mp3" % (outDir, outFilename))])
print "\n\nCreated file out/%s_sliced.mp3" % (outFilename)
print "Uses range %f - %f" % (startTime, endTime)





