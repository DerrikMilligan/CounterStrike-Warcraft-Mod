from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class Denchei( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['Famas','Pistols','Knife','Grenades']
		
		self.RaceColor                = '\x0767204E'
		self.RaceAbbreviation         = 'Denchei'

		self.RaceName                 = 'Denchei, Lokim Master'
		self.Coder                    = 'Fuzzy'
		self.RaceTypes                = ['Lokim']
		self.UltimateCooldown         = 5
		self.StartingUltimateCooldown = 5
		
		self.PlayerLimit              = 2
		self.RequiredLevel            = 0
		self.ChangeRaceIndex          = 10

		self.SkillList = [
			Skill( 'Recieve Supplies', 'You recieve an enchanted famas.'                           , 0, 0 ),
			Skill( 'Invisibility'    , 'Makes you partially invisible.'                            , 8, 0 ),
			Skill( 'Famas Expert'    , 'Chance to deal extra damage with famas.'                   , 8, 0 ),
			Skill( 'Teleport'        , '[Ultimate] Allows you to teleport to where you are aiming.', 8, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.giveWeapon( wcsPlayer, 'famas' )
		self.helper.raceTell( self, wcsPlayer, '#goodRecieve Supplies #defgives you an enchanted #goodFamas#def!' )

		lvl = skills['Invisibility']
		if ( lvl > 0 ):
			invis = 0.2 + ( lvl * 0.05 )
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, 1 - invis )
			self.helper.raceTell( self, wcsPlayer, '#goodInvisibility #defsets you to #good%i%% #definvis.' % round(invis * 100 ))

		lvl = skills['Famas Expert']
		if ( lvl > 0 ):
			chance = 24 + (lvl * 2) # 40%
			bonusDamage = 0.2 + (lvl * 0.05)
			self.helper.raceTell( self, wcsPlayer, '#goodFamas Expert #defgives you a #good%i%% #defchance to deal #good%i%% #defbonus damage!' % (chance, round(bonusDamage*100)) )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us

		weapon = ev['weapon']
		damage = ev['dmg_health']

		lvl = skills['Famas Expert']
		if ( lvl > 0 and weapon == 'weapon_famas' ):
			chance = 24 + (lvl * 2) # 40%
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				bonusDamage = damage * ( 0.2 + (lvl * 0.05) )
				self.helper.raceTell( self, wcsAttacker, '#goodFamas Expert #defdeals #good%i #defbonus damage!' % round( bonusDamage ) )
				return ( damage + bonusDamage )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]
		
		lvl = skills['Teleport']
		if ( lvl > 0 ):
			force  = 400 + ( lvl * 75 )
			self.RaceTools.pushToViewCoords( wcsPlayer, force )
			return True
