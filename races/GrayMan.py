from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class GrayMan( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse = ['Mac10', 'P228', 'Knife', 'Grenades']

		self.RaceColor         = '#gray'
		self.RaceAbbreviation  = 'GayMan'

		self.RaceName          = 'Gray Man'
		self.RaceTypes         = 'human'
		self.Coder             = 'Tortoise'

		self.PlayerLimit       = 2
		self.RequiredLevel     = 8

		self.SkillList = [
			Skill( 'Stamina'         , 'Gain more health.'                   , 25, 0 ),
			Skill( 'Dark Boots'      , 'These boots grant you godlike speed.', 25, 0 ),
			Skill( 'Parasitic Weapon', 'Your weapon deals more damage.'      , 25, 0 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.giveWeapon( wcsPlayer, 'mac10' )
		self.RaceTools.giveWeapon( wcsPlayer, 'p228' )
		self.RaceTools.setColor( wcsPlayer, 0.42, 0.42, 0.42, 1 )

		lvl = skills['Stamina']
		if ( lvl > 0 ):
			health = lvl * 2
			self.RaceTools.setHealth( wcsPlayer, 100 + health )
			self.helper.raceTell( self, wcsPlayer, '#goodStamina #defprovides you with #good%i #defbonus health!' % health )

		lvl = skills['Dark Boots']
		if ( lvl > 0 ):
			speed = lvl * 0.02
			self.RaceTools.setSpeed( wcsPlayer, 1 + speed )
			self.helper.raceTell( self, wcsPlayer, '#goodDark Boots #defgrants you #good%i%% #defincreased speed!' % int(speed * 100) )

		lvl = skills['Parasitic Weapon']
		if ( lvl > 0 ):
			self.RaceTools.setPrimaryClip( wcsPlayer,  30 + ( lvl * 2 ) )
			self.RaceTools.setPrimaryAmmo( wcsPlayer, 100 + ( lvl * 2 ) )

			self.helper.raceTell( self, wcsPlayer, '#goodParasitic Weapon #defgives you a #good25%% #defchance to do #good%i #defbonus damage on attack!' % lvl )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Parasitic Weapon']
		if ( lvl > 0 ):
			weapon = ev['weapon']
			chance = 25
			rand   = randint( 1, 100 )
			if ( weapon == 'weapon_mac10' and chance >= rand ):
				damage = ev['dmg_health']

				self.helper.raceTell( self, wcsVictim  , '#name%s #defhits you for #bad%i #defbonus damage with #badParasitic Weapon#def!' % ( wcsAttacker.player.name, lvl) )
				self.helper.raceTell( self, wcsAttacker, '#goodParasitic Weapon #defdeals #good%i #defbonus damage to #good%s#def.' % ( lvl, wcsVictim.player.name ) )

				return ( damage + lvl )
