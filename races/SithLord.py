from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class SithLord( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['Knife', 'Grenades']

		self.RaceColor                = '\x07333333'
		self.RaceAbbreviation         = 'Sith'

		self.RacePrefix               = '[K]'
		self.RaceName                 = 'Sith Lord'
		self.RaceTypes                = ['human','sith']
		self.Coder                    = 'Chikendinner'

		self.UltimateCooldown         = 20
		self.StartingUltimateCooldown = 10
		
		self.RequiredLevel            = 17
		self.PlayerLimit              = 2

		self.SkillList = [
			Skill( 'Lightsaber'   , 'Burn enemies with your lightsabre.'                   , 5, 0 ),
			Skill( 'Jedi Training', 'Your training lets you dodge bullets.'                , 5, 0 ),
			Skill( 'Force Jump'   , 'You jump with aid of the force.'                      , 5, 0 ),
			Skill( 'Force Choke'  , '[Ultimate] Choke your enemies and darken their minds.', 5, 5 )
		]

	# Little helper function to keep our screen darkened all the time
	def screenDarkness( self, wcsPlayer, darkLevel ):
		self.RaceTools.fadeScreen( wcsPlayer, 2, 0, 0, 0, darkLevel )

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.setColor( wcsPlayer, 0.1, 0.1, 0.1, 1 )

		# darkness for us
		self.RaceTools.Aura( wcsPlayer, 2, self.screenDarkness, 'darkness', 150 )

		lvl = skills['Lightsaber']
		if ( lvl > 0 ):
			bonusDamage = 0.1 + ( lvl * 0.05 )
			self.helper.raceTell( self, wcsPlayer, '#goodLightsaber #defgrants you #good%i%% #defbonus damage.' % int(bonusDamage*100) )

		lvl = skills['Jedi Training']
		if ( lvl > 0 ):
			chance = 25 + ( lvl * 5 )
			self.helper.raceTell( self, wcsPlayer, '#goodJedi Training #defgives you a #good%i%% #defchance to evade!' % chance )

		lvl = skills['Force Jump']
		if ( lvl > 0 ):
			grav = 0.1 + ( lvl * 0.075 )
			self.RaceTools.setGravity( wcsPlayer, 1 - grav )
			self.helper.raceTell( self, wcsPlayer, '#goodForce Jump #defgrants you #good%i%% #deflower gravity!' % round(grav*100) )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		# wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		weapon   = ev['weapon']

		lvl = skills['Lightsaber']
		if ( lvl > 0 and weapon == 'knife' ):
			damage      = ev['dmg_health']
			bonusDamage = damage * ( 0.1 + ( lvl * 0.05 ) )

			self.helper.raceTell( self, wcsAttacker, '#goodLightsaber #defdeals #good%i #defbonus damage!' % round(bonusDamage) )

			return ( damage + bonusDamage )

	def player_hurt( self, ev, skills ):
		wcsVictim = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Jedi Training']
		if ( lvl > 0 ):
			chance = 25 + ( lvl * 5 )
			rand   = randint( 1, 100 )

			if ( chance >= rand ):
				damage = ev['dmg_health']

				self.helper.raceTell( self, wcsVictim, '#goodJedi Training #defallows you to evades #good%i #defdamage!' % int(damage) )

				return 0

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Force Choke']
		if ( lvl > 0 ):
			distance = 400
			freeze   = 1 + ( lvl * 0.5 )

			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

			if ( len(targets) > 0 ):
				es.emitsound( 'player', wcsPlayer, 'wcs/nocturne_darkness.mp3', 1.0, 0.6 )
				for wcsTarget in targets:
					self.RaceTools.freezePlayer( wcsTarget, freeze )

					self.RaceTools.fadeScreen( wcsTarget, freeze, 0, 0, 0, 245 )

					self.Effects.beampoints( wcsPlayer, wcsTarget, 60, 60, 60, 255, freeze, 1, 'sprites/lgtning.vmt' )

					self.helper.raceTell( self, wcsTarget, '#name%s #defforce chokes you!' % wcsPlayer.player.name )

				self.helper.raceTell( self, wcsPlayer, '#goodForce Choke #defhits #good%i #defpeople!' % len(targets) )

				return True

			else:
				self.helper.raceTell( self, wcsPlayer, '#goodForce Choke #defno targets in range!' )

				return False
