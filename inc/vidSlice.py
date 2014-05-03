
# helps you cut out a segment of a video


import sys, os, re, ntpath, ConfigParser, inspect, subprocess

def timecodeToTime(timecode):
	timeData = timecode.split(':')
	sec = float(re.split(',', timeData[2])[0])
	return float(timeData[0]) * 3600 + float(timeData[1]) * 60 + sec
	return timeData
#

def timecodeToSec(timecode):
	DHMS = [1, 60, 60*60, 24*60*60]
	length = sum(a * b for a,b in zip(DHMS, map(float, reversed(timecode.split(":")))))
	return length
#

durationStr = ''
duration = 0

def getDuration(filename):
	global duration
	global durationStr
	cmd = '%s/inc/ffmpeg.exe -i "%s" 2>&1' % (scriptsPath, filename)
	ffmpegInfo = os.popen(cmd).read();
	durationStr = (re.search(r".*?Duration: (\d+:\d+:\d+\.\d+),", ffmpegInfo, re.MULTILINE)).group(1)

	duration = timecodeToTime(durationStr)
	return duration
#

inDir = sys.argv[1]

# just in case the file has spaces and ughhhhh:
filename = ' '.join(sys.argv[2:])
ext = os.path.splitext(filename)[1][1:]

scriptsPath = os.path.dirname(os.path.abspath('%s/../' % inspect.getfile(inspect.currentframe())))#.replace('\\', '/')

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

if config.has_option('Paths', 'vlcDir') :
	vlcDir = config.get('Paths', 'vlcDir')
else :
	print 'no vlcDir set in config/ffmpeg.ini!'
	sys.exit(1)
#

outFilename = ntpath.basename(os.path.splitext(filename)[0])

good = '0'
startTime = 0
endTime = -1

while(good != '1') :
	if(good == '0') :
		startTime = timecodeToSec(raw_input("Start time?"));
	else :
		startTime = timecodeToSec(good)
	# ffmpeg -ss 00:18:14 -i 24.s03e03.ws.dvdrip.xvid-sfm.avi -t 00:00:16 -vcodec copy -acodec copy -y 24temp1.avi
	#OLD: subprocess.call(['%s/inc/ffmpeg.exe' % scriptsPath, '-ss', ('%f' % startTime), '-y', '-i', filename, '-force_key_frames', ('%f' % startTime), '-t', '5', '-vcodec', 'copy', '-acodec', 'copy', '%s/temp/vidSliceTemp.%s'  % (scriptsPath, ext)])
	
	# new:
	subprocess.call(['%s/inc/ffmpeg.exe' % scriptsPath, '-i', filename, '-ss', ('%f' % startTime), '-t', '5','-c:v','libx264', '-y', '%s/temp/vidSliceTemp.%s'  % (scriptsPath, ext)])
	

	# this gets keyframed results (its offset). lets find out by how much
	offset = getDuration("%s/temp/vidSliceTemp.%s" % (scriptsPath, ext)) - 5
	
	#if(offset > 1110.02) :
	#	subprocess.call(['%s/inc/ffmpeg.exe' % scriptsPath, '-i', '%s/temp/vidSliceTemp.%s'  % (scriptsPath, ext), '-force_key_frames', '%f' % offset, '-vcodec', 'copy', '-acodec', 'copy', '-y', '%s/temp/tempKeyOffset.%s'  % (scriptsPath, ext)])
	#	
	#	subprocess.call(['%s/inc/ffmpeg.exe' % scriptsPath, '-ss', '%f' % offset, '-i', '%s/temp/tempKeyOffset.%s' % (scriptsPath, ext), '-vcodec', 'copy', '-acodec', 'copy', '-y', '%s/temp/vidSliceTemp.%s'  % (scriptsPath, ext)])
	#
	print "\n\nPlaying starting at %s" % (startTime)
	print "\n\n\nNote: video start is offset %fs theres nothing I can do about it" % -offset

	# play the vid with vlc
	subprocess.call(['%s/vlc.exe' % vlcDir, '-vvv', '%s/temp/vidSliceTemp.%s' % (scriptsPath, ext), '--video-on-top', '--no-loop', '--play-and-exit'])
	
	good = raw_input("%f is good? (1/0)?" % (startTime))
#


getDuration(filename)

good = '0'
while (good != '1') :
	if(good == '0') :
		endTime = timecodeToSec(raw_input("End time? currently %f sec  (%s" % (duration, durationStr)))
	else :
		endTime = timecodeToSec(good)
	if(endTime > duration) :
		endTime = duration
	if(endTime <= startTime) :
		print "Invalid time"
		good = '0'
		continue
	subprocess.call([("%s/inc/ffmpeg.exe" % scriptsPath), '-ss', ('%f' % max(endTime - 5, 0)), '-i', filename, '-t', '5','-c:v','libx264', '-y', ("%s/temp/vidSliceTemp.%s" % (scriptsPath, ext))])
	
	print "\n\nPlaying ending at %s" % (endTime)
	
	subprocess.call(['%s/vlc.exe' % vlcDir, '-vvv', '%s/temp/vidSliceTemp.%s' % (scriptsPath, ext), '--video-on-top', '--no-loop', '--play-and-exit'])
	
	good = raw_input("%f is good? (1/0)?" % (endTime))
#

ext = 'mp4'

subprocess.call([("%s/inc/ffmpeg.exe" % scriptsPath), '-i', filename, '-ss', ('%f' % startTime), '-t', ('%f' % (endTime - startTime)), '-c:v','libx264', '-preset', 'placebo', '-y', '%s/temp/vidSliceOut.%s' % (scriptsPath, ext)])

#subprocess.call(['copy', '%s/temp/vidSliceOut.%s' % (scriptsPath, ext), '"%s/%s_sliced_%s-%s.%s"' % (outDir, outFilename, startTime, endTime, ext)])

print "\n\nUses range %f - %f" % (startTime, endTime)
raw_input('\nDone processing. Press enter to view.')

print ['%s/vlc.exe' % vlcDir, '-vvv', '%s/temp/vidSliceOut.%s' % (scriptsPath.replace('\\', '/'), ext), '--video-on-top', '--no-loop', '--play-and-exit']

subprocess.call(['%s/vlc.exe' % vlcDir, '-vvv', '%s/temp/vidSliceOut.%s' % (scriptsPath, ext), '--video-on-top', '--no-loop', '--play-and-exit'])

uploadConfirm = raw_input('Want to save a copy of this on your filesystem?')
while (uploadConfirm != 'y' and uploadConfirm != 'n') :
	uploadConfirm = raw_input('save to ffmpegOut/ dir? (y/n)?')
#

#cmd = 'copy "%s/temp/vidSliceOut.%s" "%s/%s_sliced_%s-%s.%s" /y' % (scriptsPath.replace('\\', '/'), ext, outDir, outFilename, startTime, endTime, ext)
#os.system(cmd)

print '%s/temp/vidSliceOut.%s' % (scriptsPath.replace('\\', '/'), ext)
print '%s/%s_sliced_%s-%s.%s' % (outDir, outFilename, startTime, endTime, ext)

subprocess.call(['cp', '%s/temp/vidSliceOut.%s' % (scriptsPath.replace('\\', '/'), ext), '%s/%s_sliced_%s-%s.%s' % (outDir, outFilename, startTime, endTime, ext)]);


os.system('pushd "%s" && toHd "%s_sliced_%s-%s.%s" && popd' % (outDir, outFilename, startTime, endTime, ext))
if(uploadConfirm == 'y') :
	print "\n\nCreated file out/%s_sliced_%s-%s.%s" % (outFilename, startTime, endTime, ext)
else :
	os.system('del "%s/%s_sliced_%s-%s.%s"' % (outDir, outFilename, startTime, endTime, ext))
#
print "uploaded to HD"

# ffmpeg -ss 00:18:14 -i 24.s03e03.ws.dvdrip.xvid-sfm.avi -t 00:00:16 -vcodec copy -acodec copy -y 24temp1.avi

uploadConfirm = raw_input('Upload to youtube?')
while (uploadConfirm != 'y' and uploadConfirm != 'n') :
	uploadConfirm = raw_input('what??? upload to youtube (y/n)?')
#

if(uploadConfirm == 'y') :
	print '\nNO! DONT!';
	#subprocess.call(['python', '%s/inc/youtubeVidUpload.py' % scriptsPath, '--noauth_local_webserver', '--privacyStatus', 'unlisted', '--file', '%s/%s_sliced_%s-%s.%s' % (outDir, outFilename, startTime, endTime, ext)])
#
#youtubeVidUpload.py --noauth_local_webserver --privacyStatus unlisted --file "E:\downloads\ffmpegOut\24.s03e03.ws.dvdrip.xvid-sfm_sliced_1094.0-1110.0.avi"

