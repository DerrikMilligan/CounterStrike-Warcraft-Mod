from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class RetiredArmyOfficer( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse = ['m4a1', 'pistols', 'knife', 'grenades']

		self.RaceName          = 'Retired Army Officer'
		self.RaceTypes         = ['human']
		self.Coder             = 'MrCoolness'

		self.PlayerLimit       = 2
		self.RequiredLevel     = 16
		self.ChangeRaceIndex   = 100

		self.SkillList = [
			Skill( 'Battle Prep', 'Prepare for battle, gain bonus hp.'    , 8, 0 ),
			Skill( 'Army Camo'  , 'War paint paints you invisible.'       , 8, 0 ),
			Skill( 'Disarm'     , 'Remove your enemies primary weapon.'   , 8, 0 ),
			Skill( 'Reload'     , 'Killing your enemy overloads your gun.', 8, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.giveWeapon( wcsPlayer, 'm4a1' )

		lvl = skills['Battle Prep']
		if ( lvl > 0 ):
			bonusHealth = lvl * 5
			self.RaceTools.setHealth( wcsPlayer, 100 + bonusHealth )
			self.helper.raceTell( self, wcsPlayer, '#goodBattle Prep #defgrants you #good%i #defbonus HP!' % ( bonusHealth ) )

		lvl = skills['Army Camo']
		if ( lvl > 0 ):
			invis = 0.15 + ( lvl * 0.05 ) # 55%
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, (1-invis) )
			self.helper.raceTell( self, wcsPlayer, '#goodArmy Camo #defmakes you #good%i%% #defsee through!' % int(invis*100) )

		lvl = skills['Disarm']
		if ( lvl > 0 ):
			chance = lvl * 3
			self.helper.raceTell( self, wcsPlayer, '#goodDisarm #defgives you a #good%i%% #defchance to disarm people!' % chance )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Disarm']
		if ( lvl > 0 ):
			chance = lvl * 3
			rand = randint( 1, 100 )
			if ( chance >= rand ):
				self.RaceTools.disarm( wcsVictim )
				self.helper.raceTell( self, wcsAttacker, '#goodDisarm #defhas disarmed #name%s#def!' % wcsVictim.player.name )
				self.helper.raceTell( self, wcsVictim  , '#name%s #defhas disarmed you!' % wcsAttacker.player.name )

	def player_kill( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us

		lvl = skills['Reload']
		if ( lvl > 0 ):
			bonusAmmo = lvl * 3
			wcsAttacker.player.clip.primary += bonusAmmo

			self.helper.raceTell( self, wcsAttacker, '#goodReload #defadds #good%i #defammo to your M4A1 clip!' % bonusAmmo )
