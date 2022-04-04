from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class MegaMan( baseRace ):
	def __init__( self ):

		self.RaceColor                = '\x070033CC'
		self.RaceAbbreviation         = 'MegaM'

		self.RaceName                 = 'Mega Man'
		self.RaceTypes                = [ 'human' ]
		self.Coder                    = 'MrCoolness & Mini Dude'
		self.AbilityCooldown          = 15
		self.UltimateCooldown         = 30
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 0
		self.RequiredLevel            = 12
		self.ChangeRaceIndex          = 0

		self.SkillList = [
			Skill( 'Jump and Shoot', 'Mega Man is an expert at jumping and shooting',  0,  0 ),
			Skill( 'Charging Shot' , 'Charge up your shot for bonus damage.'        , 10,  0 ),
			Skill( 'Dash'          , '[Ability] Run faster for a short duration'    , 20,  0 ),
			Skill( 'Mega Armor'    , '[Ultimate] Mega Man reduces damage taken.'    , 10, 10 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.setColor( wcsPlayer, 0.5, 0.5, 1, 1 )
		self.RaceTools.setGravity( wcsPlayer, 0.75 )
		self.helper.raceTell( self, wcsPlayer, '#goodJump and Shoot #defsets you to #good75% #defgravity!' )

		lvl = skills['Charging Shot']
		if ( lvl > 0 ):
			wcsPlayer.infoMegaManChargingShot = True
			self.helper.raceTell( self, wcsPlayer, '#goodCharging Shot #defis ready, and will do #good20 #defbonus damage on your next attack!' )

		lvl = skills['Mega Armor']
		if ( lvl > 0 ):
			wcsPlayer.infoMegaManMegaArmor = False

		'''
		Race Mastery
		'''
		wcsPlayer.infoMegaManMasteryDamage    = 0
		wcsPlayer.infoMegaManMasteryReduction = False
		if ( wcsPlayer.level > 75 ):
			# setup the bonus damage mastery
			wcsPlayer.infoMegaManMasteryDamage = min( (wcsPlayer.level - 75), 5 )

			self.helper.raceTell( self, wcsPlayer, '#masteryRace Mastery #defprovides you with #good%i #defbonus damage on all attacks!' % wcsPlayer.infoMegaManMasteryDamage )

			if ( wcsPlayer.level > 120 ):
				wcsPlayer.infoMegaManMasteryReduction = True
				self.helper.raceTell( self, wcsPlayer, '#masteryRace Mastery #defcauses your ultimate to reduce #good10% #defmore damage!' )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Charging Shot']
		if ( lvl > 0 ):
			bonusDamage = 0

			if ( wcsAttacker.infoMegaManChargingShot ):
				bonusDamage += 20
				wcsAttacker.infoMegaManChargingShot = False
				self.helper.raceTell( self, wcsAttacker, '#goodCharging Shot #defhit #name%s #deffor #good20 #defbonus damage!' % wcsVictim.player.name )

				# delay to recharge the shot, and message
				gamethread.delayed( ( 15 - lvl ), setattr, ( wcsAttacker, 'infoMegaManChargingShot', True ) )
				gamethread.delayed( ( 15 - lvl ), self.helper.raceTell, ( self, wcsAttacker, '#goodCharging Shot #defis #goodready!' ) )

			if ( wcsAttacker.infoMegaManMasteryDamage > 0):
				bonusDamage += wcsAttacker.infoMegaManMasteryDamage

			return ( ev['dmg_health'] + bonusDamage )

	def player_hurt( self, ev, skills ):
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Mega Armor']
		if ( lvl > 0 and wcsVictim.infoMegaManMegaArmor ):
			reduction = round( 0.25 + lvl * 0.025, 2 )

			if ( wcsVictim.infoMegaManMasteryReduction ): reduction += 0.1

			return ( ev['dmg_health'] * ( 1 - reduction ) )

	def player_ability( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Dash']
		if ( lvl > 0 ):
			bonusSpeed = 0.2 + lvl * 0.02
			duration   = int(round( 2 + ( lvl / 4 ) ))

			wcsPlayer.player.speed += bonusSpeed

			self.helper.raceTell( self, wcsPlayer, '#goodDash #defgrants you #good%i%% #defbonus speed for #good%i #defseconds!' % ( int(bonusSpeed*100), duration ) )

			# reset your speed after the duration
			gamethread.delayed( duration, setattr, ( wcsPlayer.player, 'speed', 1 ) )
			gamethread.delayed( duration, self.helper.raceTell, ( self, wcsPlayer, '#goodDash #defis ending!' ) )

			return True

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Mega Armor']
		if ( lvl > 0 ):
			duration  = int(round( 5 + lvl / 2 ))      # 10 seconds
			reduction = round( 0.25 + lvl * 0.025, 2 ) # 50 % reduction

			if ( wcsPlayer.infoMegaManMasteryReduction ): reduction += 0.1

			self.helper.raceTell( self, wcsPlayer, '#goodMega Armor #defreduces #good%i%% #defof incoming damage for #good%i #defseconds!' % ( reduction*100, duration ) )

			wcsPlayer.infoMegaManMegaArmor = True
			gamethread.delayed( duration, setattr, ( wcsPlayer, 'infoMegaManMegaArmor', False ) )
			gamethread.delayed( duration, self.helper.raceTell, ( self, wcsPlayer, '#goodMega Armor #defis ending!' ) )

			return True
