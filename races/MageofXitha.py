from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class MageofXitha( baseRace ):
	def __init__( self ):
		self.RaceColor         = '#teal'
		self.RaceAbbreviation  = 'MgXit'

		self.RaceName          = 'Mage of Xitha'
		self.Coder             = 'Tortoise & Mini Dude'
		self.RaceTypes         = ['human', 'wizard']

		self.PlayerLimit       = 0
		self.RequiredLevel     = 10

		self.SkillList = [
			Skill( 'Weapon Summoning', 'Spawn with a deagle.'              , 8, 0 ),
			Skill( 'Mage Camouflage' , 'You become harder to see.'         , 8, 0 ),
			Skill( 'Magic Barrier'   , 'Deal damage back to your attacker.', 8, 0 ),
			Skill( 'Fire bolt'       , 'Light your enemy on fire.'         , 8, 0 )
		]

	def player_spawn( self, ev, skills ):
		# player = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Weapon Summoning']
		if ( lvl > 0 ):
			chance = lvl * 13 
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				extraAmmo = 5 * lvl
				self.RaceTools.giveWeapon( wcsPlayer, 'deagle' )
				self.RaceTools.setSecondaryClip( wcsPlayer,  7 + ( lvl * 2 ) )
				self.RaceTools.setSecondaryAmmo( wcsPlayer, 35 + ( lvl * 2 ) )

		lvl = skills['Mage Camouflage']
		if ( lvl > 0 ):
			invis = 0.2 + ( 0.05 * lvl )
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, (1 - invis) )
			self.helper.raceTell( self, wcsPlayer, '#goodMage Camouflage #defgrants you #good%i%% #definvisibility.' % int( invis * 100 ) )

		lvl = skills['Magic Barrier']
		if ( lvl > 0 ):
			chance = 20 + lvl * 3
			self.helper.raceTell( self, wcsPlayer, '#goodMagic Barrier #defgrants a #good%i%% #defchance to reflect #good25%% #defof damage back!' % chance )

		lvl = skills['Fire bolt']
		if ( lvl > 0 ):
			chance = 20 + lvl * 3
			self.helper.raceTell( self, wcsPlayer, '#goodFire bolt #defgrants a #good%i%% #defchance to #redBurn #defenemies on atttack!' % chance )

	def player_hurt( self, ev, skills ):
		wcsVictim = self.helper.players[ str(ev['userid']) ]
		
		wcsAttacker = False
		if ( str(ev['attacker']) in self.helper.players ):
			wcsAttacker = self.helper.players[ str(ev['attacker']) ]

		lvl = skills['Magic Barrier']
		if ( lvl > 0 and wcsAttacker ):
			damage = ev['dmg_health']
			chance = 20 + lvl * 3
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				mirror = int( damage * 0.25 )
				self.RaceTools.damage( wcsVictim, wcsAttacker, mirror )
				self.helper.raceTell( self, wcsAttacker, '#name%s #def hits you for #good%i #defmirror damage!' % ( wcsVictim.player.name, mirror ) )
				self.helper.raceTell( self, wcsVictim  , '#goodMagic Barrier #defhit #name%s #deffor #good%i #defdamage!' % ( wcsAttacker.player.name, mirror ) )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ]
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Fire bolt']
		if ( lvl > 0 ):
			chance = 20 + lvl * 3
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				# 4.5 seconds
				time   = 1.5 + ( 0.5 * lvl )
				# 13.5 damage
				damage = int( time * 3 )

				self.helper.raceTell( self, wcsAttacker, '#goodFire bolt #defsets #name%s on #redfire#def!' % wcsVictim.player.name )
				self.helper.raceTell( self, wcsVictim  , '#name%s #defset you on #redfire#def!' % wcsAttacker.player.name )

				self.RaceTools.DOT( wcsAttacker, wcsVictim, time, damage, self.Effects.Burn )
