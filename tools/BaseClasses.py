import es
import playerlib

import time

# from DatabaseManager import db

class Skill( object ):
	def __init__( self, name, description, levels, requiredlevel, old=None, old1=None ):
		self.Name          = name
		self.Description   = description
		self.Levels        = levels
		self.RequiredLevel = requiredlevel

class baseRace( object ):
	# helper Object
	helper             = 0

	# race tools object
	RaceTools          = 0

	# restrictions
	WeaponsCanOnlyUse  = []
	WeaponsCantUse     = []
	ItemsCantUse       = []

	# race information
	RaceTypes          = []
	RaceName           = 'Base Race'
	Coder              = 'MiniDude'
	isSubscriber       = False
	isPrivate          = False

	RaceColor          = '#race'

	RaceAbbreviation   = 'Race'

	# for knife / pisto races
	RacePrefix         = ''

	# race limitations
	PlayerLimit        = False
	LimitTeamDependant = True
	RequiredLevel      = 0

	# cooldowns
	UltimateCooldown   = 20
	AbilityCooldown    = 0

	# if you want an alternate round start cooldown
	StartingUltimateCooldown = None
	StartingAbilityCooldown  = None

	UltimateTriggered = {}
	AbilityTriggered  = {}

	# menu positioning
	ChangeRaceIndex   = 100

	@property
	def CompiledName( self ):
		if ( self.RacePrefix != '' ):
			return self.RaceColor + self.RacePrefix + ' ' + self.RaceName
		else:
			return self.RaceColor + self.RaceName

	# if you try and turn the race object into a string, just retun the race name
	def __str__( self ):
		return self.RaceName

	def player_connect( self, ev, skills ):
		pass

	def spawn_messages( self, ev, skills ):
		pass

	def adjust_cooldowns( self, ev, skills ):
		pass

	def player_spawn( self, ev, skills ):
		pass

	def player_death( self, ev, skills ):
		pass

	def player_kill( self, ev, skills ):
		pass

	def player_hurt( self, ev, skills ):
		pass

	def player_attack( self, ev, skills ):
		pass

	def player_jump( self, ev, skills ):
		pass

	def player_ability( self, ev, skills ):
		pass

	def player_ability_off( self, ev, skills ):
		pass

	def player_ultimate( self, ev, skills ):
		pass

	def player_ultimate_off( self, ev, skills ):
		pass

	def pre_race_changed( self, ev, skills ):
		pass

	def race_changed( self, ev, skills ):
		pass

	def round_start( self, ev, skills ):
		pass

	def round_freeze_end( self, ev, skills ):
		pass

	def round_end( self, ev, skills ):
		pass

	def Es_map_start( self, ev, skills ):
		pass

	def weapon_fire( self, ev, skills ):
		pass

	def bullet_impact( self, ev, skills ):
		pass

	def player_air( self, ev, skills ):
		pass

	def player_land( self, ev, skills ):
		pass

	def client_keypress( self, ev, skills ):
		pass

class baseItem( object ):
	Name          = 'Base Item'
	Description   = 'Base Item Description'
	Price         = 1000
	Requiredlevel = 0
	Persistent    = 0

	def player_spawn( self, ev ):
		pass

	def player_death( self, ev ):
		pass

	def player_kill( self, ev ):
		pass

	def player_hurt( self, ev ):
		pass

	def player_attack( self, ev ):
		pass

	def player_jump( self, ev ):
		pass

	def round_start( self, ev ):
		pass

	def round_freeze_end( self, ev ):
		pass

	def round_end( self, ev ):
		pass

	def Es_map_start( self, ev ):
		pass

	def weapon_fire( self, ev ):
		pass

	def bullet_impact( self, ev ):
		pass

	def player_air( self, ev ):
		pass

	def player_land( self, ev ):
		pass

	def client_keypress( self, ev ):
		pass

	def item_purchase( self, event_var ):
		pass

class basePlayer( object ):
	'''
	Testable
	'''
	ultimateImmune = False
	abilityImmune  = False
	rooted         = False

	'''
	Items
	'''
	items = []

	'''
	Playerinfo Information
	'''
	starthealth = 100
	invis       = '100%'
	movespeed   = '100%'
	gravity     = '100%'

	'''
	Cooldowns
	'''
	ultimateCD  = 0
	abilityCD   = 0

	ultimateOn  = False
	abilityOn   = False

	timerInitialized = False

	'''
	Conversions for returning the userid
	'''
	def __str__( self ):
		return str(self.player.userid)

	def __int__( self ):
		return self.player.userid

	'''
	Initialize the player
	'''
	def __init__( self, userid, helper ):
		self.helper = helper
		self.player = playerlib.getPlayer( userid )
		self.refresh()

		# when itialized make sure there are no items
		self.items = []

	'''
	Temporary Attributes
	'''
	def __setattr__( self, name, value ):
		# is it a property that is aleady a part of the object?
		if hasattr( basePlayer, name ):
			object.__setattr__( self, name, value )

		# if the first 4 characters of the value you're setting are race/menu/info, we'll let you set the value
		elif ( 'info' in name[:4].lower() ):

			# set with the __dict__ so we don't recurse
			# prepend tmp so when the map changes, we can clean out all the tmp values
			self.__dict__['tmp'+name] = value

		# if its not a tmp value, then just set the value
		else:
			self.__dict__[name] = value

	def __getattr__( self, name ):
		# if ( name.lower() in [ 'deaths', 'isobserver', 'serialnumber', 'steamid', 'index', 'isinavehicle', 'armor', 'packetloss', 'ping', 'teamid', 'ishltv', 'isbot', 'health', 'timeconnected', 'handle', 'kills', 'isdead', 'address', 'name', 'language', 'weapon', 'y', 'x', 'z', 'model' ] ):
		# 	information = es.createplayerlist(self.player.userid)[int(self.player.userid)]
		# 	return( information[name] )

		# if the object has the attribute by default, just get it
		if hasattr( basePlayer, name ):
			return getattr( self, name )

		else:
			# try to get a normal value from the dict
			try:
				return self.__dict__[name]
			except KeyError, e:

				# try to get the temp value from the dict
				try:
					return self.__dict__['tmp'+name]
				except KeyError, e1:
					raise AttributeError, e

					# # try to get the attribute from the playerlib
					# try:
					# 	return getattr( self.player, name )
					# except KeyError, e2:
					# 	raise AttributeError, e

	def cleanTempValues( self ):
		# get all the key names from the __dict__ - Important because you shouldn't loop
		#   through the same list you're deleting stuff from
		d = [ name for name in self.__dict__ ]

		# loop through the key names
		for name in d:

			# if its a temporary value
			if ( name[:3].lower() == 'tmp' ):

				# remove it
				del self.__dict__[name]

	'''
	Properties
	'''
	# Property to update the player's levels when its set
	def getRoundXP( self ):
		return self.raceXP

	def setRoundXP( self, value ):
		self.raceXP = value

		save = False

		# while the xp would level us up
		while( self.raceXP >= self.helper.xpRates[str(self.level)] ):

			# set the racexp for the save
			self.raceXP -= self.helper.xpRates[str(self.level)]

			# increment the leve
			self.level += 1

			# boolean to save
			save = True

		# save
		if ( save ):
			self.save()

	roundXP = property( getRoundXP, setRoundXP )

	# property to modify speed
	speedModifier = 1
	def getSpeedModifier( self ):
		return self.speedModifier

	def setSpeedModifier( self, value ):
		self.speedModifier = value

		# es.tell( self.player, '#green', self.speedModifier )

		self.player.speed = 1 * float( value )

		# es.tell( self.player, '#green', self.player.speed )

	speed = property( getSpeedModifier, setSpeedModifier )

	# property to modify alpha
	alphaModifier = 1
	def getAlphaModifier( self ):
		return self.alphaModifier

	def setAlphaModifier( self, value ):
		self.alphaModifier = value
		self.updatePlayerColor()

	alpha = property( getAlphaModifier, setAlphaModifier )

	# property to modify red
	redModifier = 1
	def getRedModifier( self ):
		return self.redModifier

	def setRedModifier( self, value ):
		self.redModifier = value
		self.updatePlayerColor()

	red = property( getRedModifier, setRedModifier )

	# property to modify green
	greenModifier = 1
	def getGreenModifier( self ):
		return self.greenModifier

	def setGreenModifier( self, value ):
		self.greenModifier = value
		self.updatePlayerColor()

	green = property( getGreenModifier, setGreenModifier )

	# property to modify blue
	blueModifier = 1
	def getBlueModifier( self ):
		return self.blueModifier

	def setBlueModifier( self, value ):
		self.blueModifier = value
		self.updatePlayerColor()

	blue = property( getBlueModifier, setBlueModifier )

	'''
	Utilty
	'''
	weaponInvis = True
	# set player color, and weapon color
	def updatePlayerColor( self ):
		self.player.setColor( int(255*float(self.red)), int(255*float(self.green)), int(255*float(self.blue)), int(255*float(self.alpha)) )
		if ( self.weaponInvis ):
			try:
				self.player.setWeaponColor( int(255*float(self.red)), int(255*float(self.green)), int(255*float(self.blue)), int(255*float(self.alpha)) )
			except:
				pass
	'''
	Timers
	'''
	def setupTimers( self ):
		if ( self.timerInitialized == False ):
			self.timerInitialized = True

			# grab the time
			t = time.time()

			# grab the race object
			race = self.helper.races.raceList[ self.race ]

			# does the race have an alternate starting cooldown?
			if ( race.StartingUltimateCooldown != None ):
				# yeah? save it as such
				cd = race.UltimateCooldown - race.StartingUltimateCooldown
			else:
				# it doesnt? just use the normal cooldown then
				cd = race.UltimateCooldown

			self.ultimateTimer = t - cd

			self.ultimateCD = race.UltimateCooldown

			# same thing for abilities
			if ( race.StartingAbilityCooldown != None ):
				cd = race.AbilityCooldown - race.StartingAbilityCooldown
			else:
				cd = race.AbilityCooldown
			self.abilityTimer = t - cd

			self.abilityCD = race.AbilityCooldown

			self.helper.TriggerStandardEvent( 'adjust_cooldowns', self.player, { 'userid':self.player.userid, 'wcsPlayer':self } )

	def resetTimer( self, timer='ultimate' ):
		t = time.time()

		# reset ultimate timer
		if ( 'ult'  in timer.lower() ): self.ultimateTimer = t

		# reset ability timer
		if ( 'abil' in timer.lower() ): self.abilityTimer  = t

	'''
	Database Managment
	'''
	skillPoints = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )
	def refresh( self ):
		# refresh our player object
		# self.player = playerlib.getPlayer( self.player.userid )

		if ( self.player.steamid != 'BOT' ):
			# load the information out of the database
			dbInformation    = self.helper.db.GetPlayerInformation( self.player.steamid )

			# sort the loaded information
			self.playerID    = dbInformation['player_id'   ]
			self.raceID      = dbInformation['race_id'     ]
			self.race        = dbInformation['race_name'   ]
			self.raceXP      = dbInformation['xp'          ]
			self.level       = dbInformation['level'       ]
			self.skillPoints = dbInformation['skill_points']
			self.totalLevel  = dbInformation['total_level' ]

	def save( self, refresh=True ):
		# save the xp, level, and skill point changes
		self.helper.db.UpdateRaceXP( self.playerID, self.raceID, self.raceXP, self.level, self.skillPoints )

		if ( refresh ):
			self.refresh()

	def resetPlayer( self ):
		# self.helper.RaceTools.setColor( self.player, 1, 1, 1, 1 )
		self.player.speed = 1

		es.entitysetvalue( self.player.index, 'gravity', 1 )
		es.server.queuecmd( 'sm_resize #%s 1 500' % self.player.userid )
		self.starthealth = 100
		self.invis       = '100%'
		self.movespeed   = '100%'
		self.gravity     = '100%'

		self.resetWeapons()

	'''
	Weapon Modifications - Rate of Fire - Recoil
	'''
	weapons = {
		'weapon_knife'       : { 'rof': None, 'recoil': None },
		'weapon_awp'         : { 'rof': None, 'recoil': None },
		'weapon_scout'       : { 'rof': None, 'recoil': None },
		'weapon_sg550'       : { 'rof': None, 'recoil': None },
		'weapon_g3sg1'       : { 'rof': None, 'recoil': None },
		'weapon_m4a1'        : { 'rof': None, 'recoil': None },
		'weapon_ak47'        : { 'rof': None, 'recoil': None },
		'weapon_sg552'       : { 'rof': None, 'recoil': None },
		'weapon_aug'         : { 'rof': None, 'recoil': None },
		'weapon_famas'       : { 'rof': None, 'recoil': None },
		'weapon_galil'       : { 'rof': None, 'recoil': None },
		'weapon_m249'        : { 'rof': None, 'recoil': None },
		'weapon_mp5navy'     : { 'rof': None, 'recoil': None },
		'weapon_tmp'         : { 'rof': None, 'recoil': None },
		'weapon_ump45'       : { 'rof': None, 'recoil': None },
		'weapon_p90'         : { 'rof': None, 'recoil': None },
		'weapon_mac10'       : { 'rof': None, 'recoil': None },
		'weapon_xm1014'      : { 'rof': None, 'recoil': None },
		'weapon_m3'          : { 'rof': None, 'recoil': None },
		'weapon_usp'         : { 'rof': None, 'recoil': None },
		'weapon_glock'       : { 'rof': None, 'recoil': None },
		'weapon_p228'        : { 'rof': None, 'recoil': None },
		'weapon_deagle'      : { 'rof': None, 'recoil': None },
		'weapon_fiveseven'   : { 'rof': None, 'recoil': None },
		'weapon_elite'       : { 'rof': None, 'recoil': None },
		'weapon_hegrenade'   : { 'rof': None, 'recoil': None }, # don't know if works?
		'weapon_flashbang'   : { 'rof': None, 'recoil': None }, # don't know if works?
		'weapon_smokegrenade': { 'rof': None, 'recoil': None }  # don't know if works?
	}

	def setWeaponRateOfFire( self, weaponName, rate ):
		# preppend the weapon_ if its not in the name already
		if ( not 'weapon_' in weaponName ): weaponName = 'weapon_' + weaponName
		
		# make sure the weapon name is in the dictionary
		try:
			self.weapons[weaponName]['rof'] = rate
		except KeyError, e:
			raise AttributeError, e

	def getWeaponRateOfFire( self, weaponName ):
		# preppend the weapon_ if its not in the name already
		if ( not 'weapon_' in weaponName ): weaponName = 'weapon_' + weaponName

		return self.weapons[weaponName]['rof']

	def setWeaponRecoil( self, weaponName, recoil ):
		# preppend the weapon_ if its not in the name already
		if ( not 'weapon_' in weaponName ): weaponName = 'weapon_' + weaponName
		
		# make sure the weapon name is in the dictionary
		try:
			self.weapons[weaponName]['recoil'] = recoil
		except KeyError, e:
			raise AttributeError, e

	def getWeaponRecoil( self, weaponName ):
		# preppend the weapon_ if its not in the name already
		if ( not 'weapon_' in weaponName ): weaponName = 'weapon_' + weaponName

		return self.weapons[weaponName]['recoil']

	def resetWeapons( self ):
		# reset the weapon properties
		for weapon in self.weapons:
			self.weapons[weapon]['rof']    = None
			self.weapons[weapon]['recoil'] = None
