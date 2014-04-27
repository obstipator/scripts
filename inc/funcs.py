
import sys, os, ConfigParser, inspect

scriptsPath = os.path.dirname('%s' % os.path.abspath('%s/../' % inspect.getfile(inspect.currentframe()))).replace('\\', '/')

configPath = os.path.dirname('%s/config/' % scriptsPath)
tempPath = os.path.dirname('%s/temp/' % scriptsPath)
incPath = os.path.dirname('%s/inc/' % scriptsPath)
metaPath = os.path.dirname('%s/meta/' % scriptsPath)

def getConfig(iniName, section, key):
	config = ConfigParser.ConfigParser()
	config.read('%s/config/%s.ini' % (scriptsPath, iniName))

	if not config.has_section('Paths') :
		sys.exit('Invalid config/%s.ini' % iniName)

	if config.has_option(section, key) :
		return config.get(section, key)
	else :
		print 'config/%s.ini\'s [%s] is missing "%s" key' % (iniName, section, key)
		sys.exit(1)
#
def pause():
	raw_input('Press Enter to continue...')
#