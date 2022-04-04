import es
# import playerlib - booya
import weaponlib
import gamethread
import usermsg
import vecmath
import spe
import spe_effects

import math

from random import randint

import DamageTypes

class RaceTools( object ):

	# boolean for whether or not the round has ended
	duringRound = False

	# the RoundOver property
	def getRoundOver( self ):
		return self.duringRound

	def setRoundOver( self, value ):
		# when you set the value to false,
		if ( value == False ):

			'''
			Reset Auras
			'''
			# loop through all the auras
			for aura in self.auraList:

				# cancel them!
				gamethread.cancelDelayed( aura )

			# clean out the aura list
			self.auraList = {}

			'''
			Reset raceDelays
			'''
			for raceDelay in self.raceDelays:
				gamethread.cancelDelayed( raceDelay )

			self.raceDelays = []

			'''
			Reset DOT list
			'''
			# clean out the DOT list
			self.DOTList = {}

		# set the value to what you were trying to set it to
		self.duringRound = value

	roundOver = property( getRoundOver, setRoundOver )

	# list of players recieving Damage over Time
	DOTList = {}

	def __init__( self, helper ):
		self.helper = helper

	'''
	Commands for getting players
	'''
	# filters - #alive, #all, #bot, #ct, #dead, #human, #spec, #t, #un
	#         - can be combined with commas eg: '#t, #alive'
	#         - returns a wcsPlayer list
	def getPlayersInRangePlayer( self, userid, playerFilter, radius ):
		# player object
		wcsPlayer = self.helper.players[ str(userid) ]

		# players' position
		x,y,z = wcsPlayer.player.getLocation()

		# empty list
		targets = []

		# loop through all the players that match our filter
		for wcsTarget in self.helper.getPlayerList( playerFilter ):
			# get the targets location
			x1,y1,z1  = wcsTarget.player.getLocation()

			# distance formulat eh bebe
			distance  = math.sqrt( ( x - x1 )**2 + ( y - y1 )**2 + ( z - z1 )**2 )

			# is the distance within the radius?
			if ( radius >= int(distance) ):

				# add the player to the list
				targets.append( wcsTarget )

		# return the list
		return targets

	# get the players in distance of x,y,z
	def getPlayersInRangePoint( self, x, y, z, playerFilter, radius ):
		# cast to floats
		x = float(x)
		y = float(y)
		z = float(z)

		# list for returing
		targets = []

		# loop through them
		for wcsTarget in self.helper.getPlayerList( playerFilter ):

			# get the targets coordinates
			x1,y1,z1  = wcsTarget.player.getLocation()

			# distance forumale eh bebe
			distance  = math.sqrt( ( x - x1 )**2 + ( y - y1 )**2 + ( z - z1 )**2 )

			# is the distance within the radus?
			if ( radius >= int(distance) ):

				# add the player to the list
				targets.append( wcsTarget )

		# return the list
		return targets

	'''
	Pushing the player
	'''
	def pushToViewCoords( self, userid, force ):
		# grab player
		wcsPlayer = self.helper.players[ str(userid) ]

		# spawn a prop at the players view location
		command = 'es_xprop_dynamic_create %i props_c17/tv_monitor01_screen.mdl' % wcsPlayer

		# have to interupt the function
		self.helper.runCMD( wcsPlayer, command, self.pushToViewCoords1, 'RaceToolsViewCoords', force )

	# continuation as we have to call some server commands
	def pushToViewCoords1( self, userid, commandName, force ):
		wcsPlayer  = self.helper.players[ str(userid) ]

		# Get the last spawned prop's x, y, and z
		viewVec    = vecmath.Vector( es.getindexprop( self.helper.lastgive, 'CBaseEntity.m_vecOrigin' ).split(',') )

		es.server.queuecmd( 'es_xremove ' + self.helper.lastgive )

		# player location
		playerVec  = vecmath.Vector( es.getplayerlocation( wcsPlayer ) )

		# subtract them
		pushVec    = ( viewVec - playerVec )

		# typecast force to a float, as it comes in as a string
		force      = float( force )

		# apply force
		newVec     = pushVec.setlength( force )

		# get player current velocity
		x = es.getplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_vecVelocity[0]' )
		y = es.getplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_vecVelocity[1]' )
		z = es.getplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_vecVelocity[2]' )

		# remove the players current velocity
		newVec[0] -= x
		newVec[1] -= y
		newVec[2] -= z 
		newVec[2] += 200

		# apply force to player
		es.setplayerprop( wcsPlayer, "CBasePlayer.localdata.m_vecBaseVelocity", str( newVec ) )

	def pushToPoint( self, userid, x, y, z ):
		# get player object
		wcsPlayer = self.helper.players[ str(userid) ]

		# apply force
		es.setplayerprop( wcsPlayer, "CBasePlayer.localdata.m_vecBaseVelocity", ','.join( [str(x), str(y), str(z)] ) )

	def longJump( self, userid, multiplier, speedCap=900, multiplyCap=700 ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# get velocity
		x = es.getplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_vecVelocity[0]' )
		y = es.getplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_vecVelocity[1]' )

		# apply the cap
		# es.msg( (speedCap, math.fabs(x), math.fabs(y)) )
		if  (
				math.fabs(x) <= speedCap and
				math.fabs(y) <= speedCap
			):
			# increase velocity
			x *= multiplier
			y *= multiplier

			# apply the secondary cap
			x = max( -multiplyCap, min( x, multiplyCap ) )
			y = max( -multiplyCap, min( y, multiplyCap ) )

			# apply the combined cap
			if (
					math.fabs(x) <= ( speedCap + multiplyCap ) and
					math.fabs(y) <= ( speedCap + multiplyCap )
				):
				# apply the velocity
				self.pushToPoint( wcsPlayer, x, y, 0 )

	'''
	Aura functions
	'''
	# list of the auras running
	auraList = {}
	def Aura( self, userid, rate, callbackFunction, name='basic', extraParamaters=() ):
		# load the player
		wcsPlayer = self.helper.players[ str(userid) ]

		# create the unique aura name
		name = 'aura_loop_%s_%s' % ( wcsPlayer, name )

		# set the boolean for the arua to be on
		self.auraList[ name ] = True

		# cancel the aura if its already going
		gamethread.cancelDelayed( name )

		# start the Aura
		self.AuraLoop( wcsPlayer, rate, callbackFunction, name, extraParamaters )

	def AuraLoop( self, wcsPlayer, rate, callbackFunction, delayName, extraParamaters=False ):
		# is this loop supposed to keep going?
		if ( not self.roundOver and self.auraList[ delayName ] ):

			# call the function, if we have extra params, pass them
			if ( extraParamaters ): callbackFunction( wcsPlayer, extraParamaters )
			else:                   callbackFunction( wcsPlayer )

			# call this function again, at the specified rate.
			gamethread.delayedName( rate, delayName, self.AuraLoop, ( wcsPlayer, rate, callbackFunction, delayName, extraParamaters ) )

	def stopAura( self, userid, name='basic' ):
		# load the player
		wcsPlayer = self.helper.players[ str(userid) ]

		# create the unique aura name
		name = 'aura_loop_%s_%s' % ( wcsPlayer, name )

		# set it to false, to stop the aura
		self.auraList[ name ] = False

		# cancel the delayed callback
		gamethread.cancelDelayed( name )

	'''
	Aura Implementations
	'''
	# gravity is set on a loop, because touching a ladder, resets your gravity
	def setGravity( self, userid, ratio ):
		# get the player
		wcsPlayer = self.helper.players[ str(userid) ]

		# set info for the playerinfo menu
		wcsPlayer.gravity = str(int( ratio * 100 )) + '%'

		# begin the aura
		self.Aura( wcsPlayer, 0.25, self.gravityCB, 'raceToolsGravity', float(ratio) )

	# gravity Callback function for the aura
	def gravityCB( self, wcsPlayer, ratio ):
		# set the gravity
		es.entitysetvalue( wcsPlayer.player.index, 'gravity', ratio )

	# Damage over Time
	def DOT( self, attacker, victim, time, damage, effect=None, interval=0.5 ):
		# setup the info
		wcsAttacker = self.helper.players[ str(attacker) ]
		wcsVictim   = self.helper.players[ str(victim)   ]

		time     = float(time)
		damage   = float(damage)

		# build the aura string
		auraName = 'RaceToolsDOT_%s_%s' % ( str(wcsVictim), str(wcsAttacker) )

		# make sure the attacker doesn't already have a DOT going on the victim
		if ( not auraName in self.DOTList or self.DOTList[auraName] == None ):
			# get the number of times to call the damage function, when the damage is dealt every 0.5 seconds
			iterations = time / interval

			# store the iterations for later
			self.DOTList[auraName] = iterations

			# get how much damage to deal every iteration
			dot = float( damage / iterations )

			# begin the aura
			self.Aura( wcsVictim, interval, self.DOTDamage, auraName, { 'auraName':auraName, 'effect':effect, 'attacker':str(wcsAttacker), 'victim':str(wcsVictim), 'damage':dot } )
			
			return True			
		
		return False			

	# Callback function
	def DOTDamage( self, userid, var ):
		# subtract one iteration from the list
		self.DOTList[ var['auraName'] ] -= 1

		# if there are no more iterations left
		if ( self.DOTList[ var['auraName'] ] <= 0 ):

			# stop the aura
			self.stopAura( var['victim'].userid, var['auraName'] )

			# reset the iterations, to be applied again
			self.DOTList[ var['auraName'] ] = None

		# deal the damage
		self.damage( var['attacker'], var['victim'], var['damage'] )

		# is there an effect!?!?
		if ( var['effect'] != None ):
			wcsPlayer = self.helper.players[ str(var['victim']) ]

			# make sure the victim is alive
			if ( not wcsPlayer.victim.isdead ):
				# call it!!
				var['effect']( var['attacker'], var['victim'] )

	'''
	Utility functions
	'''
	def damage( self, attacker, victim, damage, weapon=False ):
		wcsAttacker = self.helper.players[ str(attacker) ]
		wcsVictim   = self.helper.players[ str(victim)   ]

		if ( weapon ):
			es.server.queuecmd( 'damage %i %i %i %i #active' % ( wcsVictim, damage, DamageTypes.DMG_FALL, wcsAttacker ) )
		else:
			es.server.queuecmd( 'damage %i %i %i %i' % ( wcsVictim, damage, DamageTypes.DMG_FALL, wcsAttacker ) )

	def respawn( self, userid ):

		# make a call to the SouceMod helper command
		es.server.queuecmd( 'wcs_respawn #%i' % userid )

		# Works, but prefer the other method
		# es.setplayerprop( userid, "CCSPlayer.m_iPlayerState"       ,   0 )
		# es.setplayerprop( userid, "CCSPlayer.baseclass.m_lifeState", 512 )
		# es.spawnplayer( userid )

		# call to direct respawn function - Has problems on linux
		# spe.games.cstrike.respawn( player.userid )

	def setColor( self, userid, r, g, b, a, weapon=True ):
		# get player
		wcsPlayer = self.helper.players[ str(userid) ]

		# set info for the playerinfo menu
		wcsPlayer.invis = str(int(a*100)) + '%'

		wcsPlayer.redModifier   = r
		wcsPlayer.greenModifier = g
		wcsPlayer.blueModifier  = b
		wcsPlayer.alphaModifier = a

		if ( weapon == False ):
			wcsPlayer.weaponInvis = False

		wcsPlayer.updatePlayerColor()

	def setSpeed( self, userid, speed ):
		# get the player
		wcsPlayer = self.helper.players[ str(userid) ]

		# set info for the playerinfo menu
		wcsPlayer.movespeed = str(int( speed * 100 )) + '%'

		# set the actual speed for the player
		wcsPlayer.speed = speed

	def setHealth( self, userid, health ):
		# get the player
		wcsPlayer = self.helper.players[ str(userid) ]

		# set the player health
		wcsPlayer.player.health = health

		# set info for the playerinfo menu
		wcsPlayer.starthealth = health

	def freezePlayer( self, userid, duration ):
		# get the player
		wcsPlayer = self.helper.players[ str(userid) ]

		# create the delay name string
		delayName = 'raceToolsFreeze_' + str( wcsPlayer )

		# cancel the last delayed call
		gamethread.cancelDelayed( delayName )

		# if the player isn't a bot
		if ( wcsPlayer ):
			# set the rooted flag to prevent movement ults - zergling
			wcsPlayer.rooted = True

		# setup a new one
		gamethread.delayedName( duration, delayName, self.unfreezePlayer, ( wcsPlayer ) )

		# freeze the player
		wcsPlayer.player.freeze( True )

	# freezePlayer calls this after the duration
	def unfreezePlayer( self, wcsPlayer ):
		# unroot
		wcsPlayer.rooted = False

		# make sure the player isn't dead
		if ( not wcsPlayer.player.isdead ):

			# unfreeze the player
			wcsPlayer.player.freeze( False )

	# list of slowed players
	slowedPlayers = {}
	def slowPlayer( self, userid, speed, duration ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# if the player isn't in the list, put him in it
		if ( not str(wcsPlayer) in self.slowedPlayers ):
			self.slowedPlayers[str(wcsPlayer)] = False

		# if the player ISN'T already slowed
		if ( self.slowedPlayers[str(wcsPlayer)] == False ):
			# lets slow him
			self.slowedPlayers[str(wcsPlayer)] = True

			wcsPlayer.speed -= speed

			# set him up to be unslowed of course
			gamethread.delayed( duration, self.unslowPlayer, ( wcsPlayer, speed ) )

	# slowPlayer calls this after the duration
	def unslowPlayer( self, wcsPlayer, speed ):
		# set the players speed back to normal
		wcsPlayer.speed += speed
		self.slowedPlayers[str(wcsPlayer)] = False

	def fadeScreen( self, userid, duration, r, g, b, a ):
		usermsg.fade( int(userid), 1, duration*500, duration*500, r, g, b, a )

	def unRoot( self, userid ):
		wcsPlayer = self.helper.players[ str(userid) ]

		wcsPlayer.rooted = False

	cheatCounter = 0
	def cheatsOn( self ):
		# increment the counter
		self.cheatCounter += 1

		# if this is the first time turning on cheats, then lets actually turn em on
		if ( self.cheatCounter == 1 ):

			# turn on cheats quietly.
			es.server.queuecmd( 'es_xflags remove notify sv_cheats;sv_cheats 1;es_xflags add notify sv_cheats' )

	def cheatsOff( self ):
		# decrement the counter
		self.cheatCounter -= 1

		# if no commands need the cheats on anymore, then lets turn em off
		if ( self.cheatCounter == 0 ):

			# turn off cheats quietly
			es.server.queuecmd( 'es_xflags remove notify sv_cheats;sv_cheats 0;es_xflags add notify sv_cheats' )

	'''
	Race Delayed Functions
	'''
	# list of the raceDelays to be canceled when the round ends
	raceDelays = []

	# interface to the gamethread.delayedName function, that will cancel the deayed calls when the round ends
	def delayed( self, seconds, cmd, args=(), kw=None ):

		# build our unique delayName
		delayName = 'raceTools_delayed_%i' % len( self.raceDelays )

		# append it to our list, to be canceled when the round ends.
		self.raceDelays.append( delayName )

		# call the delayed thread just like you normally would
		gamethread.delayedName( seconds, delayName, cmd, args, kw )

	'''
	Weapon Functions
	'''
	weaponList = {
		'primary'  : ['weapon_m3','weapon_xm1014','weapon_mp5navy','weapon_tmp','weapon_p90','weapon_mac10','weapon_ump45','weapon_galil','weapon_famas','weapon_ak47','weapon_sg552','weapon_m4a1','weapon_aug','weapon_scout','weapon_awp','weapon_g3sg1','weapon_sg550','weapon_m249'],
		'secondary': ['weapon_usp','weapon_glock','weapon_deagle','weapon_elite','weapon_p228','weapon_fiveseven'],
		'grenade'  : ['weapon_flashbang','weapon_smokegrenade','weapon_hegrenade']
	}
	def giveWeapon( self, userid, weapon, ammount=1 ):
		gamethread.delayed( 0.5, self.giveWeapon2, (userid, weapon, ammount) )

	def giveWeapon2( self, userid, weapon, ammount=1 ):
		# append weapon_ if its not part of the weapon name.
		if ( not 'weapon_' in weapon ):
			weapon = 'weapon_' + weapon.lower()

		# make sure that we're not trying to give c4, or knife
		if ( weapon != 'weapon_c4' and weapon != 'weapon_knife' ):

			# load the player
			wcsPlayer = self.helper.players[ str(userid) ]

			# get a list of the players weapons
			weapons = wcsPlayer.player.getWeaponList()

			# we're not holding the weapon we're trying to give
			if ( not weapon in weapons ):

				# is the weapon we're trying to give a primary?
				if ( weapon in self.weaponList['primary'] ):
					# get the weapon we have out of the primary
					dropWeapon = [ w for w in weapons if w in self.weaponList['primary'] ]

					if ( len( dropWeapon ) == 1 ):
						dropWeapon = dropWeapon[0]
						es.server.queuecmd( 'es_xsexec %i use %s' % ( wcsPlayer, dropWeapon ) )
						es.server.queuecmd( 'es_xsexec %i drop'   % ( wcsPlayer             ) )

				elif ( weapon in self.weaponList['secondary'] ):
					dropWeapon = [ w for w in weapons if w in self.weaponList['secondary'] ]

					if ( len( dropWeapon ) == 1 ):
						dropWeapon = dropWeapon[0]
						es.server.queuecmd( 'es_xsexec %i use %s' % ( wcsPlayer, dropWeapon ) )
						es.server.queuecmd( 'es_xsexec %i drop'   % ( wcsPlayer             ) )

				elif ( weapon in self.weaponList['grenade'] ):
					dropWeapon = [ w for w in weapons if w in self.weaponList['grenade'] ]

					if ( len( dropWeapon ) == 1 ):
						dropWeapon = dropWeapon[0]
						es.server.queuecmd( 'es_xsexec %i use %s' % ( wcsPlayer, dropWeapon ) )
						es.server.queuecmd( 'es_xsexec %i drop'   % ( wcsPlayer             ) )

				# loop the number of times to give the weapon, eg: 2 flashbangs
				for i in range( ammount ):
					es.server.queuecmd( 'es_xgive %i %s' % ( wcsPlayer, weapon ) )

	def getActiveWeapon( self, userid ):
		return spe.games.cstrike.getActiveWeapon( int(userid) )

	def noRecoil( self, userid ):
		# get player
		wcsPlayer = self.helper.players[ str(userid) ]

		# get properties for no recoil
		es.setplayerprop( wcsPlayer, 'CCSPlayer.cslocaldata.m_iShotsFired', 0 )
		es.setplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_Local.m_vecPunchAngle', '0,0,0' )

	'''
	Helpers for setting the Clip on a weapon
	'''
	def setPrimaryClip( self, userid, ammount ):
		self.helper.runCMD( int(userid), '', self.setClip, 'RTsetPrimaryClip'  , 'primary'  , ammount, delay=2 )

	def setSecondaryClip( self, userid, ammount ):
		self.helper.runCMD( int(userid), '', self.setClip, 'RTsetSecondaryClip', 'secondary', ammount, delay=2 )

	def setClip( self, userid, commandName, weapon, ammount ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# get the propper weapon - this is what needs to be called AFTER the server give command
		if ( weapon == 'primary' ):
			weapon = wcsPlayer.player.getPrimary()
		elif ( weapon == 'secondary' ):
			weapon = wcsPlayer.player.getSecondary()

		wcsPlayer.player.setClip( weapon, ammount )

	'''
	Helpers for setting the Ammo on a weapon
	'''
	def setPrimaryAmmo( self, userid, ammount ):
		self.helper.runCMD( int(userid), '', self.setAmmo, 'RTsetPrimaryAmmo'  , 'primary'  , ammount, delay=2 )

	def setSecondaryAmmo( self, userid, ammount ):
		self.helper.runCMD( int(userid), '', self.setAmmo, 'RTsetSecondaryAmmo', 'secondary', ammount, delay=2 )

	def setAmmo( self, userid, commandName, weapon, ammount ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# get the propper weapon - this is what needs to be called AFTER the server give command
		if ( weapon == 'primary' ):
			weapon = wcsPlayer.player.getPrimary()
		elif ( weapon == 'secondary' ):
			weapon = wcsPlayer.player.getSecondary()

		wcsPlayer.player.setAmmo( weapon, ammount )

	# 1 seems to be the weapons standard rate... anything below 0 messes up sounds on client side
	# but the weapon is still firing that much faster.
	# needs to be called in the weapon_fire event
	def ModifyWeaponsRateOfFire( self, userid, weaponIndex, Rate ):
		# get the weapons time
		curtime = es.getindexprop( weaponIndex,"CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack")

		# modify it
		curtime += Rate

		# apply it
		es.setindexprop( weaponIndex,"CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack",curtime)

	'''
	Weapon Fire Modifications
	'''
	def modifyWeaponRateOfFire( self, userid, weapon ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# preppend the weapon_ if its not in the name already
		if ( not 'weapon_' in weapon ): weapon = 'weapon_' + weapon

		if ( wcsPlayer.weapons[ weapon ]['rof'] != None ):
			rof = wcsPlayer.weapons[ weapon ]['rof']

			weaponIndex = wcsPlayer.player.getWeaponIndex( weapon )

			curtime  = es.getindexprop( weaponIndex, 'CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack' )

			# invert the rof
			curtime += -rof

			es.setindexprop( weaponIndex, 'CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack', curtime )

			es.server.queuecmd( 'es_setindexprop %s "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack" %s' % ( weaponIndex, curtime ) )

	def modifyWeaponRecoil( self, userid, weapon ):
		# get player
		wcsPlayer = self.helper.players[ str(userid) ]

		# preppend the weapon_ if its not in the name already
		if ( not 'weapon_' in weapon ): weapon = 'weapon_' + weapon

		if ( wcsPlayer.weapons[ weapon ]['recoil'] != None ):
			recoil = wcsPlayer.weapons[ weapon ]['recoil']

			rand1 = randint( 0, 1 )
			rand2 = randint( 0, 1 )

			if rand1 == 0: rand1 = -1
			if rand2 == 0: rand2 = -1

			es.setplayerprop( userid, 'CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle', '%s,%s,%s' % ( recoil*rand1, recoil/2*rand2, 0 ) )

			es.server.queuecmd( 'es_setplayerprop %s "CBaseCombatWeapon.LocalActiveWeaponData.m_flNextPrimaryAttack" "%s,%s,%s"' % ( wcsPlayer, recoil*rand1, recoil/2*rand2, 0 ) )

	def disarm( self, victim, kniferace=False ):
		# get player
		wcsPlayer = self.helper.players[ str(victim) ]

		# are we playing a knife race?
		if ( kniferace == True ):
			# drop current weapon, and swap to the knife
			es.server.queuecmd( 'es_xsexec %s drop'             % ( wcsPlayer ) )
			es.server.queuecmd( 'es_xsexec %s use weapon_knife' % ( wcsPlayer ) )
		else:
			# just swap to knife
			es.server.queuecmd( 'es_xsexec %s use weapon_knife' % ( wcsPlayer ) )

