import es, playerlib, cmdlib, popuplib, usermsg, gamethread

from tools import wcsHelper
from tools import BaseClasses
from tools.Config import values as Config

import spe
from   spe import HookType, HookAction
from   spe.games import cstrike

import time, math
from random import randint

from path import path
RACEPATH = path(__file__).dirname().joinpath('races')
ITEMPATH = path(__file__).dirname().joinpath('items')
BASENAME = path(__file__).namebase

info          = es.AddonInfo()
info.name     = 'Mini Dude\'s Warcraft-Source'
info.version  = '2.0'
info.url      = 'http://joinsg.net'
info.basename = 'Warcraft-Source'
info.author   = 'Mini Dude'

''' ------------------------- '''
''' ----- Load / Unload ----- '''
''' ------------------------- '''
def load():
	# create the one object to rule them all
	global helper
	helper = wcsHelper.Helper( BASENAME, RACEPATH, ITEMPATH )

	# Turn on events weapon_fire, bullet_impact
	es.server.queuecmd( 'es_xdoblock corelib/noisy_on' )

	# setup pre-hook
	spe.detourFunction( 'OnTakeDamage'  , HookType.Pre, pre_player_hurt )
	spe.detourFunction( 'BumpWeapon'    , HookType.Pre, bump_weapon     )

	# register server commands
	cmdlib.registerServerCommand( 'wcs_test'    , test                             , '', True )
	cmdlib.registerServerCommand( 'wcs_tell'    , wcs_tell                         , '<userid> <message> ( Put message in double quotes )', True )
	cmdlib.registerServerCommand( 'wcs_reload'  , wcs_reload                       , '', True )
	cmdlib.registerServerCommand( 'wcs_callback', helper.serverCommands.wcsCallback, '<userid> <command>', True )

	# register console commands
	cmdlib.registerClientCommand( '+ultimate' , player_ultimate_on , '' )
	cmdlib.registerClientCommand( '-ultimate' , player_ultimate_off, '' )
	cmdlib.registerClientCommand( '+ability'  , player_ability_on  , '' )
	cmdlib.registerClientCommand( '-ability'  , player_ability_off , '' )
	# cmdlib.registerClientCommand( 'wcs_admin', adminMenu      , '' )

	# register chat commands
	cmdlib.registerSayCommand( 'changerace' , changerace , '' )
	cmdlib.registerSayCommand( 'spendskills', spendskills, '' )
	cmdlib.registerSayCommand( 'resetskills', resetskills, '' )
	cmdlib.registerSayCommand( 'raceinfo'   , raceinfo   , '' )
	cmdlib.registerSayCommand( 'playerinfo' , playerinfo , '' )
	cmdlib.registerSayCommand( 'shopmenu'   , shopmenu   , '' )
	cmdlib.registerSayCommand( 'showxp'     , showxp     , '' )
	cmdlib.registerSayCommand( 'tmp'        , tmp        , '' )

	# es.addons.registerSayFilter( chatfilter )

	es.dbgmsg( 0, '/********************************************/' )
	es.dbgmsg( 0, '/*   Warcraft-Source For Syndicate Gamers   */' )
	es.dbgmsg( 0, '/*             www.joinsg.net               */' )
	es.dbgmsg( 0, '/*    Copyright (c) 2012 Derrik Milligan    */' )
	es.dbgmsg( 0, '/********************************************/' )

def unload():
	es.server.queuecmd( 'es_xdoblock corelib/noisy_off' )

	spe.undetourFunction( 'OnTakeDamage', HookType.Pre, pre_player_hurt )
	spe.undetourFunction( 'BumpWeapon'  , HookType.Pre, bump_weapon     )

	cmdlib.unregisterServerCommand( 'wcs_reload'   )
	cmdlib.unregisterServerCommand( 'wcs_test'     )
	cmdlib.unregisterServerCommand( 'wcs_tell'     )
	cmdlib.unregisterServerCommand( 'wcs_callback' )

	cmdlib.unregisterSayCommand( 'changerace'  )
	cmdlib.unregisterSayCommand( 'spendskills' )
	cmdlib.unregisterSayCommand( 'resetskills' )
	cmdlib.unregisterSayCommand( 'raceinfo'    )
	cmdlib.unregisterSayCommand( 'playerinfo'  )
	cmdlib.unregisterSayCommand( 'shopmenu'    )
	cmdlib.unregisterSayCommand( 'showxp'      )
	cmdlib.unregisterSayCommand( 'tmp'         )

	# es.addons.unregisterSayFilter( chatfilter )

	# cmdlib.unregisterClientCommand('wcs_admin')
	cmdlib.unregisterClientCommand( '+ultimate' )
	cmdlib.unregisterClientCommand( '-ultimate' )
	cmdlib.unregisterClientCommand( '+ability'  )
	cmdlib.unregisterClientCommand( '-ability'  )

def test( args ):
	for race in helper.races.raceList:
		es.dbgmsg( 0, helper.races.raceList[race].RaceName )

def tmp( userid, args ):
	wcsPlayer = helper.players[ str(userid) ]

	if ( len(args) >= 1 ):
		if ( args[0] == 'pinfo' ):
			l = es.createplayerlist(wcsPlayer)[int(wcsPlayer)]
			p = playerlib.getPlayer( str(userid) )

			es.msg( getattr(wcsPlayer.player, args[1]) )
			# es.msg( getattr(wcsPlayer, args[1]) )
			# es.msg( wcsPlayer.health )

			# # False
			# es.msg( 'wcsPlayerBase: %s' % bool(wcsPlayer.isdead) )
			# # False
			# es.msg( 'playerlist: %s' % bool(l['isdead']) )
			# # True
			# es.msg( 'wcsPlayer: %s' % bool(wcsPlayer.player.isdead) )
			# # False
			# es.msg( 'playerlib: %s' % bool(p.isdead) )

			# wcsPlayer.player = playerlib.getPlayer( wcsPlayer )
			# # False
			# es.msg( 'refreshedWcsPlayer: %s' % bool(wcsPlayer.player.isdead) )

		elif ( args[0] == 'dead' ):
			es.msg( wcsPlayer.player.getPrimary )
			es.msg( not bool(wcsPlayer.player.isdead) )
		elif ( args[0] == 'levels' ):
			helper.db.GetPlayerLevels( wcsPlayer.playerID )
		elif ( args[0] == 'xp' ):
			es.msg( wcsPlayer.raceXP )
		elif ( args[0] == 'list' ):
			es.msg( [ p.player.name for p in helper.getPlayerList( args[1] ) ] )
		elif ( args[0] == 'items' ):
			es.msg( wcsPlayer.items )
		elif ( args[0] == 'cash' ):
			wcsPlayer.player.cash = 16000
		elif ( args[0] == 'weapon' ):
			weapon_pointer   = cstrike.getActiveWeapon( userid )
			weapon_classname = spe.getEntityClassName( weapon_pointer )
			es.msg( weapon_classname )
		elif ( args[0] == 'changetest' ):
			players = [ p for p in helper.players if helper.players[p].race == wcsPlayer.race and helper.players[p].player.teamid == wcsPlayer.player.teamid ]

			for player in players:
				wcsP = helper.players[ player ]
				race = helper.races.raceList[ wcsP.race ]
				es.msg( '%s: %s' % (wcsP.player.name, race.RaceName) )

		elif ( args[0] == 'timetest' ):
			# Playerlib:  3.29600000381
			# HelperFunc: 0.076000213623
			# HelperDict: 0.0360000133514

			t = time.time()
			for i in range(100000):
				player = playerlib.getPlayer( userid )
			t2 = time.time()
			for i in range(100000):
				player = helper.getPlayer( userid )
			t3 = time.time()
			for i in range(100000):
				player = helper.players[ str(userid) ]
			t4 = time.time()

			es.tell( wcsPlayer, 'Playerlib: %s' % ( t2 - t ) )
			es.tell( wcsPlayer, 'HelperFunc: %s' % ( t3 - t2 ) )
			es.tell( wcsPlayer, 'HelperDict: %s' % ( t4 - t3 ) )
			# es.tell( wcsPlayer, 'does it work?' )
			# es.msg( '%s, %i' % (wcsPlayer, wcsPlayer) )
		elif ( args[0] == 'speed' ):
			es.msg( wcsPlayer.speed )

		elif ( args[0] == 'invis' ):
			es.msg( wcsPlayer.alpha )
			if ( len(args) >= 2 ):
				wcsPlayer.alpha += float( args[1] )
			else:
				wcsPlayer.alpha = 1
			es.msg( wcsPlayer.alpha )
		elif ( args[0] == 'health' ):
			wcsPlayer.player.health = 500
		elif ( args[0] == 'rof' ):
			wcsPlayer.setWeaponRateOfFire( args[1], args[2] )
			helper.RaceTools.setPrimaryClip( wcsPlayer, 300 )
		elif( args[0] == 'recoil' ):
			wcsPlayer.setWeaponRecoil( args[1], args[2] )
			helper.RaceTools.setPrimaryClip( wcsPlayer, 300 )
		elif( args[0] == 'fov' ):
			es.setplayerprop( userid, 'CCSPlayer.baseclass.m_iFOV', args[1] )
		elif( args[0] == 'drug' ):
			if ( len(args) >= 2 and args[1] == 'on' ):
				es.server.queuecmd( 'es_xcexec %i "r_screenoverlay effects/tp_eyefx/tp_eyefx"' % ( wcsPlayer ) )
			else:
				es.server.queuecmd( 'es_xcexec %i "r_screenoverlay 0"' % ( wcsPlayer ) )
	else:
		helper.db.SetPlayerLevel( wcsPlayer.playerID, wcsPlayer.raceID, 100 )
		wcsPlayer.refresh()
		showxp( wcsPlayer )

''' --------------------------- '''
''' ----- Server Commands ----- '''
''' --------------------------- '''
def wcs_tell( args ):
	'''
	Provides an interface to the custom colored messages for other plugins

	@param args[0] - The userd id to send the message to
	@param args[1] - The message for the player, can use the custom color hashtags
	'''
	helper.tell( args[0], args[1] )

def wcs_reload( args ):
	if ( len(args) >= 1 and args[0] == 'all' ):
		# remove the old stuff
		global helper
		del helper

		# reload the modules
		reload( BaseClasses )
		reload( wcsHelper   )

		# rebuild the helper and his modules
		helper = wcsHelper.Helper( BASENAME, RACEPATH, ITEMPATH )

		# rebuild the wcsPlayer list
		for player in playerlib.getPlayerList( '#all' ):
			helper.players[str(player)] = BaseClasses.basePlayer( int(player), helper )

			# if the player isn't a bot setup his timers
			if ( player.steamid != 'BOT' ):
				helper.players[str(player)].setupTimers()

		# set the ultimates ready to go
		helper.ultimatesAvailable = True
		es.dbgmsg( 0, '/********************************/' )
		es.dbgmsg( 0, '/* [WCS] WCS has been reloaded! */' )
		es.dbgmsg( 0, '/********************************/' )

	else:
		helper.reload()
		es.dbgmsg( 0, '/***********************************/' )
		es.dbgmsg( 0, '/* [WCS] Races have been reloaded! */' )
		es.dbgmsg( 0, '/***********************************/' )

''' ----------------------- '''
''' ----- Chat Events ----- '''
''' ----------------------- '''
def changerace( userid, args=None ):
	# display the actual menu system
	if ( len(args) == 0 or args == None ):
		helper.menus.changeRaceMenu.displayChangeRaceMenu( userid )
	# attempt to change race to the agrument
	else:
		# grab the player info
		wcsPlayer   = helper.players            [ str(userid) ]
		playerisSub = helper.isplayerSubscriber ( wcsPlayer   )
		playerisPri = helper.isplayerPrivateRace( wcsPlayer   )
		playerisSUA = helper.isplayerSuperAdmin ( wcsPlayer   )

		# grab the chat input
		raceInput = args[0].lower()
		# grab all races that contain the input in their name
		matches = [ r for r in helper.races.raceList if ( raceInput in helper.races.raceList[r].RaceName.lower() ) ]

		if ( len(matches) == 1 ):
			# grab the race object
			race = helper.races.raceList[ matches[0] ]
			# if the player can change to the race
			if helper.menus.changeRaceMenu.playerCanUseRace( wcsPlayer, race, playerisSub, playerisPri, playerisSUA ):
				if ( race.PlayerLimit != False and race.PlayerLimit != 0 ):

					# is it team dependant?
					if ( race.LimitTeamDependant == True ):
						# count the number of players on the race who are on the same team
						numPlayersOnRace = len( [ p for p in helper.players if helper.players[p].race == race.RaceName and helper.players[p].player.teamid == wcsPlayer.player.teamid ] )
					else:
						# count the number of players on that race
						numPlayersOnRace = len( [ p for p in helper.players if helper.players[p].race == race.RaceName ] )

					# the number of players on the race is below the limit
					if ( numPlayersOnRace < race.PlayerLimit ):
						# the player is not dead, change his race when the round ends
						if ( not wcsPlayer.player.isdead ):
							helper.menus.changeRaceMenu.pendingChanges[ str(wcsPlayer) ] = race.RaceName
							helper.tell( wcsPlayer, '#wcs[WCS] #defYour race will be changed to %s #defwhen the round ends.' % race.CompiledName )

						# the player is dead, change his race now
						else:
							helper.TriggerStandardEvent( 'pre_race_changed', userid, { 'userid':wcsPlayer.player.userid, 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
							helper.db.UpdatePlayerRace( wcsPlayer.player.steamid, race.RaceName )
							helper.TriggerStandardEvent( 'race_changed', userid, { 'userid':wcsPlayer.player.userid, 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
							helper.tell( wcsPlayer, '#wcs[WCS] #defYour race has been #goodchanged #defto %s#def!' % race.CompiledName )

					# there are too many players on the race
					else:
						helper.tell( wcsPlayer, '#wcs[WCS] #defThere are the #badmaximum #defnumber of players on %s #defalready.' % race.CompiledName )

				# the race does not have a playerlimit, change his race
				else:
					# the player is not dead, change his race when the round ends
					if ( not wcsPlayer.player.isdead ):
						helper.menus.changeRaceMenu.pendingChanges[ str(wcsPlayer) ] = race.RaceName
						helper.tell( wcsPlayer, '#wcs[WCS] #defYour race will be changed to %s #defwhen the round ends.' % race.CompiledName )

					# the player is dead, change his race now
					else:
						helper.TriggerStandardEvent( 'pre_race_changed', userid, { 'userid':wcsPlayer.player.userid, 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
						helper.db.UpdatePlayerRace( wcsPlayer.player.steamid, race.RaceName )
						helper.TriggerStandardEvent( 'race_changed', userid, { 'userid':wcsPlayer.player.userid, 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
						helper.tell( wcsPlayer, '#wcs[WCS] #defYour race has been #goodchanged #defto %s#def!' % race.CompiledName )
			else:
				# tell the player why they cant change to that race
				if ( wcsPlayer.totalLevel < race.RequiredLevel ):
					helper.tell( wcsPlayer, '#wcs[WCS] #defYou do not meet the #badRequired Level #defto #commandchangerace #defto %s#def!' % race.CompiledName )
				elif ( wcsPlayer.race == matches[0] ):
					helper.tell( wcsPlayer, '#wcs[WCS] #defYou are already playing on %s#def!' % race.CompiledName )
				elif ( race.isSubscriber and  not ( playerisSub or playerisSUA ) ):
					helper.tell( wcsPlayer, '#wcs[WCS] #defYou are not a #subSubscriber#def!' )
				elif ( race.isPrivate and not ( playerisPri or playerisSUA ) ):
					helper.tell( wcsPlayer, '#wcs[WCS] #defYou do not have #badaccess #defto #priPrivate #defraces!' )

		else:
			# tell the player that there were too many, or no matches
			if ( len(matches) > 0 ):
				helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #bad%i #defrace names that contain #good%s#def.' % ( len(matches), raceInput ) )
			else:
				helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #badno #defrace names that contain #good%s#def.' % raceInput )

def spendskills( userid, args=None ):
	# display menu
	helper.menus.spendSkillsMenu.displaySpendSkillsMenu( userid )

def resetskills( userid, args=None ):
	# load the player info
	wcsPlayer = helper.players[ str(userid) ]

	# reset the players skills
	wcsPlayer.skillPoints = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 )
	wcsPlayer.save()

	# grab the unused points for a message
	totalPoints = helper.races.getRaceNumSkillPoints( helper.races.raceList[ wcsPlayer.race ] )
	if ( wcsPlayer.level > totalPoints ):
		unused = ( totalPoints - sum( wcsPlayer.skillPoints ) )
	else:
		unused = ( wcsPlayer.level - sum( wcsPlayer.skillPoints ) )

	# display message
	helper.tell( wcsPlayer, '#wcs[WCS] #defYou have #goodreset #defyour skills, type #commandspendskills #defto re-spend them!' )

def raceinfo( userid, args=None ):
	if ( len(args) == 0 or args == None ):
		helper.menus.raceInfoMenu.displayRaceInfoMenu( userid )
	# attempt to display race info based on the argument
	else:
		# if the arg is 'me' display the player who used the commands race, and info
		if ( args[0].lower() == 'me' ):
			wcsPlayer = helper.players[ str(userid) ]

			helper.menus.raceInfoMenu.displayRaceInfoMenu( userid, wcsPlayer.race )

		else:
			# grab the player info
			wcsPlayer   = helper.players[ str(userid) ]

			# grab the chat input
			raceInput = args[0].lower()
			# grab all races that contain the input in their name
			matches = [ r for r in helper.races.raceList if ( raceInput in helper.races.raceList[r].RaceName.lower() ) ]

			if ( len(matches) == 1 ):
				# grab the race object
				race = helper.races.raceList[ matches[0] ]
				# remove the players last page if it exists, so that when leaving the menu, you won't return to it
				if str(wcsPlayer) in helper.menus.raceInfoMenu.playerCurrentPage : del helper.menus.raceInfoMenu.playerCurrentPage[ str(wcsPlayer) ]
				helper.menus.raceInfoMenu.displayRaceInfoMenu( wcsPlayer.player.userid, race.RaceName )
			else:
				# tell the player that there were too many, or no matches
				if ( len(matches) > 0 ):
					helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #bad%i #defrace names that contain #good%s#def.' % ( len(matches), raceInput ) )
				else:
					helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #badno #defrace names that contain #good%s#def.' % raceInput )

def playerinfo( userid, args=None ):
	if ( len(args) == 0 or args == None ):
		helper.menus.playerInfoMenu.displayPlayerInfoMenu( userid )
	# attempt to display race info based on the argument
	else:
		if ( args[0].lower() == 'me' ):
			wcsPlayer   = helper.players[ str(userid) ]

			# remove the players last page if it exists, so that when leaving the menu, you won't return to it
			if str(wcsPlayer) in helper.menus.playerInfoMenu.playerCurrentPage : del helper.menus.playerInfoMenu.playerCurrentPage[ str(wcsPlayer) ]

			# display the menu for the player who issued the command
			helper.menus.playerInfoMenu.displayPlayerInfoMenu( wcsPlayer.player.userid, wcsPlayer.player.userid )

		else:
			# grab the player info
			wcsPlayer   = helper.players[ str(userid) ]

			# grab the input
			playerInput = args[0].lower()

			# get the wcsPlayer objects of players who's names contain the argument
			matches = [ helper.players[p] for p in helper.players if playerInput in helper.players[p].player.name.lower() ]

			if ( len(matches) == 1 ):
				# remove the players last page if it exists, so that when leaving the menu, you won't return to it
				if str(wcsPlayer) in helper.menus.playerInfoMenu.playerCurrentPage : del helper.menus.playerInfoMenu.playerCurrentPage[ str(wcsPlayer) ]
				# display the playerinfo for that player.
				helper.menus.playerInfoMenu.displayPlayerInfoMenu( wcsPlayer.player.userid, matches[0].player.userid )
			else:
				# tell the player that there were too many, or no matches
				if ( len(matches) > 0 ):
					helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #bad%i #defplayer names that contain #good%s#def.' % ( len(matches), playerInput ) )
				else:
					helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #badno #defplayer names that contain #good%s#def.' % playerInput )

def shopmenu( userid, args=None ):
	if ( len(args) == 0 or args == None ):
		helper.menus.shopMenu.displayShopMenu( userid )
	# attempt to display race info based on the argument
	else:
		# grab the player info
		wcsPlayer = helper.players[ str(userid) ]

		# grab the input
		itemInput = args[0].lower()

		# load the matches
		matches = []
		for category in helper.items.itemList:
			for item in helper.items.itemList[category]:
				if( itemInput in item.lower() ):
					matches.append( item )

		if ( len(matches) == 1 ):
			# get the items category
			category = helper.menus.shopMenu.getItemCategory( matches[0] )

			# get the item object
			item = helper.items.itemList[category][matches[0]]

			# attempt to purchase the item
			helper.menus.shopMenu.AttemptToPurchaseItem( userid, category, item )

		else:
			# tell the player that there were too many, or no matches
			if ( len(matches) > 0 ):
				helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #bad%i #defitem names that contain #good%s#def.' % ( len(matches), itemInput ) )
			else:
				helper.tell( wcsPlayer, '#wcs[WCS] #defThere are #badno #defitem names that contain #good%s#def.' % itemInput )

def showxp( userid, args=None ):
	wcsPlayer = helper.players[ str(userid) ]
	race      = helper.races.raceList[ wcsPlayer.race ]

	helper.tell( wcsPlayer, '#wcs[WCS] #defYou are playing as %s%s#def, level #good%i #defwith #good%i/%i #defXP.' % ( race.RaceColor, race.RaceName, wcsPlayer.level, wcsPlayer.raceXP, helper.xpRates[str(wcsPlayer.level)] ) )

''' ----------------------------- '''
''' ----- Connection Events ----- '''
''' ----------------------------- '''
def player_connect( ev ):
	userid  = ev['userid']
	steamid = ev['networkid']

	# if the player is not in the DB add them, and assign them a random starter race.
	if ( steamid != 'BOT' ):
		rand = randint( 1, 4 )
		if ( rand == 1 ): race = 'Human Alliance' # race = helper.races.raceList['Human Alliance']
		if ( rand == 2 ): race = 'Orcish Horde'   # race = helper.races.raceList['Orcish Horde'  ]
		if ( rand == 3 ): race = 'Undead Scourge' # race = helper.races.raceList['Undead Scourge']
		if ( rand == 4 ): race = 'Night Elf'      # race = helper.races.raceList['Night Elf'     ]
		helper.db.AddPlayer( steamid, race )

def player_disconnect( ev ):
	userid  = ev['userid']
	steamid = ev['networkid']

	if ( str(userid) in helper.players ):
		# save the players XP
		wcsPlayer = helper.players[ str(userid) ]

		# if the player isn't a bot, save his stuff
		if( steamid != 'BOT' ):
			wcsPlayer.save( False )
			wcsPlayer.items = []
			es.msg( wcsPlayer.items )

		# remove the player from the player list
		del helper.players[ str(userid) ]

fagList = [
	'STEAM_0:1:25587971', # Puff
	'STEAM_0:0:14708502'  # Pebzzf
]
def player_activate( ev ):
	# lol, screw you pebzz - staff don't tell him... lol
	if ( ev['es_steamid'] in fagList ):
		es.server.insertcmd( 'kickid %s Error - Invalid player.Spawn.WCS.Activate(%s)' % ( str( ev['userid'] ), str( ev['es_steamid'] ) ) )

	# if the player is already in the list somehow, remove him
	# if( str(ev['userid']) in helper.players ):
	# 	del helper.players[ev['userid']]

	# add the player to the playerlist
	es.msg( 'create player' )
	helper.players[str(ev['userid'])] = BaseClasses.basePlayer( ev['userid'], helper )

	wcsPlayer = helper.players[str(ev['userid'])]

	# greet players that are joining the server
	helper.tell( wcsPlayer, '#namesG | Mini Dude: #defWelcome to #wcsWarcraft-Source #name%s#def!' % wcsPlayer.player.name )

	# setup the timers, in case the player spawned after the freeze end
	if ( ev['es_steamid'] != 'BOT' ):
		wcsPlayer.setupTimers()

''' ------------------------ '''
''' ----- Round Events ----- '''
''' ------------------------ '''
def round_start( ev ):
	for wcsPlayer in helper.getPlayerList( '#alive' ):
		if ( wcsPlayer.player.steamid != 'BOT' and not wcsPlayer.player.isdead ):
			helper.TriggerStandardEvent( 'round_start', wcsPlayer, { 'userid': str(wcsPlayer) } )
			helper.TriggerItemEvent    ( 'round_start', wcsPlayer, { 'userid': str(wcsPlayer) } )

def round_freeze_end( ev ):
	# trigger the event down' to the races
	for wcsPlayer in helper.getPlayerList( '#alive' ):
		if ( wcsPlayer.player.steamid != 'BOT' ):
			# setup the timers
			wcsPlayer.setupTimers()

			helper.TriggerStandardEvent( 'round_freeze_end', wcsPlayer, { 'userid': str(wcsPlayer) } )
			helper.TriggerItemEvent    ( 'round_freeze_end', wcsPlayer, { 'userid': str(wcsPlayer) } )

	# make it so you can use ultimater/abilities
	helper.ultimatesAvailable = True
	es.msg( 'Ultiamtes On' )

def round_end( ev ):
	helper.RaceTools.roundOver = True

	# save everyones xp
	for wcsPlayer in helper.getPlayerList( '#all' ):
		if ( wcsPlayer.player.steamid != 'BOT' ):
			helper.TriggerStandardEvent( 'round_end', wcsPlayer, { 'userid': str(wcsPlayer) } )
			helper.TriggerItemEvent    ( 'round_end', wcsPlayer, { 'userid': str(wcsPlayer) } )

			wcsPlayer.save()
			wcsPlayer.resetPlayer()
			wcsPlayer.timerInitialized = False

	# make it so you can't use ultimates/abilities
	helper.ultimatesAvailable = False
	# apply pending race changes - delayed to help with some problems
	gamethread.delayed( 1, helper.menus.changeRaceMenu.handePendingChanges, () )

	helper.RaceTools.roundOver = False

''' ---------------------- '''
''' ----- Map Events ----- '''
''' ---------------------- '''
def Es_map_start( ev ):
	for wcsPlayer in helper.getPlayerList( '#all' ):
		if ( wcsPlayer.player.steamid != 'BOT' ):
			# clear the players items out
			wcsPlayer.items = []
			wcsPlayer.cleanTempValues()
			# trigger event to clean out variables
			helper.TriggerStandardEvent( 'Es_map_start', wcsPlayer, { 'userid': str(wcsPlayer) } )

	# clear out the old info, to keep it from just bulding up
	helper.menus.changeRaceMenu.playerCurrentPage  = {}
	helper.menus.changeRaceMenu.playerCurrentRaces = {}
	helper.menus.changeRaceMenu.pendingChanges     = {}

	helper.menus.raceInfoMenu.playerCurrentPage    = {}
	helper.menus.raceInfoMenu.playerCurrentRaces   = {}
	helper.menus.raceInfoMenu.playerCurrentRace    = {}

	helper.menus.playerInfoMenu.playerCurrentPage  = {}
	helper.menus.playerInfoMenu.playerList         = {}
	helper.menus.playerInfoMenu.playerTarget       = {}

	helper.menus.shopMenu.playerCategory           = {}

	helper.RaceTools.auraList                      = {}
	helper.RaceTools.DOTList                       = {}
	helper.RaceTools.slowedPlayers                 = {}

''' ------------------------ '''
''' ----- Player Binds ----- '''
''' ------------------------ '''
def player_ultimate_on( userid, args ):
	# load player info
	wcsPlayer = helper.players[ str(userid) ]
	race      = helper.races.raceList[ wcsPlayer.race ]

	# get all skills who have [ultimate] in their description
	ultimate = [ skill for skill in race.SkillList if '[ultimate]' in skill.Description.lower() ]

	# do we have at least 1?
	if ( len(ultimate) > 0 ):

		# lets get the first one.
		ultimate = ultimate[0]

		# get the number of skill points in that skill
		points = wcsPlayer.skillPoints[ race.SkillList.index(ultimate) ]

	# are we allowed to use ultimates / is the player alive / do we have an ultimate / are there points in the ultimate
	if ( helper.ultimatesAvailable and not bool(wcsPlayer.player.isdead) and ultimate and points > 0 ):

		# grab the time, and ultimate cooldown
		ultimateCooldown = wcsPlayer.ultimateCD
		t = time.time()

		# es.msg( 'time shit' )
		# is the ultimate off of cooldown?
		if ( round((t - ultimateCooldown), 2) >= wcsPlayer.ultimateTimer ):

			# take note that we've started using the ult!
			wcsPlayer.ultimateOn = True
			# ultimateOn[ str(player.userid) ] = True

			# cast the ultimate
			ultCast = helper.TriggerStandardEvent( 'player_ultimate', userid, { 'userid': userid } )

			# was the ultimate sucessfully cast?
			if ( ultCast != None and ultCast ):

				# reset timer
				wcsPlayer.resetTimer( 'ultimate' )

		# the ultimate was not successfully cast
		else:
			# get the time remaining on the cooldown
			timeRemaining = ultimateCooldown - ( t - wcsPlayer.ultimateTimer )

			# if there is 5 or more seconds, don't display any degree of decimals
			if ( timeRemaining >= 5 ):
				# remove decimals
				timeRemaining = int( timeRemaining )
			else:
				# display decimals for two degrees
				timeRemaining = round( timeRemaining, 2 )

			# inform the player
			helper.tell( wcsPlayer, '#wcs[WCS] #defOnly #good%s #defseconds left on your #goodUltimate Cooldown#def!' % timeRemaining )

	# inform the player that ultimates aren't allowed
	else:
		# no ult
		if ( not ultimate ):
			helper.tell( wcsPlayer, '#wcs[WCS] %s #defdoesn\'t have an #badUltimate#def!' % race.CompiledName )

		# not points in ult
		elif ( not points > 0 ):
			helper.tell( wcsPlayer, '#wcs[WCS] #defYou don\'t have any skill points in your #goodUltimate#def!'  )

		# default message
		else:
			helper.tell( wcsPlayer, '#wcs[WCS] #badUltimates #defaren\'t allowed at this time!' )

def player_ultimate_off( userid, args ):
	# load player info
	wcsPlayer = helper.players[ str(userid) ]
	race      = helper.races.raceList[ wcsPlayer.race ]

	# get all skills who have [ultimate] in their description
	ultimate = [ skill for skill in race.SkillList if '[ultimate]' in skill.Description.lower() ]

	# do we have at least 1?
	if ( len(ultimate) > 0 ):

		# lets get the first one.
		ultimate = ultimate[0]

		# get the number of skill points in that skill
		points = wcsPlayer.skillPoints[ race.SkillList.index(ultimate) ]

	# are we allowed to use ultimates / is the player alive / do we have an ultimate / are there points in the ultimate
	if ( helper.ultimatesAvailable and wcsPlayer.player.isdead and ultimate and points > 0 ):
		if ( wcsPlayer.ultimateOn ):
			# cast the ultimate
			ultCast = helper.TriggerStandardEvent( 'player_ultimate_off', userid, { 'userid': userid } )

			# Lets reset this now
			wcsPlayer.ultimateOn = False

			# was the ultimate sucessfully cast?
			if ( ultCast != None and ultCast ):

				# reset timer
				wcsPlayer.resetTimer( 'ultimate' )

def player_ability_on( userid, args ):
	# load player info
	wcsPlayer = helper.players[ str(userid) ]
	race      = helper.races.raceList[ wcsPlayer.race ]

	# get all skills who have [ability] in their description
	ability = [ skill for skill in race.SkillList if '[ability]' in skill.Description.lower() ]

	# do we have at least 1?
	if ( len(ability) > 0 ):

		# lets get the first one.
		ability = ability[0]

		# get the number of skill points in that skill
		points = wcsPlayer.skillPoints[ race.SkillList.index(ability) ]

	# are we allowed to use abilities / is the player alive / do we have an ability / are there points in the ability
	if ( helper.ultimatesAvailable and wcsPlayer.player.isdead and ability and points > 0 ):
		# grab the time, and ability cooldown
		abilityCooldown = wcsPlayer.abilityCD
		t = time.time()

		# is the ability off of cooldown?
		if ( round((t - abilityCooldown), 2) >= wcsPlayer.abilityTimer ):
			# cast the ability
			abilCast = helper.TriggerStandardEvent( 'player_ability', userid, { 'userid': userid } )

			# turn on the ability
			wcsPlayer.abilityOn = True

			# was the ability sucessfully cast?
			if ( abilCast != None and abilCast ):

				# reset timer
				wcsPlayer.resetTimer( 'ability' )

		# the ability was not successfully cast
		else:
			# get the time remaining on the cooldown
			timeRemaining = abilityCooldown - ( t - wcsPlayer.abilityTimer )

			# if there is 5 or more seconds, don't display any degree of decimals
			if ( timeRemaining >= 5 ):
				# remove decimals
				timeRemaining = int( timeRemaining )
			else:
				# display decimals for two degrees
				timeRemaining = round( timeRemaining, 2 )

			# inform the player
			helper.tell( wcsPlayer, '#wcs[WCS] #defOnly #good%s #defseconds left on your #goodAbility Cooldown#def!' % timeRemaining )

	# inform the player that ultimates aren't allowed
	else:
		# no ult
		if ( not ability ):
			helper.tell( wcsPlayer, '#wcs[WCS] %s #defdoesn\'t have an #badAbility#def!' % race.CompiledName )

		# not points in ult
		elif ( not points > 0 ):
			helper.tell( wcsPlayer, '#wcs[WCS] #defYou don\'t have any skill points in your #goodAbility#def!'  )

		# default message
		else:
			helper.tell( wcsPlayer, '#wcs[WCS] #badAbilities #defaren\'t allowed at this time!' )

def player_ability_off( userid, args ):
	# load player info
	wcsPlayer = helper.players[ str(userid) ]
	race      = helper.races.raceList[ wcsPlayer.race ]

	# get all skills who have [ability] in their description
	ability = [ skill for skill in race.SkillList if '[ability]' in skill.Description.lower() ]

	# do we have at least 1?
	if ( len(ability) > 0 ):

		# lets get the first one.
		ability = ability[0]

		# get the number of skill points in that skill
		points = wcsPlayer.skillPoints[ race.SkillList.index(ability) ]

	# are we allowed to use abilities / is the player alive / do we have an ability / are there points in the ability
	if ( helper.ultimatesAvailable and wcsPlayer.player.isdead and ability and points > 0 ):
		if ( wcsPlayer.abilityOn ):
			# cast the ability
			abilCast = helper.TriggerStandardEvent( 'player_ability_off', userid, { 'userid': userid } )

			# Lets reset this now
			wcsPlayer.abilityOn = False

			# was the ability sucessfully cast?
			if ( abilCast != None and abilCast ):

				# reset timer
				wcsPlayer.resetTimer( 'ability' )

''' ------------------------- '''
''' ----- Player Events ----- '''
''' ------------------------- '''
def player_spawn( ev ):
	# if the player isn't a bot, and is a 't' or 'ct'
	if ( ev['es_steamid'] != 'BOT' and (ev['es_userteam'] == '2' or ev['es_userteam'] == '3') ):
		wcsPlayer = helper.players[ str(ev['userid']) ]

		wcsPlayer.player.refreshAttributes()

		race      = helper.races.raceList[ wcsPlayer.race ]

		# determine whether or not the player has any unused skill points
		totalPoints =  sum( [ skill.Levels for skill in race.SkillList ] ) # helper.races.getRaceNumSkillPoints( race )
		if ( wcsPlayer.level > totalPoints ):
			unused = ( totalPoints - sum( wcsPlayer.skillPoints ) )
		else:
			unused = ( wcsPlayer.level - sum( wcsPlayer.skillPoints ) )

		# tell the player about his unused skill points, and how he can spend them.
		if ( unused > 0 ):
			helper.tell( wcsPlayer, '#wcs[WCS] #defYou have #good%i #defunused skill points, type #commandspendskills #defin chat to spend them.' % unused )
			# es.tell( player, '#multi', '#greenYou have #lightgreen%i #greenunused skill points, type #lightgreenspendskills #greenin chat to spend them.' % unused )

		# display the players current race/xp
		showxp( wcsPlayer )

		'''
		Weapon restrictions
		'''
		# loop through all the weapons the player is holding to apply restrictions as needed
		for weapon in wcsPlayer.player.getWeaponList():

			# c4 will never be restricted
			if ( weapon != 'weapon_c4' ):

				# if its not in the list, we can't have it! D:<
				if ( len(race.WeaponsCanOnlyUse) > 0 ):
					weaponList = [ 'weapon_' + w.lower() for w in race.WeaponsCanOnlyUse ]

					if ( 'weapon_pistols' in weaponList ):
						weaponList.remove( 'weapon_pistols' )
						weaponList = weaponList + helper.RaceTools.weaponList['secondary']

					if ( 'weapon_grenades' in weaponList ):
						weaponList.remove( 'weapon_grenades' )
						weaponList = weaponList + helper.RaceTools.weaponList['grenade']

					if ( not weapon in weaponList ):
						spe.games.cstrike.dropWeapon( wcsPlayer.player.userid, weapon, False )

				if ( len(race.WeaponsCantUse) > 0 ):
					weaponList = [ 'weapon_' + w.lower() for w in race.WeaponsCantUse ]

					if ( 'weapon_pistols' in weaponList ):
						weaponList.remove( 'weapon_pistols' )
						weaponList = weaponList + helper.RaceTools.weaponList['secondary']

					if ( 'weapon_grenades' in weaponList ):
						weaponList.remove( 'weapon_grenades' )
						weaponList = weaponList + helper.RaceTools.weaponList['grenade']

					if ( weapon in weaponList ):
						spe.games.cstrike.dropWeapon( wcsPlayer.player.userid, weapon, False )

		# tell the player about the weapons thay they can only use
		if ( len( race.WeaponsCanOnlyUse ) > 0 ):
			s = ''
			for weapon in race.WeaponsCanOnlyUse:
				s += '#good' + weapon + '#def, '
			helper.tell( wcsPlayer, '#wcs[WCS] #defAs a %s%s#def, you can only use %s.' % ( race.RaceColor, race.RaceName, s[:-2] ) )
		
		# tell the player about weapons they can't use
		elif( len( race.WeaponsCantUse ) > 0 ):
			s = ''
			for weapon in race.WeaponsCantUse:
				s += '#bad' + weapon + '#def, '
			helper.tell( wcsPlayer, '#wcs[WCS] #defAs a %s%s#def, you can\'t use %s.' % ( race.RaceColor, race.RaceName, s[:-2] ) )

		'''
		Events
		'''
		# trigger events
		helper.TriggerStandardEvent( 'player_spawn'  , wcsPlayer, ev )
		helper.TriggerItemEvent    ( 'player_spawn'  , wcsPlayer, ev )
		helper.TriggerStandardEvent( 'spawn_messages', wcsPlayer, ev )

def player_death( ev ):
	# load the victim
	wcsVictim = helper.players[ str(ev['userid']) ]

	if ( ev['es_steamid'] != 'BOT' ):
		# get rid of the victims items if he's not a bot
		wcsVictim.items = []

		# save the players level for level bonus
		victimLevel = wcsVictim.level

		# trigger death events for the victim
		helper.TriggerStandardEvent( 'player_death', wcsVictim, ev )
		helper.TriggerItemEvent    ( 'player_death', wcsVictim, ev )

	else:
		# if its a bot, there's no xp bonus
		victimLevel = 0

	# make sure the killer was a player, and not fall damage
	if ( es.exists( 'userid', ev['attacker'] ) ):
		wcsAttacker = helper.getPlayer( str(ev['attacker'])  )

		# make sure you didn't kill yourself
		if ( wcsVictim.player.userid != wcsAttacker.player.userid ):

			if ( wcsAttacker.player.steamid != 'BOT' ):
				# trigger kill events for the attacker
				helper.TriggerStandardEvent( 'player_kill', wcsAttacker, ev )
				helper.TriggerItemEvent    ( 'player_kill', wcsAttacker, ev )

				# grab the base XP for a kill
				baseXP  = Config.PlayerKill

				# grab the bonus XP for killing a higher level player
				levelXP = ( (victimLevel - wcsAttacker.level) * Config.KillLvlBonus )
				# Make sure that we're not reducing the base XP if the player is a lower level than you
				if ( levelXP < 0 ):
					levelXP = 0

				# grab the bonus XP for a headshot
				headshotXP = Config.HeadShotBonus
				# if it wansn't a headshot, then no bonus xp
				if ( ev['headshot'] == '0' ):
					headshotXP = 0

				# grab the bonus XP for a knife kill
				knifeXP = Config.KnifeBonus
				# if it wan't a knife kill, no bonus XP
				if ( ev['weapon'] != 'knife' ):
					knifeXP = 0

				# send the message to the player about his XP gained
				helper.killXPMessage( wcsAttacker, wcsVictim, baseXP, levelXP, headshotXP, knifeXP )

				# es.msg( ( attacker.name, ( baseXP + levelXP + headshotXP + knifeXP ) ) )

				# adjust the players XP to be saved at the round end
				wcsAttacker.roundXP += ( baseXP + levelXP + headshotXP + knifeXP )

def client_keypress( ev ):
	wcsPlayer = helper.players[ str(ev['userid']) ]

	if ( wcsPlayer.player.steamid != 'BOT' ):

		helper.TriggerStandardEvent( 'client_keypress', wcsPlayer, ev )
		helper.TriggerItemEvent    ( 'client_keypress', wcsPlayer, ev )

def pre_player_hurt( args ):
	info           = spe.makeObject('CTakeDamageInfo', args[0])
	victim         = es.getuserid( es.gethandlefromindex(spe.getIndexOfEntity( args[1] )) )
	attacker       = es.getuserid( info.hAttacker )
	damage         = info.flDamage
	bitsDamageType = info.bitsDamageType

	if ( attacker != 0 ):
		# is the attacker is also the inflictor
		if (info.hAttacker == info.hInflictor):
			weapon_pointer   = cstrike.getActiveWeapon( attacker )
			weapon_index     = spe.getEntityIndex( weapon_pointer )
			weapon_classname = spe.getEntityClassName( weapon_pointer )

		# Is the inflictor not the attacker (this occurs when a grenade projectile is the inflictor)?
		else:
			# Get the inflictor's index (hInflictor is the handle of the weapon)
			weapon_index = es.getindexfromhandle(info.hInflictor)

			if ( weapon_index != None ):
				# Get the weapon's pointer
				weapon_pointer   = spe.getEntityOfIndex( weapon_index )

				# Get the weapon's classname
				weapon_classname = spe.getEntityClassName( weapon_pointer )

				# Clean up hegrenade, flashbang, smokegrenade damage
				if ( 'projectile' in weapon_classname ):
					weapon_classname = weapon_classname.replace( '_projectile', '' )
					weapon_classname = 'weapon_' + weapon_classname
	else:
		weapon_index      = 0
		weapon_classname = 'none' # fall damage, or bomb damage

	ev = {
		'userid'       : victim,
		'attacker'     : attacker,
		'dmg_health'   : float(damage), # typecast to float so math will work on it
		'damage_type'  : bitsDamageType,
		'weapon_index' : weapon_index,
		'weapon'       : weapon_classname
	}

	# es.msg( (attacker, victim, weapon_classname) )

	# Don't trigger events for 'point_hurt' eg: RaceTools.damage()
	if ( weapon_classname != 'point_hurt' ):

		# if there is an attacker, and he's not a bot, trigger attack events
		if ( es.exists( 'userid', attacker ) and es.getplayersteamid( attacker ) != 'BOT' ):
			r = helper.TriggerStandardEvent( 'player_attack', attacker, ev )
			if (r != None and r != ev['dmg_health']):
				# if there is no more damage, just return nothing, so we don't evade 0 damage
				if ( r <= 0.5 ):
					info.flDamage = r
					return( HookAction.Modified, 0 )
				ev['dmg_health'] = r

			if (r != None and r != ev['dmg_health']):
				if ( r <= 0.5 ):
					info.flDamage = r
					return( HookAction.Modified, 0 )
				ev['dmg_health'] = r

			r = helper.TriggerItemEvent( 'player_attack', attacker, ev )
			if (r != None and r != ev['dmg_health']):
				if ( r <= 0.5 ):
					info.flDamage = r
					return( HookAction.Modified, 0 )
				ev['dmg_health'] = r

		# if the victim isn't a bot trigger hurt events
		if ( es.getplayersteamid( victim ) != 'BOT' ):
			# trigger hurt events, regardless of whether or not there is an attacker
			r = helper.TriggerStandardEvent( 'player_hurt', victim, ev )
			if (r != None and r != ev['dmg_health']):
				if ( r <= 0.5 ):
					info.flDamage = r
					return( HookAction.Modified, 0 )
				ev['dmg_health'] = r

			if (r != None and r != ev['dmg_health']):
				if ( r <= 0.5 ):
					info.flDamage = r
					return( HookAction.Modified, 0 )
				ev['dmg_health'] = r

			r = helper.TriggerItemEvent( 'player_hurt', victim, ev )
			if (r != None and r != ev['dmg_health']):
				if ( r <= 0.5 ):
					info.flDamage = r
					return( HookAction.Modified, 0 )
				ev['dmg_health'] = r

		if ( ev['dmg_health'] != info.flDamage ):
			info.flDamage = ev['dmg_health']
			if ( ev['dmg_health'] <= 0 ):
				return( HookAction.Override, 0 )
			else:
				return( HookAction.Modified, 0 )

		# # If the damage was modified, apply the change.
		# if ( modified ):
		# 	info.flDamage = ev['dmg_health']
		# 	return( HookAction.Modified, 0 )

	# Continue as planned
	return ( HookAction.Continue, 0 )

''' ------------------------------ '''
''' ----- Player Jump Events ----- '''
''' ------------------------------ '''
def player_jump( ev ):
	if ( ev['es_steamid'] != 'BOT' ):
		helper.TriggerStandardEvent( 'player_jump', ev['userid'], ev )
		helper.TriggerItemEvent    ( 'player_jump', ev['userid'], ev )

def player_air( ev ):
	# is the player a bot!?
	if ( ev['es_steamid'] != 'BOT' ):
		helper.TriggerStandardEvent( 'player_air', ev['userid'], ev )

def player_land( ev ):
	# is the player a bot!?
	if ( ev['es_steamid'] != 'BOT' ):
		helper.TriggerStandardEvent( 'player_land', ev['userid'], ev )

''' -------------------------------- '''
''' ----- Player Weapon Events ----- '''
''' -------------------------------- '''
def weapon_fire( ev ):
	# is the player a bot!?
	if ( ev['es_steamid'] != 'BOT' ):
		helper.TriggerStandardEvent( 'weapon_fire', ev['userid'], ev )

		# modifications for recoil, and rate of fire for the races!
		helper.RaceTools.modifyWeaponRateOfFire( ev['userid'], ev['weapon'] )
		helper.RaceTools.modifyWeaponRecoil    ( ev['userid'], ev['weapon'] )

def bullet_impact( ev ):
	# is the player a bot!?
	if ( ev['es_steamid'] != 'BOT' ):
		helper.TriggerStandardEvent( 'bullet_impact', ev['userid'], ev )

# weapon list for restrictions
allWeapons = ['knife', 'usp', 'glock', 'deagle', 'elite', 'p228','fiveseven', 'm3', 'xm1014', 'mp5navy', 'tmp', 'p90', 'mac10','ump45', 'galil', 'famas', 'ak47', 'sg552', 'm4a1', 'aug', 'scout', 'awp', 'g3sg1', 'sg550', 'm249', 'flashbang', 'smokegrenade', 'hegrenade']
def bump_weapon( args ):
	# get the userid
	userid = es.getuserid( es.gethandlefromindex( spe.getIndexOfEntity( args[1] ) ) )

	# get the wcsPlayer
	wcsPlayer = helper.players[ str(userid) ]

	# is the player not a WCS player?!
	if ( wcsPlayer.player.steamid == 'BOT' ):
		# have the function continue as normal
		return ( HookAction.Continue, 0 )

	# get the players race object
	race = helper.races.raceList[ wcsPlayer.race ]

	# get the weapon name
	weapon = spe.getEntityClassName( args[0] ) #.replace( 'weapon_', '' )

	# make sure we won't restrict c4
	if ( weapon != 'weapon_c4' ):

		# do we have a can only use list?
		if ( len( race.WeaponsCanOnlyUse ) > 0 ):
			weaponList = [ 'weapon_' + w.lower() for w in race.WeaponsCanOnlyUse ]

			if ( 'weapon_pistols' in weaponList ):
				weaponList.remove( 'weapon_pistols' )
				weaponList = weaponList + helper.RaceTools.weaponList['secondary']

			if ( 'weapon_grenades' in weaponList ):
				weaponList.remove( 'weapon_grenades' )
				weaponList = weaponList + helper.RaceTools.weaponList['grenade']

			# if its not in the list, we can't have it! D:<
			if ( not weapon in weaponList ):

				# better not let them pick it up
				return ( HookAction.Override, 0 )

		# doe we have a can't use list?
		elif ( len( race.WeaponsCantUse ) > 0 ):
			weaponList = [ 'weapon_' + w.lower() for w in race.WeaponsCantUse ]

			if ( 'weapon_pistols' in weaponList ):
				weaponList.remove( 'weapon_pistols' )
				weaponList = weaponList + helper.RaceTools.weaponList['secondary']

			if ( 'weapon_grenades' in weaponList ):
				weaponList.remove( 'weapon_grenades' )
				weaponList = weaponList + helper.RaceTools.weaponList['grenade']

			# is this weapon in it?
			if ( weapon in weaponList ):

				# cant have it D:<
				return ( HookAction.Override, 0 )

	# have the function continue as normal
	return ( HookAction.Continue, 0 )

''' ----------------------- '''
''' ----- Bomb Events ----- '''
''' ----------------------- '''
def bomb_planted( ev ):
	if ( ev['es_steamid'] != 'BOT' ):
		wcsPlayer = helper.players[ str(ev['userid']) ]

		helper.tell( wcsPlayer, '#wcs[WCS] #defYou have gained #xp%i XP #deffor planting the bomb!' % Config.BombPlant )

		wcsPlayer.roundXP += Config.BombPlant

def bomb_defused( ev ):
	if ( ev['es_steamid'] != 'BOT' ):
		wcsPlayer = helper.players[ str(ev['userid']) ]

		helper.tell( wcsPlayer, '#wcs[WCS] #defYou have gained #xp%i XP #deffor defusing the bomb!' % Config.BombDefuse )

		wcsPlayer.roundXP += Config.BombDefuse

def bomb_exploded( ev ):
	if ( ev['es_steamid'] != 'BOT' ):
		wcsPlayer = helper.players[ str(ev['userid']) ]

		helper.tell( wcsPlayer, '#wcs[WCS] #defYou have gained #xp%i XP #deffor the bomb detonating!' % Config.BombExplode )

		wcsPlayer.roundXP += Config.BombExplode
