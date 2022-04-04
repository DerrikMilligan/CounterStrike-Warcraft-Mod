from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class NightElf( baseRace ):
	def __init__( self ):
		self.RaceAbbreviation         = 'Elf'

		self.RaceName                 = 'Night Elf'
		self.RaceTypes                = ['elf', 'humanoid']
		self.Coder                    = 'Mini Dude'
		self.UltimateCooldown         = 25
		self.StartingUltimateCooldown = 10

		self.PlayerLimit              = 0
		self.RequiredLevel            = 0
		self.ChangeRaceIndex          = 30

		self.SkillList = [
			Skill( 'Evasion'         , 'Gives you a chance of evading a shot.'                                 , 8, 0 ),
			Skill( 'Thorns Aura'     , 'Deals damage back when you get hurt.'                                  , 8, 0 ),
			Skill( 'Trueshot Aura'   , 'Deal extra damage.'                                                    , 8, 0 ),
			Skill( 'Entangling Roots', '[Ultimate] Every enemy in range will become immobile for a short time.', 8, 8 )
		]
	
	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Evasion']
		if ( lvl > 0 ):
			# 32%
			chance = 16 + lvl * 2
			self.helper.raceTell( self, wcsPlayer, '#goodEvasion #defgives you a #good%i%% #defchance to evade damage!' % chance )

		lvl = skills['Thorns Aura']
		if ( lvl > 0 ):
			# 40%
			chance = 24 + lvl * 2
			self.helper.raceTell( self, wcsPlayer, '#goodThorns Aura #defgives you a #good%i%% #defchance mirror #good50%% #defdamage back to your attacker!' % chance )

		lvl = skills['Trueshot Aura']
		if ( lvl > 0 ):
			# 32%
			chance = 16 + lvl * 2
			self.helper.raceTell( self, wcsPlayer, '#goodTrueshot Aura #defgives you a #good%i%% #defchance mirror #good20%% #defbonus damage!' % chance )

	def player_hurt( self, ev, skills ):
		wcsVictim = self.helper.players[ str(ev['userid']) ]

		wcsAttacker = False
		if ( str(ev['attacker']) in self.helper.players ):
			wcsAttacker = self.helper.players[ str(ev['attacker']) ]

		lvl = skills['Thorns Aura']
		if ( lvl > 0 and wcsAttacker ):
			chance = 24 + lvl * 2
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				damage       = ev['dmg_health']
				mirrorDamage = int(round( damage * 0.5 ))

				self.RaceTools.damage( wcsVictim, wcsAttacker, mirrorDamage )

				self.helper.raceTell( self, wcsVictim  , '#goodThorns Aura #defdealth #good%i #defmirror damage to #name%s#def!' % ( mirrorDamage, wcsAttacker.player.name ) )
				self.helper.raceTell( self, wcsAttacker, '#name%s #defdeals #bad%i #defmirror damage!' % ( wcsVictim.player.name, mirrorDamage ) )

		lvl = skills['Evasion']
		if ( lvl > 0 ):
			chance = 16 + lvl * 2
			rand   = randint( 1, 100 )
			if ( chance >= rand ):

				self.helper.raceTell( self, wcsVictim, '#goodEvasion #defevaded #good%i #defdamage!' % ev['dmg_health'] )

				return 0

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Trueshot Aura']
		if ( lvl > 0 ):
			chance = 16 + lvl * 2
			rand   = randint( 1, 100 )
			
			if ( chance >= rand ):
				damage      = ev['dmg_health']
				bonusDamage = int(round( damage * 0.2 ))

				self.helper.raceTell( self, wcsAttacker, '#goodTrueshot Aura #defdealt #good%i #defbonus damage to #name%s#def!' % ( bonusDamage, wcsVictim.player.name ) )

				return ( damage + bonusDamage )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Entangling Roots']
		if ( lvl > 0 ):
			distance = 300 + ( lvl * 10 )
			freeze   = 3

			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

			if ( len(targets) == 0 ):
				self.helper.raceTell( self, wcsPlayer, '#goodEntangling Roots #defNo targets in #goodrange#def!' )
				return False

			else:
				for wcsTarget in targets:

					self.RaceTools.freezePlayer( wcsTarget, freeze )

					self.Effects.beampoints( wcsPlayer, wcsTarget, 0, 255, 0, 255, freeze, 1, 'sprites/lgtning.vmt' )

					self.helper.raceTell( self, wcsTarget, '#name%s #badRoots #defyou in place for #bad%i #defseconds!' % ( wcsPlayer.player.name, freeze ) )

				self.helper.raceTell( self, wcsPlayer, '#goodEntangling Roots #defHits #good%i #defplayers!' % len( targets ) )

				return True
