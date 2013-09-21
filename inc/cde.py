
# doskey cde=C:/scripts/cde.bat $1

import sys, ConfigParser, os, inspect


path = sys.argv[1]

scriptPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

config = ConfigParser.ConfigParser()
config.read('%s/../config/cde.ini' % scriptPath)

if not config.has_section('Paths') :
	sys.exit('Invalid cde.ini')

if config.has_option('Paths', path) :
	print config.get('Paths', path)
else :
	print path
#
