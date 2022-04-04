from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class UndeadScourge ( baseRace ):
	def __init__( self ):
		self.RaceAbbreviation  = 'Undead'

		self.RaceName          = 'Undead Scourge'
		self.RaceTypes         = ['undead']
		self.Coder             = 'Tortoise'

		self.PlayerLimit       = 0
		self.RequiredLevel     = 0
		self.ChangeRaceIndex   = 9

		self.SkillList = [
			Skill( 'Vampiric Aura' , 'Gives you a chance to gain damage you do in attack back as health.'           , 8, 0 ),
			Skill( 'Unholy Aura'   , 'Gives you a speed boost.'                                                     , 8, 0 ),
			Skill( 'Levitation'    , 'Allows you to jump higher by reducing your gravity.'                          , 8, 0 ),
			Skill( 'Suicide Bomber', 'On death, you have a chance to explode and do damage on each player in range.', 8, 0 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Vampiric Aura']
		if ( lvl > 0 ):
			chance =   10 + ( lvl *   2 ) # 26%
			vamp   = 0.26 + ( lvl * .03 ) # 50%
			self.helper.raceTell( self, wcsPlayer, '#goodVampiric Aura #defgrants you a #good%i%% #defchance to leech #good%i%% #defhealth back!' % ( chance, round(vamp*100) ) )

		lvl = skills['Unholy Aura']
		if ( lvl > 0 ):
			speed = .2 + ( lvl * .04 ) # 52%

			self.RaceTools.setSpeed( wcsPlayer, (1+speed) )
			self.helper.raceTell( self, wcsPlayer, '#goodUnholy Aura #defgrants you #good%i%% #defbonus movement speed!' % round(speed*100) )

		lvl = skills['Levitation']
		if ( lvl > 0 ):
			grav = 0.7 - ( lvl * .04 ) # 38%

			self.RaceTools.setGravity( wcsPlayer, grav )
			self.helper.raceTell( self, wcsPlayer, '#goodLevitation #defgrants you #good%i%% #defgravity!' % round(100*grav) )

		lvl = skills['Suicide Bomber']
		if ( lvl > 0 ):
			chance = 40 + ( lvl * 5 )

			self.helper.raceTell( self, wcsPlayer, '#goodSuicide Bomber #defgives you a #good%i%% #defchance when you die to explode!' % chance )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ]
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Vampiric Aura']
		if ( lvl > 0 ):
			chance = 10 + ( lvl * 2 ) # 26%
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				damage = ev['dmg_health']
				vamp   = damage * (0.26 + ( lvl * .03 )) # 50%

				if ( wcsAttacker.player.health < 250 ):
					wcsAttacker.player.health += vamp
					self.helper.raceTell( self, wcsAttacker, '#goodVampiric Aura #defstole #good%i #defhp from #name%s#def!' % ( round(vamp), wcsVictim.player.name ) )

	def player_death( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Suicide Bomber']
		if ( lvl > 0 ):

			chance = 40 + ( lvl * 5 )
			rand   = randint( 1, 100 )
			if ( chance >= rand ):

				damage   = 125 + ( lvl * 15 )
				distance = 200 + ( lvl * 15 )

				targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
				targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

				self.Effects.Explode( wcsPlayer, distance )

				for wcsTarget in targets:

					self.RaceTools.damage( wcsPlayer, wcsTarget, damage )
					self.helper.raceTell( self, wcsTarget, '#name%s #defexploded, dealing #bad%i #defdamage to you!' % ( wcsPlayer.player.name, damage ) )

				if ( len(targets) > 0 ):
					self.helper.raceTell( self, wcsPlayer, '#goodSuicide Bomber #defYou exploded, and hit #good%i #defpeople!' % len(targets) )
