from ..tools.BaseClasses import baseRace, Skill

import es, playerlib
from random import randint, choice

class FlamePredator( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse = ['knife', 'flashbang', 'smokegrenade', 'hegrenade']

		self.RaceColor         = '\x07CC0000'
		self.RaceAbbreviation  = 'FPred'

		self.RacePrefix        = '[K]'
		self.RaceName          = 'Flame Predator'
		self.RaceTypes         = ['humanoid', 'monster']
		self.Coder             = 'Mini Dude'

		self.PlayerLimit       = 0
		self.RequiredLevel     = 6
		self.ChangeRaceIndex   = 0

		self.SkillList = [
			Skill( 'Berserk'              , 'Pump yourself with adrenaline to gain speed and hp.', 4, 0 ),
			Skill( 'Cloak of Invisibility', 'Put on your cloak to become invisible.'             , 4, 0 ),
			Skill( 'Levitation'           , 'Reduce your gravity.'                               , 4, 0 ),
			Skill( 'Claw Attack'          , 'Force weapon drop upon hit.'                        , 4, 0 ),
			Skill( 'Burning Blade'        , 'Chance to set your enemy on fire.'                  , 4, 0 ),
			Skill( 'Burning Inferno'      , 'Chance to blow up upon death.'                      , 4, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Berserk']
		if ( lvl > 0 ):
			health = 20 + ( lvl * 5 )
			speed  = 1.1 + ( lvl * .075 )

			self.RaceTools.setHealth( wcsPlayer, 100 + health )
			self.RaceTools.setSpeed( wcsPlayer, speed )
			self.helper.raceTell( self, wcsPlayer, '#goodBerserk #defprovides #good%i #defbonus health, and #good%i%% #defbonus movement speed.' % ( health, round(speed*100) ) )

		lvl = skills['Cloak of Invisibility']
		if ( lvl > 0 ):
			invis = 0.2 + ( 0.1 * lvl )

			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, (1 - invis) )
			self.helper.raceTell( self, wcsPlayer, '#goodCloak of Invisibility #defgrants you #good%s%% #definvisibility.' % int( invis * 100 ) )

		lvl = skills['Levitation']
		if ( lvl > 0 ):
			gravity = 0.8 - ( 0.1 * lvl )

			self.RaceTools.setGravity( wcsPlayer, gravity )
			self.helper.raceTell( self, wcsPlayer, '#goodLevitation #defsets you to #good%i%% #defgravity!' % int( gravity * 100 ) )

		lvl = skills['Burning Inferno']
		if ( lvl > 0 ):
			chance = 20 + ( lvl * 10 )
			self.helper.raceTell( self, wcsPlayer, '#redBurning Inferno #defprovides you with #good%i%% #defchance to explode upon death!' % chance )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Claw Attack']
		if ( lvl > 0 ):
			chance   = lvl * 5
			rand     = randint( 1, 100 )
			if ( chance >= rand and self.RaceTools.getActiveWeapon( wcsAttacker ) != 'wepaon_knife' ):
				self.RaceTools.disarm( victim, True )
				self.helper.raceTell( self, wcsVictim  , '#name%s #defhas #baddisarmed #defyou!' % wcsAttacker.player.name )
				self.helper.raceTell( self, wcsAttacker, 'You have #gooddisarmed #name%s#def!' % wcsVictim.player.name )

		lvl = skills['Burning Blade']
		if ( lvl > 0 ):
			chance   = lvl * 10
			rand     = randint( 1, 100 )
			if ( chance >= rand ):
				time   = 1.5 + ( 0.5 * lvl )
				damage = int( time * 5 )
				self.helper.raceTell( self, wcsVictim, '#name%s #defhas set you on #redfire#def!' % wcsAttacker.player.name )
				self.helper.raceTell( self, wcsAttacker, 'You have set #name%s #defon #redfire#def.' % wcsVictim.player.name )
				self.RaceTools.DOT( wcsAttacker, wcsVictim, time, damage, self.Effects.Burn )

	def player_death( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]
		# player = playerlib.getPlayer( ev['userid'] )

		lvl = skills['Burning Inferno']
		if ( lvl > 0 ):
			chance = 20 + ( lvl * 10 )
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				damage   = 125 + (15 * lvl)
				distance = 200 + (10 * lvl)

				targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
				targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )
				
				self.Effects.Explode( wcsPlayer, distance )

				# if ( len(targets) > 0 ):
				for wcsVictim in targets:
					self.RaceTools.damage( wcsPlayer, wcsVictim, damage )
					self.helper.raceTell( self, wcsVictim, '#name%s #defdealt #bad%s #defdamage from #redBuring Inferno#def!' % ( player.name, damage ) )
