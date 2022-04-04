from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread, usermsg
from random import randint

class MarauderKhalid( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse = ['Galil','Pistols','Grenades','Knife']

		self.RaceColor         = '\x07FFBD55'
		self.RaceAbbreviation  = 'Khalid'

		self.RaceName          = 'Marauder Khalid'
		self.Coder             = 'MrCoolness'
		self.RaceTypes         = ['human']
		self.UltimateCooldown  = 30
		self.AbilityCooldown   = 20

		self.PlayerLimit       = 2
		self.RequiredLevel     = 11
		self.ChangeRaceIndex   = 80

		self.SkillList = [
			Skill( 'Marauder\'s Arsenal', 'You carry a galil with an oversized clip.'           , 8,  0 ),
			Skill( 'Thorned Carapace'   , 'You hurt those who hurt you.'                        , 8,  0 ),
			Skill( 'Warrior Training'   , 'Precise aim provides bonus damage.'                  , 8,  0 ),
			Skill( 'Dirty Tricks'       , 'Pack your bullets with a toxin which weakens vision.', 8,  0 ),
			Skill( 'War Cry'            , '[Ability] Shake nearby enemies with your war cry.'   , 8,  8 ),
			Skill( 'For Allah'          , '[Ultimate] Take others with you, for Allah.'         , 8, 16 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Marauder\'s Arsenal']
		if ( lvl > 0 ):
			bonusclip = lvl * 5
			self.RaceTools.giveWeapon( wcsPlayer, 'galil' )
			self.RaceTools.setPrimaryClip( wcsPlayer, 35 + bonusclip )
			self.helper.raceTell( self, wcsPlayer, '#goodMarauder\'s Arsenal #defProvides you a #goodGalil #defwith #good%i #defbonus bullets!' % bonusclip )

		lvl = skills['Thorned Carapace']
		if ( lvl > 0 ):
			reflectAmmount = lvl * 0.025
			self.helper.raceTell( self, wcsPlayer, '#goodThorned Carapace #defreflects #good%i%% #defof all damage!' % int( reflectAmmount * 100 ) )

		lvl = skills['Warrior Training']
		if ( lvl > 0 ):
			bounusDamage = lvl * 0.0125
			self.helper.raceTell( self, wcsPlayer, '#goodWarrior Training #defprovides #good%i%% #defdamage on all attacks!' % int( bounusDamage * 100 ) )

		lvl = skills['Dirty Tricks']
		if ( lvl > 0 ):
			chance = 3 * lvl
			self.helper.raceTell( self, wcsPlayer, '#goodDirty Tricks #defprovides a #good%i%% #defchance to blind people on attack!' % chance )

	def player_hurt( self, ev, skills ):
		wcsVictim = self.helper.players[ str(ev['userid']) ]

		wcsAttacker = False
		if ( str(ev['attacker']) in self.helper.players ):
			wcsAttacker = self.helper.players[ str(ev['attacker']) ]

		lvl = skills['Thorned Carapace']
		if ( lvl > 0 and wcsAttacker ):
			damage = ev['dmg_health']

			reflect = damage * ( lvl * 0.025 )

			self.RaceTools.damage( wcsVictim, wcsAttacker, reflect )

			self.helper.raceTell( self, wcsVictim  , '#goodThorned Carapace #defreflects #good%i #defdamage to #name%s#def.' % ( int( reflect ), wcsAttacker.player.name ) )
			self.helper.raceTell( self, wcsAttacker, '#name%s #defreflects #good%i #defdamage.' % ( wcsVictim.player.name, int( reflect ) ) )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ]
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Dirty Tricks']
		if ( lvl > 0 ):
			chance = 3 * lvl
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				self.RaceTools.fadeScreen( wcsVictim, 1, 0, 0, 0, 240 )
				self.helper.raceTell( self, wcsAttacker, '#goodWarrior Training #defblinds #name%s#def.' % wcsVictim.player.name )
				self.helper.raceTell( self, wcsVictim  , '#goodWarrior Training #name%s #defblinds you.' % wcsAttacker.player.name )

		lvl = skills['Warrior Training']
		if ( lvl > 0 ):
			damage      = ev['dmg_health']
			bonusDamage = damage * ( lvl * 0.0125 )

			self.helper.raceTell( self, wcsAttacker, '#goodWarrior Training #defhits #name%s #deffor #good%i #defbonus damage.' % ( wcsVictim.player.name, int( bonusDamage ) ) )

			return ( damage + bonusDamage )

	def player_ability( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['War Cry']
		if ( lvl > 0 ):
			duration = 0.375 * lvl
			distance = lvl * 100

			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

			if ( len(targets) == 0 ):
				self.helper.raceTell( self, wcsPlayer, '#goodWar Cry #defNo targets in range!' )
				return False
			else:
				for wcsTarget in targets:
					usermsg.shake( wcsTarget, 80, duration )
					self.helper.raceTell( self, wcsTarget, '#name%s roars fiercly and #badshakes #defyour screen!' % wcsPlayer.player.name )

				self.helper.raceTell( self, wcsPlayer, '#goodWar Cry #defhits #good%i #defpeople!' % len( targets ) )
				return True

	def player_ultimate( self, ev, skills ):
		player = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['For Allah']
		if ( lvl > 0 ):
			distance    = lvl * 40
			bonusDamage = lvl * 25

			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

			self.RaceTools.damage( wcsPlayer, wcsPlayer, 300 )

			for wcsTarget in targets:
				self.RaceTools.damage( wcsPlayer, wcsTarget, bonusDamage )
				self.helper.raceTell( self, wcsTarget, '#name%s #defhas sacrificed himself for #redAllah#def, and dealt #bad%i #defdamage to you!' % ( wcsPlayer.player.name, bonusDamage ) )

			self.helper.raceTell( self, wcsPlayer, '#goodFor Allah #defhit #good%i #defplayers for #good%i #defdamage.' % ( len(targets), bonusDamage ) )
			return True
