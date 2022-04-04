from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class DeathKnight( baseRace ):
	def __init__( self ):
		self.RaceColor                = '#gray'
		self.RaceAbbreviation         = 'DeathK'

		self.RaceName                 = 'Death Knight'
		self.RaceTypes                = ['humanoid', 'undead']
		self.Coder                    = 'MrCoolness & Mini Dude'
		self.UltimateCooldown         = 20
		self.StartingUltimateCooldown = 10

		self.RequiredLevel            = 4
		self.ChangeRaceIndex          = 50

		self.SkillList = [
			Skill( 'Howl of Terror', 'Some of your opponents shots miss through fear.'     , 5, 0 ),
			Skill( 'Blood Presence', 'Chance to deal mirror damage when attacked.'         , 5, 0 ),
			Skill( 'Death Pact'    , 'Receive extra health and armor at the cost of speed.', 5, 0 ),
			Skill( 'Chains of Ice' , '[Ultimate] Freezes an enemy in place ( Roots ).'     , 5, 5 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		# player color - blackish
		self.RaceTools.setColor( wcsPlayer, 0.4, 0.4, 0.4, 1 )

		lvl = skills['Death Pact']
		if ( lvl > 0 ):
			# determine new stats
			speed        = 0.04 * lvl
			bonushealth  = lvl * 15
			bonusarmor   = lvl * 20

			# apply new stats
			wcsPlayer.player.armor = 100 + bonusarmor
			self.RaceTools.setHealth( wcsPlayer, 100 + bonushealth )
			self.RaceTools.setSpeed( wcsPlayer, 1 - speed )

			# inform
			self.helper.raceTell( self, wcsPlayer, '#goodDeath Pact #defgrants you #good%i #defbonus #goodhp #defand #goodarmor#def, but reduces your speed to #bad%i%%#def.' % ( bonushealth, int(( 1 - speed ) * 100)) )

		lvl = skills['Howl of Terror']
		if ( lvl > 0 ) :
			chance  = lvl * 4
			self.helper.raceTell( self, wcsPlayer, '#goodHowl of Terror #defprovides a #good%i%% #defchance to #goodevade #defattacks.' % int( chance ) )

		lvl = skills['Blood Presence']
		if ( lvl > 0 ) :
			chance  = lvl * 8
			reflect = 100 * (lvl * 0.05)
			self.helper.raceTell( self, wcsPlayer, '#goodBlood Presence #defprovides a #good%i%% #defchance to #goodreflect #good%i%% #defdamage.' % ( int(chance), int(reflect) ) )

	def player_hurt( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ]
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Howl of Terror']
		if ( lvl > 0 ):
			# 20/100
			chance = lvl * 4
			rand   = randint( 1, 100 )
			if ( chance >= rand ) :
				self.helper.raceTell( self, wcsVictim, '#goodHowl of Terror #defallowed you to evade #good%i #defdamage!' % int(ev['dmg_health']) )
				return 0

		lvl = skills['Blood Presence']
		if ( lvl > 0 ):
			# 40/100
			chance = lvl * 8
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				# calculate reflect
				damage  = int(ev['dmg_health'])
				reflect = damage * (lvl * 0.05) # 25% reflect

				# messages
				self.helper.raceTell( self, wcsVictim  , '#goodBlood Presence #defreflected #good%i #defdamage to #name%s#def.' % ( int(reflect), wcsAttacker.player.name ) )
				self.helper.raceTell( self, wcsAttacker, '#name%s - #goodBlood Presence #defreflected #bad%i #defdamage!' % ( wcsVictim.player.name, int(reflect) ) )

				# damage
				self.RaceTools.damage( wcsVictim, wcsAttacker, reflect )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Chains of Ice']
		if ( lvl > 0 ):
			# range, and duration
			distance = 200 + ( lvl * 50  )
			freeze   =   1 + ( lvl * 0.2 )

			# get targets
			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

			# is there at least 1 target!?
			if ( len(targets) > 0 ):
				# message for player
				self.helper.raceTell( self, wcsPlayer, '#blueChains of Ice #deffreezes #good%i #defplayers!' % len(targets) )

				# loop through ALL targets
				for victim in targets:
					# freeze target for duration
					self.RaceTools.freezePlayer( victim, freeze )
					# line effect between player, and victim
					self.Effects.beampoints( wcsPlayer, victim, 0, 0, 255, 255, freeze, 1, 'sprites/lgtning.vmt' )
					# message for victim
					self.helper.raceTell( self, victim, '#name%s - #blueChains of Ice #deffreezes you for #bad%i #defseconds!' % ( wcsPlayer.player.name, freeze ) )

				# reset timer
				return True

			else:
				# inform player no targets in range
				self.helper.raceTell( self, wcsPlayer, 'No #badtargets #defwithin range!' )

				# don't reset timer
				return False
