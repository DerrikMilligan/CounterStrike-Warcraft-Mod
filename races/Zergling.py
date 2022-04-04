from ..tools.BaseClasses import baseRace, Skill
from ..tools import DamageTypes

import es, playerlib, gamethread
from random import randint

class Zergling ( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['Knife', 'Grenades']

		self.RaceColor                = '\x079F00FF'
		self.RaceAbbreviation         = 'Zerg'

		self.RacePrefix               = '[K]'
		self.RaceName                 = 'Zergling'
		self.RaceTypes                = [ 'monster', 'zerg', 'swarm' ]
		self.Coder                    = 'Mini Dude & Tortoise'

		self.UltimateCooldown         = 5
		self.StartingUltimateCooldown = 1

		self.PlayerLimit              = 0
		self.RequiredLevel            = 0

		self.SkillList = [
			Skill( 'Alien Lunge'       , 'You can lunge forward for a quick attack.'     , 6, 0 ),
			Skill( 'Alien Regeneration', 'Zerg slowly regenerate health'                 , 6, 0 ),
			Skill( 'Metabolic Boost'   , 'Increase the movement speed of zerglings.'     , 6, 0 ),
			Skill( 'Adrenal Glands'    , 'You deal extra damage with your acidic glands.', 6, 0 ),
			Skill( 'Burrow'            , '[Ultimate] Burrow Underground'                 , 6, 6 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		es.server.queuecmd( 'sm_resize #%s 0.7 500' % wcsPlayer )
		self.RaceTools.setColor( wcsPlayer, 0.4, 0, 0.4, 1, 1 )
		wcsPlayer.infoZerglingBurrow = False

		lvl = skills['Alien Lunge']
		if ( lvl > 0 ):
			multiplier = 0.3 + ( lvl * 0.2 )

			self.helper.raceTell( self, wcsPlayer, '#goodAlien Lunge #defallows you to jump #good%i%% #deffarther!' % round(multiplier*100) )

		lvl = skills['Alien Regeneration']
		if ( lvl > 0 ):
			self.RaceTools.Aura( wcsPlayer, ( 10 - lvl ), self.RegenerationAura, 'regeneration', lvl )
			self.helper.raceTell( self, wcsPlayer, '#goodAlien Regeneration #defheals you for %i every %i seconds, and doubles when #goodBurrowed#def!' % ( lvl, ( 10 - lvl ) ) )

		lvl = skills['Metabolic Boost']
		if ( lvl > 0 ):
			speed  =   1 + ( lvl * 0.1 )
			health = 100 - ( lvl *  15 )

			self.RaceTools.setSpeed( wcsPlayer, speed )
			self.RaceTools.setHealth( wcsPlayer, health )

			self.helper.raceTell( self, wcsPlayer, '#goodMetabolic Boost #defsets your speed to #good%i%%#def, but lowers your health to #bad%i#def!' % ( int(speed*100), health ) )

		lvl = skills['Adrenal Glands']
		if ( lvl > 0 ):
			bonusDamage = lvl * 0.08
			self.helper.raceTell( self, wcsPlayer, '#goodAdrenal Glands #defgrant you #good%i%% #defbonus damage!' % round(bonusDamage*100) )

	def player_jump( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Alien Lunge']
		if ( lvl > 0 ):
			multiplier = lvl * 0.2 + 0.3
			self.RaceTools.longJump( wcsPlayer, multiplier )

	def RegenerationAura( self, wcsPlayer, lvl ):
		health = lvl
		if ( wcsPlayer.infoZerglingBurrow ):
			health = lvl * 2

		if ( wcsPlayer.player.health + health >= 75 ):
			wcsPlayer.player.health = 75
		else:
			wcsPlayer.player.health += health

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		damage = int(event_var['dmg_health'])

		bonusdamage = damage * ( lvl * 0.08 )

		weapon = event_var['weapon']

		if ( weapon == 'weapon_knife' ):
			self.helper.raceTell( self, wcsAttacker, 'Your #goodAdrenal Glands #defdeal #good%i #defbonus damage!' % int(bonusdamage) )

			return (damage + bonusdamage)
		
	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Burrow']
		if ( lvl > 0 ):

			if ( not wcsPlayer.rooted ):

				x, y, z = wcsPlayer.player.location
				if ( wcsPlayer.infoZerglingBurrow == False ):

					wcsPlayer.player.freeze( 1 )
					z -= 100

					self.burrowPosition( wcsPlayer, x, y, z )
					gamethread.delayed( 0.05, self.burrowPosition, ( wcsPlayer, x, y, z ) )
					gamethread.delayed( 0.1, self.burrowPosition, ( wcsPlayer, x, y, z ) )
					gamethread.delayed( 0.2, self.burrowPosition, ( wcsPlayer, x, y, z ) )
					gamethread.delayed( 0.4, self.burrowPosition, ( wcsPlayer, x, y, z ) )
					gamethread.delayed( 0.6, self.burrowPosition, ( wcsPlayer, x, y, z ) )
					gamethread.delayed( 0.8, self.burrowPosition, ( wcsPlayer, x, y, z ) )

					self.RaceTools.setColor( wcsPlayer, 0.4, 0, 0.4, 0.9, 1 )

					self.helper.raceTell( self, wcsPlayer, '#goodBurrow #defYou\'re now underground!' )

					wcsPlayer.infoZerglingBurrow = True

					return True

				else:
					wcsPlayer.player.freeze(0)
					z += 110

					self.burrowPosition( wcsPlayer, x, y, z )
					self.helper.raceTell( self, wcsPlayer, '#goodBurrow #defYou\'re no longer underground!' )
					self.RaceTools.setColor( wcsPlayer, 0.4, 0, 0.4, 0.9, 1 )
					wcsPlayer.infoZerglingBurrow = False

					return True

			else:
				self.helper.raceTell( self, wcsPlayer, 'You\'re #badrooted#def, and are unable to #goodBurrow#def!' )

	def burrowPosition( self, wcsPlayer, x, y, z ):
		es.server.queuecmd( 'es_xsetpos %s %s %s %s' % ( wcsPlayer, x, y, z ) )

	# adjust the CD
	def adjust_cooldowns( self, ev, skills ):
		lvl = skills['Burrow']
		wcsPlayer = ev['wcsPlayer']
		if ( lvl == 2 or lvl == 3 ):
			wcsPlayer.ultimateCD = 3
		elif ( lvl == 4 or lvl == 5 ):
			wcsPlayer.ultimateCD = 2
		elif ( lvl == 6 ):
			wcsPlayer.ultimateCD = 1
		else:
			wcsPlayer.ultimateCD = 5

	# prevent fall damage
	def player_hurt( self, event_var, skills ):
		damageType = event_var['damage_type']

		# if the damage type is fall damage, prevent it
		if ( damageType & DamageTypes.DMG_FALL ):
			return 0

	# stop aura
	def round_end( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]
		lvl = skills['Alien Regeneration']
		if ( lvl > 0 ):
			self.RaceTools.stopAura( wcsPlayer, 'regeneration' )
