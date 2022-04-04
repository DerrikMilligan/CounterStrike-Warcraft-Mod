import es
import usermsg

from ..admin.SuperAdmin  import superAdmins
from ..admin.Subscribers import subscribers
from ..admin.PrivateRace import privateRacePeople

# helpers organized into seperate files
from Config    import values as Conf
from Menus     import *
from dbManager import *

import RaceTools
import Effects

import re
from operator import itemgetter

class Helper( object ):
	# boolean for whether or not players can use ultimates
	ultimatesAvailable = False

	def __init__( self, BASENAME, RACEPATH, ITEMPATH ):
		# for wcs_reload all
		reload( RaceTools )
		reload( Effects   )
		# reload( Config    )
		# reload( Menus     )
		# reload( dbManager )

		# save the paths for reloading
		self.BASENAME = BASENAME
		self.RACEPATH = RACEPATH
		self.ITEMPATH = ITEMPATH

		# instansiate more helpers
		self.RaceTools = RaceTools.RaceTools( self )
		self.Effects   = Effects.Effects( self )
		self.db        = DatabaseManager( self )
		self.xpManager = xpManager()
		self.xpRates   = self.xpManager.xpRates

		# initialize menus/races/items
		self.races = Races( self )
		self.items = Items( self )
		self.menus = Menus( self.races, self.items, self )

		# colors object, and make some methods quicker to access
		self.colors   = ColorMessages()
		self.tell     = self.colors.tell
		self.raceTell = self.colors.raceTell

		# initialize the callback command
		self.serverCommands = serverCommands( self )
		self.runCMD         = self.serverCommands.runCMD

		# initialize the filter dictionary
		self.filters = Filters().filters

		self.lastgive = es.ServerVar('eventscripts_lastgive')

	# reload method
	def reload( self ):
		reload( RaceTools )
		reload( Effects   )
		# reload( Config    )
		# reload( Menus     )
		# reload( dbManager )

		# reload the items, and races
		self.races.reload()
		self.items.reload()

	# list of the wcsPlayer Objects
	players = {}
	# get the player object from the players list based on id
	def getPlayer( self, userid ):
		if ( str(userid) in self.players ):
			return self.players[ str(userid) ]
		else:
			return None

	# get all players matching a filter.
	def getPlayerList( self, filterName=None ):
		# grab a list of all the player objects
		playerList = [ self.players[p] for p in self.players ]

		if ( filterName != None ):
			# remove the spaces if there are any
			filterName = filterName.replace( ' ', '' )

			# loop through all the filters
			for f in filterName.split( ',' ):

				# make sure the filter starts propperly
				if ( not f.startswith(('#', '!')) ):

					# raise an error if it doesn't
					raise KeyError, filterName + ' is not a valid wcsPlayer filter!'

				else:
					# Run through the filter
					if ( f.startswith('#') ):
						playerList = filter( self.filters[ f[1:] ], playerList )

					# Run it through the filter, excluding
					else:
						playerList = filter( lambda x: not self.filters[ f[1:] ](x), playerList )

		# return the list
		return playerList

	# trigger the event on races through the event name
	def TriggerStandardEvent( self, event, userid, event_var ):
		wcsPlayer = self.players[ str(userid) ]

		# if the player has a race set
		if ( wcsPlayer.race ):
			# get the race object
			race = self.races.raceList[ wcsPlayer.race ]

			# map the skill points to the skill names in the race!
			skills = dict( ( race.SkillList[ i ].Name, wcsPlayer.skillPoints[ i ] ) for i in range( len( race.SkillList ) ) )

			# call the standard function for that race.
			return getattr( race, event )( event_var, skills )

	# trigger the event on items through the event name
	def TriggerItemEvent( self, event, userid, event_var, purchasedItem=None ):
		wcsPlayer = self.players[ str(userid) ]

		# did we just purchase the item?
		if ( event == 'item_purchase' ):
			category = self.menus.shopMenu.getItemCategory( purchasedItem )
			getattr( self.items.itemList[category][purchasedItem], event )( event_var )
		else:
			if ( len( wcsPlayer.items ) > 0 ):
				for item in wcsPlayer.items:
					category = self.menus.shopMenu.getItemCategory( item )
					# if its an attack or hurt event, return, so that the damage will be modified
					if ( event == 'player_hurt' or event == 'player_attack' ):
						return getattr( self.items.itemList[category][item], event )( event_var )
					# otherwise, trigger the event as normal
					else:
						getattr( self.items.itemList[category][item], event )( event_var )

	# send the XP message to the player for killing someone
	def killXPMessage( self, attacker, victim, baseXP, levelXP, headshotXP, knifeXP ):
		# keep the data consistant
		wcsAttacker = self.players[ str(attacker) ]
		wcsVictim   = self.players[ str(victim)   ]

		xpTotal = baseXP + levelXP + headshotXP + knifeXP
		message = '#wcs[WCS] #defYou gain #xp%i XP#def' % xpTotal

		# add to the message if tehre was a headshot
		if ( headshotXP > 0 ):
			message += ' ( #xp%i #def+ #xp%i #def[Headshot] )' % ( baseXP, headshotXP )

		# add to the message if it was a knife kill
		if ( knifeXP > 0 ):
			message += ' ( #xp%i #def+ #xp%i #def[Knife] )' % ( baseXP, knifeXP )

		message += ' for killing #name%s#def' % wcsVictim.player.name

		# add to the message if there was level bonus XP
		if ( levelXP > 0 ):
			message += ', and #xp%i #defbonus xp for killing a higher level!' % levelXP
		else:
			message += '!'

		# send off the message!
		self.tell( wcsAttacker, message )

	# is the player a SuperAdmin? - gets both private, and sub
	def isplayerSuperAdmin( self, userid ):
		wcsPlayer = self.players[ str(userid) ]
		if ( wcsPlayer.player.steamid in superAdmins ):
			return True
		return False
	
	# does the player have access to private races?
	def isplayerPrivateRace( self, userid ):
		wcsPlayer = self.players[ str(userid) ]
		if ( wcsPlayer.player.steamid in privateRacePeople ):
			return True
		return False
	
	# does the player have access to subscriber races?
	def isplayerSubscriber( self, userid ):
		wcsPlayer = self.players[ str(userid) ]
		if ( wcsPlayer.player.steamid in subscribers ):
			return True
		return False

class xpManager( object ):

	# custom dictionary class for the xp rates
	class xpRateDict( dict ):

		# overide the getter
		def __getitem__( self, key ):

			# if you try to get an xp value higher than the max value
			if ( int(key) > len(self)-1 ): # shift len down one because we start at index 0

				# return the max value
				return dict.__getitem__( self, str(len(self)-1) )

			# otherwise, return the value as normal
			return dict.__getitem__( self, key )

	# when the object is constructed, 
	def __init__( self ):

		# custom dictionary for the xp required at each level
		self.xpRates = self.xpRateDict()

		# loop through the number of levels before the xp repeats
		for i in range( Conf.levelCapRepeat ):

			# setup the rate
			self.xpRates[ str(i) ] = Conf.StartingXP + ( Conf.ExtraPerLevel * i )

class Filters( object ):
	# dictionary to hold filters 'name':function
	filters = {}
	def __init__( self ):
		self.filters['all'  ] = self.filterAll   # All players
		self.filters['alive'] = self.filterAlive # Players Alive
		self.filters['dead' ] = self.filterDead  # Players Dead
		self.filters['human'] = self.filterHuman # Human
		self.filters['bot'  ] = self.filterBot   # Bots
		self.filters['un'   ] = self.filterTeam0 # Undecide
		self.filters['spec' ] = self.filterTeam1 # Spectator
		self.filters['t'    ] = self.filterTeam2 # Terrorist
		self.filters['ct'   ] = self.filterTeam3 # Counter-terrorist

	# modified from playerlib
	def filterAll( self, wcsPlayer ):
		""" Returns True. """
		return True

	def filterTeam0( self, wcsPlayer ):
		""" Returns True if the userid parameter is on team 0 otherwise returns False. """
		return wcsPlayer.player.getAttribute('teamid') == 0

	def filterTeam1( self, wcsPlayer ):
		""" Returns True if the userid parameter is on team 1 otherwise returns False. """
		return wcsPlayer.player.getAttribute('teamid') == 1

	def filterTeam2( self, wcsPlayer ):
		""" Returns True if the userid parameter is on team 2 otherwise returns False. """
		return wcsPlayer.player.getAttribute('teamid') == 2

	def filterTeam3( self, wcsPlayer ):
		""" Returns True if the userid parameter is on team 3 otherwise returns False. """
		return wcsPlayer.player.getAttribute('teamid') == 3

	def filterAlive( self, wcsPlayer ):
		""" Returns True if the userid parameter is alive otherwise returns False. """
		return bool(not wcsPlayer.player.getAttribute('isdead'))

	def filterDead( self, wcsPlayer ):
		""" Returns True if the userid parameter is dead otherwise returns False. """
		return bool(wcsPlayer.player.getAttribute('isdead'))

	def filterHuman( self, wcsPlayer ):
		""" Returns True if the userid parameter is a human otherwise returns False. """
		return bool(not wcsPlayer.player.getAttribute('isbot') and not wcsPlayer.player.getAttribute('ishltv'))

	def filterBot( self, wcsPlayer ):
		""" Returns True if the userid parameter is a bot otherwise returns False. """
		return bool(wcsPlayer.player.getAttribute('isbot'))

class serverCommands( object ):
	def __init__( self, helper ):
		self.helper = helper

	def runCMD( self, userid, commandString, callbackFunction, commandName, *args, **kwargs ):
		wcsPlayer = self.helper.players[ str(userid) ]

		if ( wcsPlayer ):
			setattr( wcsPlayer, 'info%i%s' % ( wcsPlayer, commandName ), callbackFunction )

			extraArgs = ' '.join( [ str(arg) for arg in args ] )

			if ( commandString ):
				es.server.queuecmd( commandString )

			# when calling this command, you can pass a keyword argument named delay, to have a delayed command
			if ( 'delay' in kwargs ):
				es.server.queuecmd( 'es_delayed %s wcs_callback %i %s %s' % ( kwargs['delay'], wcsPlayer, commandName, extraArgs ) )
			else:
				es.server.queuecmd( 'wcs_callback %i %s %s' % ( wcsPlayer, commandName, extraArgs ) )
		else:
			es.msg( 'No valid wcsPlayer for the command %s' % commandName )

	def wcsCallback( self, args ):
		commandName = args[1]

		if ( str(args[0]) in self.helper.players ):
			wcsPlayer = self.helper.players[ str(args[0]) ]

			callbackFunction = getattr( wcsPlayer, 'info%i%s' % ( wcsPlayer, commandName ) )

			callbackFunction( *args ) # userid, commandName, arg1, arg2, arg3
		else:
			es.msg( 'No valid wcsPlayer for the command %s' % commandName )

class ColorMessages( object ):

	def __init__( self ):
		self.colors = dict( self.findColors() )

	# loop through the text file for colors
	def findColors( self ):
		# open the color file as f
		f = open( 'cstrike/cfg/wcs/chat_colors.txt' )

		# pull all the colors defs out into readable characters
		for ( color, r, g, b ) in re.findall( r'(\S+)\s*=\s*(\d+),\s*(\d+),\s*(\d+)', f.read() ):
			# es.msg( ( color, r, g, b ) )
			# yield the color name, and hex string for the dictionary
			yield ( color, '\x07%02X%02X%02X' % ( int(r), int(g), int(b) ) )

	# yeh, thanks Super Dave. It hurts my brain to look at
	def replaceColorNames( self, text ):
		return reduce( lambda t, r: t.replace(*r), self.colors.iteritems(), text )

	def tell( self, userid, message ):
		# weird bug needing at least 1 space in the string?
		usermsg.saytext2( int(userid), 0, self.replaceColorNames( message + ' ' ) )

	def raceTell( self, race, userid, message ):
		# format the string coming from the race
		self.tell( int(userid), '%s[%s] #def%s' % ( race.RaceColor, race.RaceAbbreviation, message ) )

class Races( object ):
	raceList                = {}
	raceListNoPrivate       = {}
	raceListSorted          = []
	raceListNoPrivateSorted = []

	def __init__( self, helper ):
		self.helper = helper

		self.load()

	def reload( self ):
		self.raceList                = {}
		self.raceListNoPrivate       = {}
		self.raceListSorted          = []
		self.raceListNoPrivateSorted = []

		self.load()

	def load( self ):
		# load the modules
		raceModules = self.loadRaceModules()

		for race in raceModules:
			# create an instance of the raceclass
			raceObject = getattr( race[1], race[0] )()

			# give the race access to different modules
			raceObject.helper    = self.helper
			raceObject.Effects   = self.helper.Effects
			raceObject.RaceTools = self.helper.RaceTools

			# append to the racelist
			self.raceList[ raceObject.RaceName ] = raceObject

			# seperate list to have sorted
			self.raceListSorted.append( ( raceObject.RaceName, raceObject.RequiredLevel, raceObject.ChangeRaceIndex ) )

			# seperate list without private races
			if ( raceObject.isPrivate == False ):
				self.raceListNoPrivate[ raceObject.RaceName ] = raceObject
				self.raceListNoPrivateSorted.append( ( raceObject.RaceName, raceObject.RequiredLevel, raceObject.ChangeRaceIndex ) )

			# add race to DB
			self.helper.db.AddRace( raceObject.RaceName )

		# sort the sorted lists
		self.raceListSorted         .sort( key=itemgetter( 1, 2, 0 ) )
		self.raceListNoPrivateSorted.sort( key=itemgetter( 1, 2, 0 ) )

	def loadRaceModules( self ):
		for raceFile in self.helper.RACEPATH.walkfiles('*.py'):
			raceName = raceFile.namebase
			if ( raceName != '__init__' and raceName != 'exclude' ):
				# yield the name and imported module - Thanks SuperDave!
				yield raceName, reload(__import__( self.helper.BASENAME + '.races.' + raceName, fromlist=['races', raceName] ))

	# Return the number of total skill points there are in a race
	def getRaceNumSkillPoints( self, race ):
		skills = 0
		for skill in race.SkillList:
			skills += skill.Levels
		return skills

class Items( object ):
	itemList = {}
	def __init__( self, helper ):
		self.helper = helper

		self.load()

	def reload( self ):
		self.itemList = {}
		self.load()

	def load( self ):
		# load the modules
		itemModules = self.loadItemModules()

		# loop through categories
		for category in itemModules:
			categoryItems = {}

			for item in category[1]:
				itemObject = getattr( category[1][item], item )()

				# give access to different modules
				itemObject.helper    = self.helper
				itemObject.Effects   = self.helper.Effects
				itemObject.RaceTools = self.helper.RaceTools

				categoryItems[ itemObject.Name ] = itemObject

			self.itemList[ category[0] ] = categoryItems

	def loadItemModules( self ):
		for directory in self.helper.ITEMPATH.walkdirs():
			dirName  = directory.namebase
			dirItems = {}
			for itemFile in directory.walkfiles('*.py'):
				itemName = itemFile.namebase
				if ( itemName != '__init__' ):
					dirItems[ itemName ] = reload(__import__( self.helper.BASENAME + '.items.' + dirName + '.' + itemName, fromlist=['items', dirName, itemName] ))
			yield dirName, dirItems
