from ..tools.BaseClasses import baseRace, Skill

import es, playerlib
from random import randint

class Corporal( baseRace ):
	def __init__( self ):
		# self.RaceColor                = '#race' # Default color anyways
		self.RaceAbbreviation         = 'Corp'

		self.RaceName                 = 'Corporal'
		self.RaceTypes                = ['human', 'soilder']
		self.Coder                    = 'MrCoolness & Mini Dude'
		self.UltimateCooldown         = 25
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 0
		self.RequiredLevel            = 2
		self.ChangeRaceIndex          = 90

		self.SkillList = [
			Skill( 'Liberation', 'Chance to spawn with a MP5.'                                 , 6, 0 ),
			Skill( 'Body Armor', 'Put on a suit of armor.'                                     , 6, 0 ),
			Skill( 'Light Load', 'Your physique is excellent. Your equipment feels weightless.', 6, 0 ),
			Skill( 'Med-Kit'   , '[Ultimate] Restore your health.'                             , 6, 0 )
		]

	def player_spawn( self, ev, skills ):
		# player = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Liberation']
		if ( lvl > 0 ):
			chance = 10 + lvl*15
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				self.RaceTools.giveWeapon( wcsPlayer, 'mp5navy' )
				self.helper.raceTell( self, wcsPlayer, '#goodLiberation #defprovides you with a #goodMP5#def.' )

		lvl = skills['Body Armor']
		if ( lvl > 0 ):
			bonusarmor    = lvl * 30
			bonushealth   = lvl * 5
			self.RaceTools.setHealth( wcsPlayer, 100 + bonushealth )
			wcsPlayer.player.armor  = 100 + bonusarmor
			self.helper.raceTell( self, wcsPlayer, '#goodBody Armor #defgrants you #good%i #defbonus health, and #good%i #defbonus armor!' % ( bonushealth, bonusarmor ) )

		lvl = skills['Light Load']
		if ( lvl > 0 ):
			grav  = 1 - ( lvl * 0.05 )
			speed = 1 + ( lvl * 0.05 )
			self.RaceTools.setSpeed( wcsPlayer, speed )
			self.RaceTools.setGravity( wcsPlayer, grav )
			self.helper.raceTell( self, wcsPlayer, '#goodLight Load #defgrants you #good%i%% #deflower #goodgravity #defand increased #goodspeed#def!' % int ( lvl * 5 ) )

	def player_ultimate( self, ev, skills ):
		# player = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Med-Kit']
		if ( lvl > 0 ):
			medKitHP = lvl * 5

			if ( wcsPlayer.player.health + medKitHP < 250 ):
				self.helper.raceTell( self, wcsPlayer, 'You heal yourself for #good%i HP #defwith your #goodMed-Kit#def.' % int( medKitHP ) )
				wcsPlayer.player.health += medKitHP
			else:
				self.helper.raceTell( self, wcsPlayer, 'You heal yourself for #good%i HP (MAX) #defwith your #goodMed-Kit#def.' % int( 250 - player.health ) )
				wcsPlayer.player.health = 250

			return True
