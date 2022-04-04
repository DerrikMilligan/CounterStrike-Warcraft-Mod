from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread, usermsg
from random import randint

class Chewbacca( baseRace ):
	def __init__( self ):
		self.RaceColor                = '#brown'
		self.RaceAbbreviation         = 'Chewey'

		self.RaceName                 = 'Chewbacca'
		self.RaceTypes                = ['wookie', 'humanoid', 'monster']
		self.Coder                    = 'Chikendinner'
		self.UltimateCooldown         = 25
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 1
		self.RequiredLevel            = 10
		self.ChangeRaceIndex          = 10

		self.SkillList = [
			Skill( 'Wookie Rifleman', 'Chance to spawn with AWP.'                  , 5, 0 ),
			Skill( 'Wookie Training', 'You\'re heavy, train to move faster.'       , 5, 0 ),
			Skill( 'Wookie Fur'     , 'Reduce the impact of bullets.'              , 5, 0 ),
			Skill( 'Wookie Call'    , '[Ultimate] Growl to fear enemies in battle.', 5, 5 )
		]

	def player_spawn( self, ev, skills ):
		# player = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Wookie Rifleman']
		if ( lvl > 0 ):
			chance = lvl * 20
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				self.RaceTools.giveWeapon( wcsPlayer, 'awp' )
				self.helper.raceTell( self, wcsPlayer, '#goodWookie Rifleman #defprovies you with an #goodAWP#def.' )

		lvl = skills['Wookie Training']
		speed = 0.8 + (lvl * 0.04)
		self.RaceTools.setSpeed( wcsPlayer, speed )
		self.helper.raceTell( self, wcsPlayer, '#goodWookie Training #defsets your speed to #bad%s%%#def.' % int( speed * 100 ) )

		lvl = skills['Wookie Fur']
		if ( lvl > 0 ):
			reduction = lvl * 0.05
			self.helper.raceTell( self, wcsPlayer, '#goodWookie\'s Fur #defreduces the damage you take by #good%i%%#def!' % int( reduction * 100 ) )

	def player_hurt( self, ev, skills ):
		# player = playerlib.getPlayer( ev['userid'] )
		# wcsVictim = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Wookie Fur']
		if ( lvl > 0 ):
			damage = int( ev['dmg_health'] )
			reduction = lvl * 0.05
			return (damage * (1-reduction))

	def player_ultimate( self, ev, skills ):
		# player = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.players[ str(ev['userid']) ]


		lvl = skills['Wookie Call']
		if ( lvl > 0 ):
			magnitude = 100
			time      = lvl

			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive' # condenses 4 lines into 1. VERRY NICE, YA!
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, 700 )

			if ( len(targets) > 0 ):
				for wcsTarget in targets:
					usermsg.shake( wcsTarget, magnitude, time )
					self.helper.raceTell( self, wcsTarget, '#name%s\'s #badWookie Call #defstrikes great fear into your heart!' % player.name )
				self.helper.raceTell( self, wcsPlayer, '#goodWookie Call #defstrikes fear into the hearts of #good%i #defpeople!' % len( targets ) )
				return True
			else:
				self.helper.raceTell( self, wcsPlayer, 'No foes within range of the #goodWookie Call#def!' )
				return False
