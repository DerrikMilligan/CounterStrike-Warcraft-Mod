from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class Lobster( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = [ 'knife', 'flashbang', 'smokegrenade', 'hegrenade' ]

		self.RaceColor                = '\x07CC0000'
		self.RaceAbbreviation         = 'Lob'

		self.RacePrefix               = '[K]'
		self.RaceName                 = 'Lobster'
		self.RaceTypes                = [ 'lobster', 'food', 'monster' ]
		self.Coder                    = 'Tortoise & Mini Dude\nIdea: 3Dolla^Mafia'
		self.UltimateCooldown         = 15
		# self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 2
		self.RequiredLevel            = 8

		self.SkillList = [
			Skill( 'Biologically Immortal', 'You will Regenerate lost Health.'                                       , 8,  0 ),
			Skill( 'Hard Shell'           , 'Your hard exoskeleton provides extra Health and Armor'                  , 8,  0 ),
			Skill( 'Powerful Tail'        , 'Your powerful tail allows you to move quickly.'                         , 8,  0 ),
			Skill( 'Powerful Claws'       , 'Your claws have a chance to tear your opponents arms off.'              , 8,  0 ),
			Skill( 'Claw Attack'          , '[Ultimate] Your next attack has a chance to tear your opponent in half.', 8, 24 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.setColor( wcsPlayer, 1, 0, 0, 1 )

		lvl = skills['Biologically Immortal']
		if ( lvl > 0 ):
			interval = 10-lvl
			regen    = lvl * 2
			self.RaceTools.Aura( wcsPlayer, interval, self.RegenerationAura, 'regen', regen )
			self.helper.raceTell( self, wcsPlayer, '#good[Regeneration] #defGrants #good%s #defhealth every #good%s #defseconds!' % ( regen, interval ) )

		lvl = skills['Hard Shell']
		if ( lvl > 0 ):
			health = 60 + (lvl * 5)
			armor  = lvl * 10

			self.RaceTools.setHealth( wcsPlayer, 100 + health )
			wcsPlayer.player.armor = 100 + armor
			self.helper.raceTell( self, wcsPlayer, '#good[Hard Shell] #defProvides you wtih #good%i #defbonus health, and #good%i #defbonus armor!' % ( health, armor ) )

		lvl = skills['Powerful Tail']
		if ( lvl > 0 ):
			speed = 0.3 + lvl * 0.04
			self.RaceTools.setSpeed( wcsPlayer, 1 + speed )
			self.helper.raceTell( self, wcsPlayer, '#good[Powerful Tail] #defAllows you to move #good%i%% #deffaster!' % int( speed*100 ) )

		lvl = skills['Powerful Claws']
		if ( lvl > 0 ):
			chance = 10 + lvl * 5
			self.helper.raceTell( self, wcsPlayer, '#good[Powerful Claws] #defGrants a #good%i%% #defchance to disarm a player on attack!' % chance )

		lvl = skills['Claw Attack']
		if ( lvl > 0 ):
			wcsPlayer.infoLobsterUlt = False

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Powerful Claws']
		if ( lvl > 0 ):
			weapon = ev['weapon']
			# 50 / 100
			chance = 10 + lvl * 5 
			rand   = randint( 1, 100 )
			if ( weapon == 'weapon_knife' and chance >= rand ):
				self.helper.raceTell( self, wcsVictim  , '#name%s #defhas disarmed you!' % wcsAttacker.player.name )
				self.helper.raceTell( self, wcsAttacker, '#good[Powerful Claws] #defYou have disarmed #name%s#def!' % wcsVictim.player.name )
				self.RaceTools.disarm( wcsVictim, True )

		lvl = skills['Claw Attack']
		if ( lvl > 0 ):
			weapon = ev['weapon']
			damage = ev['dmg_health']

			# is our ult been used, and is the wepon our knife
			if ( wcsAttacker.infoLobsterUlt and weapon == 'weapon_knife' ):
				# is it a right click attack?
				if ( damage >= 60 ):
					chance = lvl * 9
					rand   = randint( 1, 100 )
					if ( chance >= rand ):
						self.RaceTools.damage( wcsAttacker, wcsVictim, wcsVictim.player.health/2, True )
						self.helper.raceTell( self, wcsAttacker, '#good[Claw Attack] #defCut #name%s #defin half!' % wcsVictim.player.name )
					else:
						self.helper.raceTell( self, wcsAttacker, '#good[Claw Attack] #defMissed!' )

					# begin the ult CD timer
					wcsAttacker.resetTimer( 'ultimate' )
				else:
					self.helper.raceTell( self, wcsAttacker, '#good[Claw Attack] #defonly works with a #goodright click #defknife attack!' )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Claw Attack']
		if ( lvl > 0 ):

			if ( wcsPlayer.infoLobsterUlt ):
				self.helper.raceTell( self, wcsPlayer, '#good[Claw Attack] #defis already prepped!' )
			else:
				chance = lvl * 9
				wcsPlayer.infoLobsterUlt = True
				self.helper.raceTell( self, wcsPlayer, '#good[Claw Attack] #defYour next right click knife has a #good%i%% #defchance to #goodhalf #defthe guys health!' % chance )

			# return True # lets put on cd When he attacks

		return None

	def RegenerationAura( self, wcsPlayer, regen ):
		if ( wcsPlayer.player.health + regen <= 250 ):
			wcsPlayer.player.health += regen