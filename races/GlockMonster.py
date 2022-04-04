from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class GlockMonster( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['Glock', 'Knife', 'Grenades']

		self.RaceColor                = '\x0722AAAA'
		self.RaceAbbreviation         = 'GloMo' # faggy for fun - fff

		self.RaceName                 = 'Glock Monster'
		self.RaceTypes                = ['human']
		self.Coder                    = 'Tortoise & Mini Dude'
		self.UltimateCooldown         = 30
		self.StartingUltimateCooldown = 15
		
		self.PlayerLimit              = 0
		self.RequiredLevel            = 7
		self.ChangeRaceIndex          = 0

		self.SkillList = [
			Skill( 'Swiftness'      , 'Gain extra speed.'                , 5, 0 ),
			Skill( 'Vamp Aura'      , 'Steal health from opponents.'     , 5, 0 ),
			Skill( 'Fortitude Boost', 'Extra Health and Armor.'          , 5, 0 ),
			Skill( 'Army Supply'    , 'Extra Ammo.'                      , 5, 0 ),
			Skill( 'Gun Bash'       , 'Freeze Enemies.'                  , 5, 0 ),
			Skill( 'Burst Rage'     , '[Ultimate] Deal even more damage!', 5, 5 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		# give him his race gun!
		self.RaceTools.giveWeapon( wcsPlayer, 'glock' )

		lvl = skills['Swiftness']
		if ( lvl > 0 ):
			speed = 1 + ( lvl * 0.08 )
			self.RaceTools.setSpeed( wcsPlayer, speed )
			self.helper.raceTell( self, wcsPlayer, '#goodSwiftness #defgrants #good%i%% #defmove speed!' % int(speed*100) )

		lvl = skills['Vamp Aura']
		if ( lvl > 0 ):
			chance  = lvl * 4
			percent = lvl * 0.1
			self.helper.raceTell( self, wcsPlayer, '#redVamp Aura #defgrants a #good%i%% #defchance to steal #good%i%% #defof damage back as health!' % ( chance, int(percent*100) ) )

		lvl = skills['Fortitude Boost']
		if ( lvl > 0 ):
			bonus = lvl * 20
			self.RaceTools.setHealth( wcsPlayer, 100 + bonus )
			# FREE 100 ARMOR weeoh
			wcsPlayer.player.armor = 100 + bonus
			self.helper.raceTell( self, wcsPlayer, '#goodFortitude Boost #defgrants you #good%i #defbonus health and armor!' % bonus )

		lvl = skills['Army Supply']
		if ( lvl > 0 ):
			bonusAmmo = 20 * lvl

			self.RaceTools.setSecondaryClip( wcsPlayer,  20 + bonusAmmo )
			self.helper.raceTell( self, wcsPlayer, '#goodArmy Supply #defhas provided you with #good%i #defextra rounds in your clip!' % bonusAmmo )

		lvl = skills['Gun Bash']
		if ( lvl > 0 ):
			chance = lvl * 4
			freeze = 0.1
			self.helper.raceTell( self, wcsPlayer, '#blueGun Bash #defprovides a #good%i%% #defchance to freeze enemies on hit for #good%s #defseconds!' % ( chance, freeze ) )

		lvl = skills['Burst Rage']
		if ( lvl > 0 ):
			wcsPlayer.infoGlockMonsterUlt = False

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Vamp Aura']
		if ( lvl > 0 ):
			rand   = randint(1, 100)
			chance = lvl * 4
			if ( chance >= rand ):
				damage  = ev['dmg_health']
				percent = lvl * 0.1
				vamp    = percent * damage
				if( wcsAttacker.player.health + vamp <= 250 ):
					wcsAttacker.player.health += vamp
					self.helper.raceTell( self, wcsAttacker, '#redVamp Aura #defstole #good%i #defhealth from #name%s#def!' % ( int(vamp), wcsVictim.player.name ) )
		
		lvl = skills['Gun Bash']
		if ( lvl > 0 ):
			chance = lvl * 4
			rand   = randint(1, 100)
			if ( chance >= rand ):
				freeze = 0.1
				self.RaceTools.freezePlayer( wcsVictim, freeze )
				self.helper.raceTell( self, wcsAttacker, '#blueGun Bash #defyou have frozen #name%s #deffor #good%s #defseconds!' % ( wcsVictim.player.name, freeze ) )
				self.helper.raceTell( self, wcsVictim  , '#name%s #deffreezes you in place for #bad%s #defseconds!' % ( wcsAttacker.player.name, freeze ) )

		lvl = skills['Burst Rage']
		if ( lvl > 0 ):
			if ( wcsAttacker.infoGlockMonsterUlt ):
				return ev['dmg_health'] + lvl

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Burst Rage']
		if ( lvl > 0 ):
			duration = lvl + 5
			damage   = lvl

			wcsPlayer.infoGlockMonsterUlt = True

			self.helper.raceTell( self, wcsPlayer, '#goodBurst Rage #defall your attacks will do #good%i #defbonus damage over the next #good%i #defseconds!' % ( damage, duration ) )

			# turn the ult off
			gamethread.delayed( duration, setattr, ( wcsPlayer, 'infoGlockMonsterUlt', False ) )

			return True
