from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class RangerofVekas( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['Scout', 'Pistols', 'Knife', 'Grenades' ]

		self.RaceColor                = '\x0700AACC'
		self.RaceAbbreviation         = 'Ranger'

		self.RaceName                 = 'Ranger of Vekas'
		self.RaceTypes                = ['human']
		self.Coder                    = 'MrCoolness'
		self.UltimateCooldown         = 30
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 2
		self.RequiredLevel            = 15
		self.ChangeRaceIndex          = 100

		self.SkillList = [
			Skill( 'Woodsman'    , 'Your camouflage provides invisibility.'   , 5, 0 ),
			Skill( 'Hunters Shot', 'Your Scout does more damage.'             , 5, 0 ),
			Skill( 'Light Foot'  , 'You move quicker.'                        , 5, 0 ),
			Skill( 'Rooting'     , '[Ultimate] Freeze the enemies around you.', 5, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.giveWeapon( wcsPlayer, 'scout' )

		lvl = skills['Woodsman']
		if ( lvl > 0 ):
			invis = 0.25 + ( lvl * 0.05 )
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, (1 - invis) )
			self.helper.raceTell( self, wcsPlayer, '#goodWoodsman #defgrants you #good%i%% #definvis!' % int(invis*100) )

		lvl = skills['Hunters Shot']
		if ( lvl > 0 ):
			bonusDamage = 0.1 + ( lvl * 0.02 )
			self.helper.raceTell( self, wcsPlayer, '#goodHunters Shot #defgrants you #good%i%% #defbonus damage with your #goodScout#def!' % int( bonusDamage*100 ) )

		lvl = skills['Light Foot']
		if ( lvl > 0 ):
			speed = 0.1 + ( lvl * 0.04 )
			self.RaceTools.setSpeed( wcsPlayer, 1 + speed )
			self.helper.raceTell( self, wcsPlayer, '#goodLight Foot #defgrants you #good%i%% #defbonus speed!' % int(speed*100) )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		# wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		weapon   = ev['weapon']

		lvl = skills['Hunters Shot']
		if ( lvl > 0 and weapon == 'weapon_scout' ):
			damage      = ev['dmg_health']
			bonusDamage = damage * (0.1 + ( lvl * 0.02 ))
			self.helper.raceTell( self, wcsAttacker, '#goodHunters Shot #defdeals #good%i #defbonus damage!' % int(bonusDamage) )
			return ( damage + bonusDamage )

	def player_ultimate( self, ev, skills ) :
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Rooting']
		if ( lvl > 0 ):
			distance = 300 + ( lvl * 40 )
			freeze   = 1   + ( lvl * .2 )

			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

			if ( len(targets) == 0 ):
				self.helper.raceTell( self, wcsPlayer, '#goodRooting #defNo targets in range!' )
				return False

			else:
				for wcsTarget in targets:
					#freeze
					self.RaceTools.freezePlayer( wcsTarget, freeze )

					# effect
					self.Effects.beampoints( wcsPlayer, wcsTarget, 0, 255, 0, 255, freeze, 1, 'sprites/lgtning.vmt' )

					# message
					self.helper.raceTell( self, wcsTarget, '#name%s #defroots you in place for #bad%s #defseconds!' % ( wcsPlayer.player.name, freeze ) )

				self.helper.raceTell( self, wcsPlayer, '#goodRooting #deffreezes #good%i #defplayers for #good%s #defseconds!' % ( len(targets), freeze ) )
				return True
