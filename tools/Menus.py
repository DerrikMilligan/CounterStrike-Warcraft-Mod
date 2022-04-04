# import es # uncomment for es.msg()
import popuplib
from Config import values as Conf

class Menus( object ):
	def __init__( self, races, items, helper ):
		self.changeRaceMenu  = ChangeRaceMenu( races, helper, self )
		self.spendSkillsMenu = SpendSkillsMenu( races, helper )
		self.raceInfoMenu    = RaceInfoMenu( races, helper, self )
		self.playerInfoMenu  = PlayerInfoMenu( races, helper, self )
		self.shopMenu        = ShopMenu( items, races, helper )

	def getListTotalPages( self, tehList ):
		listLength = len( tehList )

		pages     = listLength / 7
		remainder = listLength % 7

		if ( remainder > 0 ):
			pages += 1

		return pages

class ChangeRaceMenu( object ):
	# for hodling which page they are currently on
	playerCurrentPage = {}

	# for holding the races the player is looking at
	playerCurrentRaces = {}

	# for holding the changes to occur at round end.
	pendingChanges = {}

	def __init__( self, races, helper, menus ):
		self.helper = helper
		self.menus  = menus
		self.races  = races

	def displayChangeRaceMenu( self, userid, page=0 ):
		page = self.buildChangeRacePage( userid, page )
		popuplib.quicksend( 0, userid, page, self.changeRaceHandleSelection )

	def buildChangeRacePage( self, userid, page ):
		# grab player info
		wcsPlayer    = self.helper.players[ str(userid) ]
		playerLevels = self.helper.db.GetPlayerLevels( wcsPlayer.playerID )
		playerisSub  = self.helper.isplayerSubscriber( wcsPlayer )
		playerisPri  = self.helper.isplayerPrivateRace( wcsPlayer )
		playerisSUA  = self.helper.isplayerSuperAdmin( wcsPlayer )

		# What list are we using?
		raceList = self.races.raceListNoPrivateSorted
		if ( playerisPri or playerisSUA ):
			# list with private races included
			raceList = self.races.raceListSorted

		# store the page for later
		self.playerCurrentPage[ str(wcsPlayer) ] = page

		# get the total pages
		totalPages = self.menus.getListTotalPages( raceList )

		# Menu header info
		menu  = 'Changerace Page %i of %i\n' % ( page + 1, totalPages )
		menu += 'Total Level: %i\n' % wcsPlayer.totalLevel
		menu += 'Current Race: %s [Level %s]\n \n' % ( wcsPlayer.race, wcsPlayer.level )

		# get the starting index of races
		startingIndex = 7 * page
		# get the ending index
		endingIndex   = min( len(raceList), startingIndex+7 )

		counter = 1

		# loop through the races to display
		for i in range( startingIndex, endingIndex ):

			# grab the race Object
			race = self.races.raceList[ raceList[i][0] ]

			# grab the levels the player has for the race.
			level = 0
			if ( race.RaceName in playerLevels ):
				level = playerLevels[ race.RaceName ]

			# if the player can change to the race, change the color in the menu
			if ( self.playerCanUseRace( wcsPlayer, race, playerisSub, playerisPri, playerisSUA ) ):
				menu += '->'

			# append the index number, the race prefix if there is one, and the race Name
			if ( race.RacePrefix != '' ):
				menu += '%i. %s ' % ( counter, race.RacePrefix + ' ' + race.RaceName )
			else:
				menu += '%i. %s ' % ( counter, race.RaceName )

			# Display the players level on the race
			if ( level != 0 ):
				menu += '[Level %s]' % level

			# Display if the play is on the race
			if ( wcsPlayer.race == race.RaceName ):
				menu += '[Current]'

			# Display the required level if you can't use the race
			if ( wcsPlayer.totalLevel < race.RequiredLevel ):
				menu += '[Level %s required]' % race.RequiredLevel

			# display the subscriber tag
			if ( race.isSubscriber and not race.isPrivate ):
				menu += '[Sub]'

			# display the private Tag - Wont display
			if ( race.isPrivate ):
				menu += '[Private]'

			menu += '\n'

			counter += 1

		# save the list used, and the race choices for when an option is selected
		self.playerCurrentRaces[str(wcsPlayer)] = ( raceList, range( startingIndex, endingIndex ) )

		menu += ' \n->8. Previous\n->9. Next\n0. Exit'

		return menu

	def playerCanUseRace( self, wcsPlayer, race, playerisSub, playerisPri, playerisSUA ):
		if  (
				# the race is subscriber and the player is too, or the race isn't subscriber
				((race.isSubscriber and ( playerisSub or playerisSUA )) or race.isSubscriber == False) and
				((race.isPrivate    and ( playerisPri or playerisSUA )) or race.isPrivate    == False) and
				# the player meets the required level
				(wcsPlayer.totalLevel >= race.RequiredLevel) and
				# the player isn't already on that race.
				(wcsPlayer.race != race.RaceName)
			):
			return True
		return False

	def changeRaceHandleSelection( self, userid, choice, popupid ):
		# grab the player information
		wcsPlayer   = self.helper.players[ str(userid) ]
		playerisSub = self.helper.isplayerSubscriber ( wcsPlayer )
		playerisPri = self.helper.isplayerPrivateRace( wcsPlayer )
		playerisSUA = self.helper.isplayerSuperAdmin ( wcsPlayer )

		if ( choice > 0 and choice < 8 ):
			race = self.races.raceList[ self.playerCurrentRaces[str(wcsPlayer)][0][ self.playerCurrentRaces[str(wcsPlayer)][1][choice-1] ][0] ]

			if self.playerCanUseRace( wcsPlayer, race, playerisSub, playerisPri, playerisSUA ):
				# does the race have a player limit?
				# es.msg( 'race.PlayerLimit: %s' % race.PlayerLimit )
				if ( race.PlayerLimit != False and race.PlayerLimit != 0 ):

					# is it team dependant?
					# es.msg( 'race.LimitTeamDependant: %s' % str(race.LimitTeamDependant) )
					if ( race.LimitTeamDependant == True ):
						# count the number of players on the race who are on the same team
						numPlayersOnRace = len( [ p for p in self.helper.players if self.helper.players[p].race == race.RaceName and self.helper.players[p].player.teamid == wcsPlayer.player.teamid ] )
					else:
						# count the number of players on that race
						numPlayersOnRace = len( [ p for p in self.helper.players if self.helper.players[p].race == race.RaceName ] )
					
					# es.msg( 'numPlayersOnRace: %i' % numPlayersOnRace )

					# the number of players on the race is below the limit
					if ( numPlayersOnRace < race.PlayerLimit ):
						# the player is not dead, change his race when the round ends
						if ( not wcsPlayer.player.isdead ):
							self.pendingChanges[ str(wcsPlayer) ] = race.RaceName
							self.helper.tell( wcsPlayer, '#wcs[WCS] #defYour race will be changed to %s #defwhen the round ends.' % race.CompiledName )

						# the player is dead, change his race now
						else:
							self.helper.TriggerStandardEvent( 'pre_race_changed', wcsPlayer, { 'userid':str(wcsPlayer), 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
							self.helper.db.UpdatePlayerRace( wcsPlayer.player.steamid, race.RaceName )
							self.helper.TriggerStandardEvent( 'race_changed', wcsPlayer, { 'userid':str(wcsPlayer), 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
							self.helper.tell( wcsPlayer, '#wcs[WCS] #defYour race has been #goodchanged #defto %s#def!' % race.CompiledName )

					# there are too many players on the race
					else:
						self.helper.tell( wcsPlayer, '#wcs[WCS] #defThere are the #badmaximum #defnumber of players on %s #defalready.' % race.CompiledName )
						page = self.buildChangeRacePage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)] )
						popuplib.quicksend( 0, wcsPlayer, page, self.changeRaceHandleSelection )

				# the race does not have a playerlimit, change his race
				else:
					# the player is not dead, change his race when the round ends
					if ( not wcsPlayer.player.isdead ):
						self.pendingChanges[ str(wcsPlayer) ] = race.RaceName
						self.helper.tell( wcsPlayer, '#wcs[WCS] #defYour race will be changed to %s #defwhen the round ends.' % race.CompiledName )

					# the player is dead, change his race now
					else:
						self.helper.TriggerStandardEvent( 'pre_race_changed', wcsPlayer, { 'userid':str(wcsPlayer), 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
						self.helper.db.UpdatePlayerRace( wcsPlayer.player.steamid, race.RaceName )
						self.helper.TriggerStandardEvent( 'race_changed', wcsPlayer, { 'userid':str(wcsPlayer), 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
						self.helper.tell( wcsPlayer, '#wcs[WCS] #defYour race has been #goodchanged #defto %s#def!' % race.CompiledName )

			# if you can't use the race, resend the page
			else:
				page = self.buildChangeRacePage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)] )
				popuplib.quicksend( 0, wcsPlayer, page, self.changeRaceHandleSelection )

		# go to the previous page.
		elif ( choice == 8 ):
			# if there is a previous page
			if ( self.playerCurrentPage[str(wcsPlayer)]-1 in range( 0, self.menus.getListTotalPages( self.playerCurrentRaces[str(wcsPlayer)][0] ) ) ):
				# display it
				page = self.buildChangeRacePage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)]-1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.changeRaceHandleSelection )
			# if not, display the last page in the list, eg loop back around
			else:
				page = self.buildChangeRacePage( wcsPlayer, self.menus.getListTotalPages( self.playerCurrentRaces[str(wcsPlayer)][0] )-1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.changeRaceHandleSelection )

		elif ( choice == 9 ):
			# if there is a previous page
			if ( self.playerCurrentPage[str(wcsPlayer)]+1 in range( 0, self.menus.getListTotalPages( self.playerCurrentRaces[str(wcsPlayer)][0] ) ) ):
				# display it
				page = self.buildChangeRacePage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)]+1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.changeRaceHandleSelection )
			# if not, display the last page in the list, eg loop back around
			else:
				page = self.buildChangeRacePage( wcsPlayer, 0 )
				popuplib.quicksend( 0, wcsPlayer, page, self.changeRaceHandleSelection )

	def handePendingChanges( self ):
		for userid in self.pendingChanges:
			if ( str(userid) in self.helper.players ):
				wcsPlayer = self.helper.getPlayer( userid )
				race      = self.races.raceList[ self.pendingChanges[userid] ]

				self.helper.TriggerStandardEvent( 'pre_race_changed', wcsPlayer, { 'userid':str(wcsPlayer), 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )
				self.helper.db.UpdatePlayerRace( wcsPlayer.player.steamid, race.RaceName )
				wcsPlayer.refresh()
				self.helper.TriggerStandardEvent( 'race_changed', wcsPlayer, { 'userid':str(wcsPlayer), 'last_race':wcsPlayer.race, 'new_race':race.RaceName } )

				self.helper.tell( wcsPlayer, '#wcs[WCS] #defYour race has been set to %s#def!' % race.CompiledName )

		self.pendingChanges = {}

class SpendSkillsMenu( object ):
	def __init__( self, races, helper ):
		self.races  = races
		self.helper = helper

	def displaySpendSkillsMenu( self, userid ):
		page = self.buildSpendSkillsmenu( userid )
		popuplib.quicksend( 0, userid, page, self.spendSkillsHandleSelection )

	def buildSpendSkillsmenu( self, userid ):
		# load information
		wcsPlayer   = self.helper.players[ str(userid) ]
		race        = self.races.raceList[ wcsPlayer.race ]
		totalPoints = sum( [ skill.Levels for skill in race.SkillList ] ) # self.races.getRaceNumSkillPoints( race )
		spentPoints = sum( wcsPlayer.skillPoints )

		# build the menu
		menu  = 'Spend Skills for: %s\n' % race.RaceName
		menu += 'Current Level: %i/%i\n' % ( wcsPlayer.level, totalPoints )
		if ( wcsPlayer.level > totalPoints ):
			level = totalPoints
		else:
			level = wcsPlayer.level
		menu += 'Unused Points: %i\n \n' % ( level - spentPoints )
		
		i = 1
		# loop through all the races skills
		for skill in race.SkillList:
			# does the skill have a leve req? eg: Human ult needs 8 levels to level it
			if ( spentPoints >= skill.RequiredLevel ):
				# is the skill not passive?
				if ( skill.Levels > 0 ):
					# is teh skill maxed already?
					if ( ( level - spentPoints ) > 0 and wcsPlayer.skillPoints[ i - 1 ] < skill.Levels ):
						# display selectable
						menu += '->%i. %s [%i/%i]\n' % ( i, skill.Name, wcsPlayer.skillPoints[ i - 1 ], skill.Levels )
					else:
						# display unselectable
						menu += '%i. %s [%i/%i]\n' % ( i, skill.Name, wcsPlayer.skillPoints[ i - 1 ],  skill.Levels )
				else:
					# display passive
					menu += '%i. %s [Passive]\n' % ( i, skill.Name )
			else:
				# display unselectable and show level requirement
				menu += '%i. %s [Requires Skill Level %i]\n' % ( i, skill.Name, skill.RequiredLevel )
			i += 1
		
		menu += ' \n0. Exit'
		return menu

	def spendSkillsHandleSelection( self, userid, choice, popupid ):
		wcsPlayer   = self.helper.players[ str(userid) ]
		race        = self.races.raceList[ wcsPlayer.race ]
		spentPoints = sum(wcsPlayer.skillPoints)
		unusedPoints = wcsPlayer.level - spentPoints

		if ( choice > 0 and choice < 10 ):
			choice -= 1
			if  (
					# you have points to spend
					( unusedPoints > 0 ) and
					# the choice lies within the number of skills the race has
					( choice < len(race.SkillList) ) and
					# you meet the skills required level
					( spentPoints >= race.SkillList[ choice ].RequiredLevel ) and
					# the skill isn't maxed already
					( wcsPlayer.skillPoints[ choice ] < race.SkillList[ choice ].Levels )
				):
				# Update the player skillPoints
				wcsPlayer.skillPoints[ choice ] += 1
				# Save the player
				wcsPlayer.save()
				# resend the menu until the player presses 0
				self.displaySpendSkillsMenu( wcsPlayer )
			else:
				# resend the menu
				self.displaySpendSkillsMenu( wcsPlayer )

class RaceInfoMenu( object ):
	# for hodling which page they are currently on
	playerCurrentPage = {}

	# for holding the races the player is looking at
	playerCurrentRaces = {}

	# for hodling the race (singular) the player is looking at
	playerCurrentRace = {}

	def __init__( self, races, helper, menus ):
		self.races  = races
		self.helper = helper
		self.menus  = menus

	def displayRaceInfoMenu( self, userid, race=None, page=0 ):
		if ( race != None ):
			page = self.buildRaceInfoMenuRace( userid, race )
			popuplib.quicksend( 0, userid, page, self.RaceInfoMenuRaceHandleSelection )
		else:
			page = self.buildRaceInfoMenuPage( userid, page )
			popuplib.quicksend( 0, userid, page, self.RaceInfoMenuPageHandleSelection )

	def buildRaceInfoMenuPage( self, userid, page ):
		# grab player info
		wcsPlayer    = self.helper.players[ str(userid) ]
		playerLevels = self.helper.db.GetPlayerLevels( wcsPlayer.playerID )
		playerisSub  = self.helper.isplayerSubscriber( wcsPlayer )
		playerisPri  = self.helper.isplayerPrivateRace( wcsPlayer )
		playerisSUA  = self.helper.isplayerSuperAdmin( wcsPlayer )

		# What list are we using?
		raceList = self.races.raceListNoPrivateSorted
		if ( playerisPri or playerisSUA ):
			# list with private races included
			raceList = self.races.raceListSorted

		# store the page for later
		self.playerCurrentPage[ str(wcsPlayer) ] = page

		# get the total pages
		totalPages = self.menus.getListTotalPages( raceList )

		# Menu header info
		menu  = 'Raceinfo Page %i of %i\n' % ( page + 1, totalPages )
		menu += 'Select a race to view its skills\n'
		menu += 'Current Race: %s [Level %s]\n \n' % ( wcsPlayer.race, wcsPlayer.level )

		# get the starting index of races
		startingIndex = 7 * page
		# get the ending index
		endingIndex   = min( len(raceList), startingIndex+7 )

		counter = 1

		# loop through the races to display
		for i in range( startingIndex, endingIndex ):
			# grab the race Object
			race = self.races.raceList[ raceList[i][0] ]

			# grab the levels the player has for the race.
			level = 0
			if ( race.RaceName in playerLevels ):
				level = playerLevels[ race.RaceName ]

			# append the index number, the race prefix if there is one, and the race Name
			if ( race.RacePrefix != '' ):
				menu += '->%i. %s ' % ( counter, race.RacePrefix + ' ' + race.RaceName )
			else:
				menu += '->%i. %s ' % ( counter, race.RaceName )

			# Display the players level on the race
			if ( level != 0 ):
				menu += '[Level %s]' % level

			# Display if the play is on the race
			if ( wcsPlayer.race == race.RaceName ):
				menu += '[Current]'

			# display the subscriber tag
			if ( race.isSubscriber and not race.isPrivate ):
				menu += '[Sub]'

			# display the private Tag - Wont display
			if ( race.isPrivate ):
				menu += '[Private]'

			menu += '\n'
			counter += 1

		# save the list used, and the race choices for when an option is selected
		self.playerCurrentRaces[str(wcsPlayer)] = ( raceList, range( startingIndex, endingIndex ) )

		menu += ' \n8. Previous\n9. Next\n0. Exit'

		return menu

	def RaceInfoMenuPageHandleSelection( self, userid, choice, popupid ):
		# grab the player information
		wcsPlayer = self.helper.players[ str(userid) ]

		if ( choice > 0 and choice < 8 ):
			# grab the choice information
			raceList    = self.playerCurrentRaces[ str(wcsPlayer) ][0]
			raceIndexes = self.playerCurrentRaces[ str(wcsPlayer) ][1]

			if ( (choice-1) < len(raceIndexes) ):
				raceChoice  = raceList[ raceIndexes[ choice-1 ] ][0] # index 0 for the RaceName
				race        = self.races.raceList[ raceChoice ]

				# display the raceinfo for that race
				self.displayRaceInfoMenu( userid, race.RaceName )

			else:
				page = self.buildRaceInfoMenuPage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)] )
				popuplib.quicksend( 0, wcsPlayer, page, self.RaceInfoMenuPageHandleSelection )


		# go to the previous page.
		elif ( choice == 8 ):
			# if there is a previous page
			if ( self.playerCurrentPage[str(wcsPlayer)]-1 in range( 0, self.menus.getListTotalPages( self.playerCurrentRaces[str(wcsPlayer)][0] ) ) ):
				# display it
				page = self.buildRaceInfoMenuPage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)]-1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.RaceInfoMenuPageHandleSelection )
			# if not, display the last page in the list, eg loop back around
			else:
				page = self.buildRaceInfoMenuPage( wcsPlayer, self.menus.getListTotalPages( self.playerCurrentRaces[str(wcsPlayer)][0] )-1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.RaceInfoMenuPageHandleSelection )

		elif ( choice == 9 ):
			# if there is a previous page
			if ( self.playerCurrentPage[str(wcsPlayer)]+1 in range( 0, self.menus.getListTotalPages( self.playerCurrentRaces[str(wcsPlayer)][0] ) ) ):
				# display it
				page = self.buildRaceInfoMenuPage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)]+1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.RaceInfoMenuPageHandleSelection )
			# if not, display the last page in the list, eg loop back around
			else:
				page = self.buildRaceInfoMenuPage( wcsPlayer, 0 )
				popuplib.quicksend( 0, wcsPlayer, page, self.RaceInfoMenuPageHandleSelection )

	def buildRaceInfoMenuRace( self, userid, raceName, skillNumber=1 ):
		# grab the player information
		wcsPlayer = self.helper.players[ str(userid) ]
		race      = self.races.raceList[ raceName ]

		lvl       = self.helper.db.GetPlayerLevel( wcsPlayer.playerID, race.RaceName )
		# fix level
		if lvl == -1: lvl = 0
		numPoints = self.races.getRaceNumSkillPoints( race )

		menu  = 'Race %s:\n' % race.RaceName
		menu += 'Current Level: %i/%i\n' % ( lvl, numPoints )
		menu += 'WCS Coder: Mini Dude\n'
		menu += 'Race Coder: %s\n \n' % ( race.Coder )
		menu += 'Select a skill to view its description.\n \n'

		i = 1
		# loop through all the skills
		for skill in race.SkillList:
			if ( skill.Levels > 0 ):
				# append the skill name
				menu += '->%i. %s [%i Levels]:\n' % ( i, skill.Name, skill.Levels )
			else:
				# append passive tag
				menu += '->%i. %s [Passive]:\n' % ( i, skill.Name )

			# if its the skill you're viewing, display its levels, and description
			if ( skillNumber == i ):
				menu += '   %s\n' % skill.Description
			i += 1

		# store the race for later.
		self.playerCurrentRace[ str(wcsPlayer) ] = race.RaceName

		if ( str(userid) in self.playerCurrentPage ):
			menu += ' \n0. Back'
		else:
			menu += ' \n0. Exit'

		return menu

	def RaceInfoMenuRaceHandleSelection( self, userid, choice, popupid ):
		# grab the player information
		wcsPlayer = self.helper.players[ str(userid) ]

		if ( choice > 0 and choice < 10 ):
			# grab the race
			race = self.races.raceList[ self.playerCurrentRace[str(wcsPlayer)] ]

			page = self.buildRaceInfoMenuRace( wcsPlayer, race.RaceName, choice )
			popuplib.quicksend( 0, wcsPlayer, page, self.RaceInfoMenuRaceHandleSelection )
		else:
			if ( str(wcsPlayer) in self.playerCurrentPage ):
				page = self.buildRaceInfoMenuPage( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)] )
				popuplib.quicksend( 0, wcsPlayer, page, self.RaceInfoMenuPageHandleSelection )

class PlayerInfoMenu( object ):
	# page that the player is viewing
	playerCurrentPage = {}
	# list that the player is viewing
	playerList = {}
	# which player they are viewing
	playerTarget = {}
	def __init__( self, races, helper, menus ):
		self.races  = races
		self.helper = helper
		self.menus  = menus

	def displayPlayerInfoMenu( self, userid, player=None, page=0 ):
		if ( player == None ):
			page = self.buildPlayerInfoMenu( userid )
			popuplib.quicksend( 0, userid, page, self.PlayerInfoHandleSelection )
		else:
			page = self.buildPlayerInfoPlayerMenu( userid, player )
			popuplib.quicksend( 0, userid, page, self.PlayerInfoPlayerHandleSelection )

	def buildPlayerInfoMenu( self, userid, page=0 ):
		# grab all player objects of players who aren't bots
		players = [ self.helper.players[p] for p in self.helper.players if self.helper.players[p].player.steamid != 'BOT' ]

		# the range from the list to use.
		low  =  page    * 7
		high = (page+1) * 7

		pages = self.menus.getListTotalPages( players )

		self.playerCurrentPage[str(userid)] = page

		# counter for the list items
		counter = 1

		menu  = 'Playerinfo Page %i of %i\n' % ( page + 1, pages )
		menu += 'Select player for information:\n \n'

		# loop through players for that page
		for wcsPlayer in players[ low : high ]:
			# grab the race object
			race = self.races.raceList[ wcsPlayer.race ]

			# append the player and race name
			menu += '->%i. %s - %s [Level %i] ' % ( counter, wcsPlayer.player.name, race.RaceName, wcsPlayer.level )

			# add Subscriber if its a sub race
			if ( race.isSubscriber and not race.isPrivate ):
				menu += '[Sub]'

			# add Private if its a private race
			if ( race.isPrivate ):
				menu += '[Private]'

			menu += '\n'

			counter += 1

		self.playerList[str(userid)] = players[ low : high ]

		menu += '\n \n8. Previous\n9. Next\n0. Exit'

		return menu

	def PlayerInfoHandleSelection( self, userid, choice, popupid ):
		# grab the player information
		wcsPlayer = self.helper.players[ str(userid) ]

		if ( choice > 0 and choice < 8 ):
			try:
				# grab the race
				wcsTarget = self.playerList[ str(wcsPlayer) ][ choice-1 ]

				# display the raceinfo for that race
				page = self.buildPlayerInfoPlayerMenu( wcsPlayer, wcsTarget )
				popuplib.quicksend( 0, wcsPlayer, page, self.PlayerInfoPlayerHandleSelection )
			except Exception, e:
				page = self.buildPlayerInfoMenu( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)] )
				popuplib.quicksend( 0, wcsPlayer, page, self.PlayerInfoHandleSelection )

		# go to the previous page.
		elif ( choice == 8 ):
			# if there is a previous page
			if ( self.playerCurrentPage[str(wcsPlayer)]-1 in range( 0, self.menus.getListTotalPages( self.playerList[ str(wcsPlayer) ] ) ) ):
				# display it
				page = self.buildPlayerInfoMenu( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)]-1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.PlayerInfoHandleSelection )
			# if not, display the last page in the list, eg loop back around
			else:
				page = self.buildPlayerInfoMenu( wcsPlayer, self.menus.getListTotalPages( self.playerList[ str(wcsPlayer) ] )-1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.PlayerInfoHandleSelection )

		elif ( choice == 9 ):
			# if there is a previous page
			if ( self.playerCurrentPage[str(wcsPlayer)]+1 in range( 0, self.menus.getListTotalPages( self.playerList[ str(wcsPlayer) ] ) ) ):
				# display it
				page = self.buildPlayerInfoMenu( wcsPlayer, self.playerCurrentPage[str(wcsPlayer)]+1 )
				popuplib.quicksend( 0, wcsPlayer, page, self.PlayerInfoHandleSelection )
			# if not, display the last page in the list, eg loop back around
			else:
				page = self.buildPlayerInfoMenu( wcsPlayer, 0 )
				popuplib.quicksend( 0, wcsPlayer, page, self.PlayerInfoHandleSelection )

	def buildPlayerInfoPlayerMenu( self, userid, target ):
		# load player info
		wcsPlayer = self.helper.players[ str(target) ]
		race      = self.races.raceList[wcsPlayer.race]

		# header Info
		menu  = '%s - %s\n%s [%i/%i]\n \n' % ( wcsPlayer.player.name, wcsPlayer.totalLevel, wcsPlayer.race, wcsPlayer.level, self.races.getRaceNumSkillPoints( race ) )

		# player information
		menu += 'Starting Health: %i\n' % wcsPlayer.starthealth
		menu += 'Visibility: %s\n'      % wcsPlayer.invis
		menu += 'Movement: %s\n'        % wcsPlayer.movespeed
		menu += 'Gravity: %s\n \n'      % wcsPlayer.gravity

		# items the player has
		menu += 'Items: '

		if ( len( wcsPlayer.items ) > 0 ):
			counter = 1
			# loop through items
			for item in wcsPlayer.items:
				# every 5 items, start a new line
				if ( (counter % 5) == 0 ):
					menu += '\n     '
				menu += '%s, ' % item
				counter += 1

			# remove the last comma
			menu = menu[:-2]
		else:
			menu += 'None'

		menu += '\n \n'

		counter = 1

		# loop through the skills
		for skill in race.SkillList:
			if ( skill.Levels > 0 ):
				menu += '->%i. %s [%i/%i]\n' % ( counter, skill.Name, wcsPlayer.skillPoints[ counter - 1 ], skill.Levels )
			else:
				menu += '->%i. %s [Passive]\n' % ( counter, skill.Name )
			counter += 1

		self.playerTarget[str(userid)] = target

		if ( str(userid) in self.playerCurrentPage ):
			menu += ' \n0. Back'
		else:
			menu += ' \n0. Exit'

		return menu

	def PlayerInfoPlayerHandleSelection( self, userid, choice, popupid ):
		if ( choice != 10 ):
			page = self.buildPlayerInfoPlayerMenu( userid, self.playerTarget[str(userid)] )
			popuplib.quicksend( 0, userid, page, self.PlayerInfoPlayerHandleSelection )
		else:
			if ( str(userid) in self.playerCurrentPage ):
				page = self.buildPlayerInfoMenu( userid, self.playerCurrentPage[str(userid)] )
				popuplib.quicksend( 0, userid, page, self.PlayerInfoHandleSelection )

class ShopMenu( object ):
	# hold the list of categories in order
	categoryList = []

	# item list for each category
	itemList = {}

	# holds the players category they're viewing
	playerCategory = {}

	def __init__( self, items, races, helper ):
		self.items  = items
		self.races  = races
		self.helper = helper
		self.categoryList = [ category for category in self.items.itemList ]
		# setup the item List so that it can be accesed by index
		for category in self.items.itemList:
			self.itemList[category] = [ self.items.itemList[category][item] for item in self.items.itemList[category] ]

	def displayShopMenu( self, userid, category=None ):
		if ( category == None ):
			page = self.buildShopMenuPage( userid )
			popuplib.quicksend( 0, userid, page, self.ShopMenuHandleSelection )
		else:
			page = self.buildShopMenuCategoryPage( userid, category )
			popuplib.quicksend( 0, userid, page, self.ShopMenuCategoryHandleSelection )

	def buildShopMenuPage( self, userid ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# header info
		menu  = 'Welcome to the shopmenu!\n'
		menu += 'Items are lost when you die!\n'
		menu += 'Select an item Category!\n \n'

		counter = 1

		for categoryName in self.categoryList:

			if ( Conf.ItemCatLimits[categoryName] != None ):
				menu += '->%i. %s [%s/%s]\n' % ( counter, categoryName, self.getPlayerNumItemsInCategory( wcsPlayer, categoryName ), Conf.ItemCatLimits[categoryName] )
			else:
				menu += '->%i. %s [Unlimited]\n' % ( counter, categoryName )

			counter += 1

		menu += '\n \n0. Exit'

		return menu

	def ShopMenuHandleSelection( self, userid, choice, popupid ):
		wcsPlayer = self.helper.players[ str(userid) ]

		if ( choice > 0 and choice < 10 ):
			choice -= 1

			# if there is a category for your choice
			if ( len( self.categoryList )-1 >= choice ):
				# display the menu for that category
				self.displayShopMenu( userid, self.categoryList[choice] )

				# store the category that the player was looking at
				self.playerCategory[str(wcsPlayer)] = self.categoryList[choice]

			# re-display the menu
			else:
				self.displayShopMenu( userid )

	def buildShopMenuCategoryPage( self, userid, category ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# header info
		menu  = 'Shopmenu - %s\n' % category
		menu += 'Select an item to purchase it.\n \n'

		counter = 1

		# loop through all items in the selected category
		for item in self.itemList[ category ]:
			# don't buy it if you already have one
			if ( item.Name in wcsPlayer.items ):
				menu += '->%i. [Own] [$%i] %s\n   - %s\n' % ( counter, item.Price, item.Name, item.Description )
			else:
				menu += '->%i. [$%i] %s\n   - %s\n' % ( counter, item.Price, item.Name, item.Description )

			counter += 1

		menu += '\n \n0. Back'

		return menu

	def ShopMenuCategoryHandleSelection( self, userid, choice, popupid ):
		wcsPlayer = self.helper.players[ str(userid) ]

		if ( choice > 0 and choice < 10 ):
			choice -= 1

			# if there is the item you chose in your category
			if ( len( self.itemList[ self.playerCategory[str(wcsPlayer)] ] )-1 >= choice ):
				item = self.itemList[ self.playerCategory[str(wcsPlayer)] ][ choice ]

				# try to buy the item
				if ( not self.AttemptToPurchaseItem( wcsPlayer, self.playerCategory[str(wcsPlayer)], item ) ):
					# you failed to buy the item, re-display the menu
					self.displayShopMenu( wcsPlayer, self.playerCategory[str(wcsPlayer)] )

			# re-display the menu
			else:
				self.displayShopMenu( wcsPlayer, self.playerCategory[str(wcsPlayer)] )

		# return to the category page
		else:
			self.displayShopMenu( wcsPlayer )

	def AttemptToPurchaseItem( self, userid, category, item ):
		wcsPlayer = self.helper.players[ str(userid) ]
		race      = self.races.raceList[ wcsPlayer.race ]

		# is the item restricted on that race?
		if ( not item.Name in [i.lower() for i in race.ItemsCantUse] ):

			# do you already own the item?
			if ( not item.Name in wcsPlayer.items ):

				# Have you already met the limit of items you can have in that category?
				if  ( 
						(Conf.ItemCatLimits[category] == None) or
						(self.getPlayerNumItemsInCategory( wcsPlayer, category ) < Conf.ItemCatLimits[category])
					):
					# do you have enough money to buy the item?
					if ( wcsPlayer.player.cash >= item.Price ):

						# bye bye money :[
						wcsPlayer.player.cash -= item.Price

						# is it an item you carry 'til you die?
						if ( item.Persistent ):
							# add it to the players item list!
							wcsPlayer.items.append( item.Name )

						# tell them that they bought the item!
						self.helper.tell( wcsPlayer, '#wcs[WCS] #defPurchased #race%s#def!' % item.Name )

						# trigger the item_purchase event, probably only used for tomes.
						self.helper.TriggerItemEvent( 'item_purchase', wcsPlayer, { 'userid': str(wcsPlayer) }, item.Name )

						return True

					else:
						# not enough monehz
						self.helper.tell( wcsPlayer, '#wcs[WCS] #defYou #baddon\'t #defhave enough #goodmoney #defto buy #race%s#def!' % item.Name )
				else:
					# already have the max items in that category
					self.helper.tell( wcsPlayer, '#wcs[WCS] #defYou already own the #badmaximum #defnumber of items from the #race%s #defcategory!' % category )
			else:
				# you already have the item
				self.helper.tell( wcsPlayer, '#wcs[WCS] #defYou already own #race%s#def!' % item.Name )
		else:
			# Item is restricted on this race
			self.helper.tell( wcsPlayer, '#wcs[WCS] #race%s #defis restricted when playing %s#def!' % ( item.Name, race.CompiledName ) )

		return False

	def getPlayerNumItemsInCategory( self, userid, category ):
		wcsPlayer = self.helper.players[ str(userid) ]

		# List comprehension like a baws!
		return len( [ i for i in self.itemList[category] if i.Name in wcsPlayer.items ] )

	def getItemCategory( self, itemName ):
		# loop through the categories
		for category in self.items.itemList:
			# loop through the item names
			for item in self.items.itemList[category]:
				# is it the item we're looking for?
				if ( item == itemName ):
					return category