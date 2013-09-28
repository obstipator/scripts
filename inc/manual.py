
import sys, os, inspect, glob, ntpath

scriptsPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + '/../')).replace('\\', '/')

if(len(sys.argv) == 1) :
	files = glob.glob('%s/cmd/*.bat' % scriptsPath)
	print '\nAvailable Commands:\n'
	for filename in files :
		print ntpath.basename(os.path.splitext(filename)[0])
	#
else :
	cmd = sys.argv[1]
	filename = '%s/manuals/%s.txt' % (scriptsPath, cmd)
	if not os.path.isfile(filename) :
		print 'No manual found for %s' % cmd
		print filename
		print '\ntype manual with no arguments for a list of commands'
	else :
		file = open(filename, 'r')
		print '\n%s.bat:\n' % cmd
		with file as f:
			print ''.join(f.readlines())
#
