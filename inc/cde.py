
# doskey cde=C:/scripts/cde.bat $1

import sys, ConfigParser


path = sys.argv[1]

config = ConfigParser.ConfigParser()
config.read('C:/scripts/config/cde.ini')

if not config.has_section('Paths') :
	sys.exit('Invalid cde.ini')

if config.has_option('Paths', path) :
	print config.get('Paths', path)
else :
	print path
#
