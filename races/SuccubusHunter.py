from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class SuccubusHunter( baseRace ):
	def __init__( self ):
		self.RaceAbbreviation         = 'ScrubHunter'
		self.RaceColor                = '\x07CC2255'

		self.RaceName                 = 'Succubus Hunter'
		self.Coder                    = 'MrCoolness & Mini Dude'
		self.RaceTypes                = ['human', 'hunter']

		self.UltimateCooldown         = 30
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 0
		self.RequiredLevel            = 18

		self.SkillList = [
			Skill( 'Daemonic Knife'         , 'Deal extra damage with a knife.'                                        , 3, 0 ),
			Skill( 'Head Hunter'            , 'Deal bonus damage, and collect a skull when you kill someone.'          , 3, 0 ),
			Skill( 'Totem Incantation'      , 'Gain bonus hp and money for each skull you have.'                       , 3, 0 ),
			Skill( 'Assault Tackle'         , 'Allows you to jump farther.'                                            , 3, 0 ),
			Skill( 'Daemonic Transformation', '[Ultimate] Gain invisibility, lower gravity and HP. Costs 1/2/3 skulls.', 3, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		# initialize skulls
		if ( not hasattr( wcsPlayer, 'infoSuccubusHunterSkulls' ) ):
			wcsPlayer.infoSuccubusHunterSkulls = 0

		skulls = wcsPlayer.infoSuccubusHunterSkulls

		if ( skulls > 0 ):
			self.helper.raceTell( self, wcsPlayer, '#defYou have #good%i #defskulls collected' % skulls )

		lvl = skills['Daemonic Knife']
		if ( lvl > 0 ):
			bonusDamage = 0.2 + ( lvl * 0.1 ) # 50%
			self.helper.raceTell( self, wcsPlayer, '#goodDaemonic Knife #defcauses your knife to deal #good%i%% #defbonus damage!' % round(bonusDamage*100) )

		lvl = skills['Head Hunter']
		if ( lvl > 0 ):
			chance      = 10   + ( lvl * 10   ) # 40%
			skullChance = 30   + ( lvl * 20   ) # 90%
			bonusDamage = 0.15 + ( lvl * 0.05 ) # 30%
			self.helper.raceTell( self, wcsPlayer, '#goodHead Hunter #defyou have a #good%i%% #defchance to deal #good%i%% #defbonus damage, and #good%i%% #defchance to get a skull when you kill someone!' % (chance, round(bonusDamage*100), skullChance) )

		lvl = skills['Totem Incantation']
		if ( lvl > 0 ):
			bonusHP = skulls * ( lvl * 2 )
			# cap the bonus health
			if ( bonusHP > 50 ): bonusHP = 50
			self.RaceTools.setHealth( wcsPlayer, 100 + bonusHP )

			bonusMoney = skulls * ( lvl * 100 )
			# cap the bonus money
			if ( bonusMoney > 2000 ): bonusMoney = 2000
			wcsPlayer.player.cash += bonusMoney

			self.helper.raceTell( self, wcsPlayer, '#goodTotem Incantation #defgrants you #good%i #defbonus health and #good%i #defbonus money!' % (bonusHP, bonusMoney) )

		lvl = skills['Assault Tackle']
		if ( lvl > 0 ):
			multiplier = 1 + ( lvl * 0.1 )

			self.helper.raceTell( self, wcsPlayer, '#goodAssault Tackle #defcauses you to jump #good%i%% #deffarther!' % round(multiplier*100) )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		# wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		damage   = ev['dmg_health']
		weapon   = ev['weapon']

		lvl = skills['Daemonic Knife']
		if ( lvl > 0 and weapon == 'weapon_knife' ):
			bonusDamage = damage * (0.2 + ( lvl * 0.1 )) # 50%

			self.helper.raceTell( self, wcsAttacker, '#goodDaemonic Knife #defdeals #good%i #defbonus damage!' % round(bonusDamage) )

			return ( damage + bonusDamage )

		lvl = skills['Head Hunter']
		if ( lvl > 0 ):
			chance = 10 + ( lvl * 10 ) # 40%
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				bonusDamage = damage * (0.15 + ( lvl * 0.05 )) # 30%

				self.helper.raceTell( self, wcsAttacker, '#goodHead Hunter #defdeals #good%i #defbonus damage!' % round(bonusDamage) )

				return ( damage + bonusDamage )

	def player_kill( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Head Hunter']
		if ( lvl > 0 ):
			chance = 30 + ( lvl * 20 ) # 90%
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				self.helper.raceTell( self, wcsAttacker, '#goodHead Hunter #defgot you a #redskull #def from killing #name%s#def!' % wcsVictim.player.name )

				wcsAttacker.infoSuccubusHunterSkulls += 1

	def player_jump( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Assault Tackle']
		if ( lvl > 0 ):
			multiplier = 1 + ( lvl * 0.1 ) # 130%

			self.RaceTools.longJump( wcsPlayer, multiplier )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Daemonic Transformation']
		if ( lvl > 0 ):
			# each level takes another skull
			if ( wcsPlayer.infoSuccubusHunterSkulls >= lvl ):

				bonusHP  = 10 + ( lvl * 10 )   # 40 HP
				invis    = lvl * 0.15          # 45% Invis
				grav     = 0.1 + ( lvl * 0.1 ) # 40% lower gravity
				duration = lvl * 3             # 9 seconds

				wcsPlayer.player.health += bonusHP
				self.RaceTools.setColor( wcsPlayer, 1, 1, 1, (1 - invis) )
				self.RaceTools.setGravity( wcsPlayer, (1 - grav) )

				# remove the skulls
				wcsPlayer.infoSuccubusHunterSkulls -= lvl

				self.helper.raceTell( self, wcsPlayer, '#goodDaemonic Transformation #defyou sacrifice #bad%i #defskulls, and have #good%i #defskulls remaining!' % ( lvl, wcsPlayer.infoSuccubusHunterSkulls ) )
				self.helper.raceTell( self, wcsPlayer, '#goodDaemonic Transformation #defYou gain #good%i #defbonus HP, #good%i%% #definvis, and #good%i%% #lower gravity for #good%i #defseconds!' % ( bonusHP, invis, grav, duration ) )

				gamethread.delayed( duration, self.Daemonic_Transformation_Off, wcsPlayer )

	def Daemonic_Transformation_Off( self, wcsPlayer ):
		self.RaceTools.setColor( wcsPlayer, 1, 1, 1, 1 )
		self.RaceTools.setGravity( wcsPlayer, 1 )
		self.helper.raceTell( self, wcsPlayer, '#goodDaemonic Transformation #defis ending!' )
