from ..tools.BaseClasses import baseRace, Skill
from ..tools             import DamageTypes

import es, playerlib, gamethread
from random import randint

class Predator( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['Knife', 'Grenades']

		self.RaceAbbreviation         = 'Pred'
		self.RaceColor                = '#black'

		self.RacePrefix               = '[K]'
		self.RaceName                 = 'Predator'
		self.RaceTypes                = ['humanoid', 'monster', 'alien']
		self.Coder                    = 'MrCoolness & Mini Dude'
		self.UltimateCooldown         = 25
		self.StartingUltimateCooldown = 10

		self.PlayerLimit              = 0
		self.RequiredLevel            = 14
		self.ChangeRaceIndex          = 20

		self.SkillList = [
			Skill( 'Poison Blade', 'Your knife attacks slow people!'                             , 0, 0 ),
			Skill( 'Pounce'      , 'Leap towards your enemy.'                                    , 5, 0 ),
			Skill( 'Stealth'     , 'You hide well when lurking for prey.'                        , 5, 0 ),
			Skill( 'Vanish'      , 'Your remaining enemies are baffled after your first strike.' , 5, 0 ),
			Skill( 'Gobble'      , 'The flesh of your enemy gives you strength.'                 , 5, 0 ),
			Skill( 'Ravage'      , '[Ultimate] You become more vicious.'                         , 5, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		# lvl = skills['Poison Blade']
		slow     = 0.5
		self.helper.raceTell( self, wcsPlayer, '#goodPoison Blade #defslows your victims by #good%i#def!' % int(slow*100) )

		wcsPlayer = self.helper.getPlayer( wcsPlayer )
		wcsPlayer.speed = 1

		lvl = skills['Pounce']
		if ( lvl > 0 ):
			# slow the player initially
			gamethread.delayed( 2, setattr, ( wcsPlayer, 'speed', 0.5 ) )

			multiplier = 0.5 + ( lvl * 0.5 ) # 300%
			self.helper.raceTell( self, wcsPlayer, '#goodPounce #defcauses you to jump #good%i%% #deffarther.' % int( multiplier*100 ) )

		lvl = skills['Stealth']
		if ( lvl > 0 ):
			invis = 0.4 + ( lvl * 0.08 ) # 80%
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, ( 1 - invis ) )
			self.helper.raceTell( self, wcsPlayer, '#goodStealth #defprovides you with #good%i%% #definvis!' % int( invis*100 ) )

		lvl = skills['Vanish']
		if ( lvl > 0 ):
			duration = 0.5 + ( lvl * 0.2 )
			self.helper.raceTell( self, wcsPlayer, '#goodVanish #defcauses you to go #good100%% #definvisible for #good%i #defseconds when you attack!' % int( duration ) )

		lvl = skills['Gobble']
		if ( lvl > 0 ):
			chance = 25 + ( lvl * 5 )
			hp     = 10 + lvl
			self.helper.raceTell( self, wcsPlayer, '#goodGobble #defgrants a #good%i%% #defchance to gain #good%i #defhealth when you #redattack#def.' % ( chance, hp ) )

		lvl = skills['Ravage']
		if ( lvl > 0 ):
			wcsPlayer.infoPredatorRavage = False

	def player_jump( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Pounce']
		if ( lvl > 0 ):
			multiplier = 0.5 + ( lvl * 0.5 )

			self.RaceTools.longJump( wcsPlayer, multiplier, 800, 400 )

			# x = es.getplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_vecVelocity[0]' )
			# y = es.getplayerprop( wcsPlayer, 'CBasePlayer.localdata.m_vecVelocity[1]' )

			# if (
			# 	x < 800 and x > -800 and
			# 	y < 800 and y > -800
			#    ):

			# 	x *= multiplier
			# 	y *= multiplier

			# 	x = max( -400, min( x, 400 ) )
			# 	y = max( -400, min( y, 400 ) )

			# 	if (
			# 		x <= 1200 and x >= -1200 and
			# 		y <= 1200 and y >= -1200
			# 	   ):

			# 		# es.msg( (x,y) )
			# 		# for some reason he goes to high push him down a bit
			# 		self.RaceTools.pushToPoint( player, x, y, 0 )
			# 		# self.RaceTools.pushToPoint( player, x, y, -25 )

	def player_air( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Pounce']
		if ( lvl > 0 ):
			wcsPlayer.speed += 0.5

	def player_land( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Pounce']
		if ( lvl > 0 ):
			wcsPlayer.speed -= 0.5

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		# apply the posion blade affect
		self.RaceTools.slowPlayer( wcsVictim, 0.5, 1 )

		lvl = skills['Vanish']
		if ( lvl > 0 ):
			duration = 0.5 + ( lvl * 0.2 )

			oldAlpha = wcsAttacker.alpha

			# whatever his alpha is, remove it
			wcsAttacker.alpha -= oldAlpha

			# make is so when someones cursor is over you, it doesn't show your name
			es.setplayerprop( wcsAttacker, 'CBaseAnimating.m_nHitboxSet', 2 )

			self.helper.raceTell( self, wcsAttacker, '#goodVanish #defhides you for #good%i #defseconds!' % int( duration ) )

			# then delay to set it back
			gamethread.delayed( duration, self.VanishOff, ( wcsAttacker, oldAlpha ) )

			# if you set this to '1' when people look at you, it will crash their game
			gamethread.delayed( duration, es.setplayerprop, ( wcsAttacker, 'CBaseAnimating.m_nHitboxSet', 0 ) )

		lvl = skills['Gobble']
		if ( lvl > 0 ):
			chance = 25 + ( lvl * 5 )
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				hp = 10 + lvl
				wcsAttacker.attacker.health += hp

				self.helper.raceTell( self, wcsAttacker, '#goodGobble #defgains you #good%i #defhealth!' % hp )

		lvl = skills['Ravage']
		if ( lvl > 0 and wcsAttacker.infoPredatorRavage ):
			damage = ev['dmg_health']

			# range of the bonus damage
			bonusDamage = randint( lvl*5, lvl*10 )

			self.helper.raceTell( self, wcsAttacker, '#goodRavage #defdeals #good%i #defbonus damage to #name%s#def.' % ( bonusDamage, wcsVictim.player.name ) )
			self.helper.raceTell( self, wcsVictim  , '#name%s #defdeals #bad%i #defravage damage!' % ( wcsAttacker.player.name, bonusDamage ))

			return ( damage + bonusDamage )

	def player_hurt( self, ev, skills ):
		damageType = ev['damage_type']

		# if the damage type is fall damage, prevent it
		if ( damageType & DamageTypes.DMG_FALL ):
			return 0

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Ravage']
		if ( lvl > 0 ):

			duration = lvl
			damage   = lvl * 10

			self.helper.raceTell( self, wcsPlayer, '#goodRavage #defgrants you #redup to #good%i #defbonus damage #redrandomly #deffor #good%i #defseconds!' % ( damage, duration ) )

			# turn it on
			wcsPlayer.infoPredatorRavage = True

			# turn it off
			gamethread.delayed( duration, setattr, ( wcsPlayer, 'infoPredatorRavage', False ) )

			return True

	def VanishOff( self, wcsPlayer, oldAlpha ):
		wcsPlayer.alpha += oldAlpha # no idea how to preform this opertion pragmatically
