from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class TheRake( baseRace ):
	def __init__( self ):
		self.RaceAbbreviation         = 'Rake'
		self.RaceColor                = '\x073333CC'

		self.WeaponsCanOnlyUse        = ['Knife', 'Grenades' ]

		self.RacePrefix               = '[K]'
		self.RaceName                 = 'The Rake'
		self.RaceTypes                = ['monster']
		self.Coder                    = 'Mini Dude\nIdea: 3Dolla^Mafia'

		self.UltimateCooldown         = 5
		self.StartingUltimateCooldown = 3

		self.AbilityCooldown          = 1
		StartingAbilityCooldown       = 0

		self.PlayerLimit              = 0
		self.RequiredLevel            = 19

		self.SkillList = [
			Skill( 'Dismemberment / Laceration', '[Ability] Disarm + Damage / Bleed', 6, 0 ),
			Skill( 'Shrouded in Mystery'       , 'You are quick and unseen.'        , 6, 0 ),
			Skill( 'Blood Lust'                , 'Eat the bodies of your victims.'  , 6, 0 ),
			Skill( 'Unseen Portal'             , '[Ultimate] On the wings of death.', 6, 6 )
		]

	knifeTypes = [ 'Dismemberment', 'Laceration' ]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Dismemberment / Laceration']
		if ( lvl > 0 ):
			if ( not hasattr( wcsPlayer, 'infoTheRakeKnifeType' ) ):
				wcsPlayer.infoTheRakeKnifeType = 0

			knifeType = self.knifeTypes[ wcsPlayer.infoTheRakeKnifeType ]
			if ( knifeType == 'Dismemberment' ):
				chance      = 18   + (lvl *    3) # 36%
				bonusDamage = 0.26 + (lvl * 0.04) # 50%

				self.helper.raceTell( self, wcsPlayer, '#good%s #defgives you a #good%i%% #defchance to #gooddisarm #defand deal #good%i%% #defbonus damage' % ( knifeType, chance, round(bonusDamage*100) ) )
			
			else:
				chance = 30 + (lvl * 5) # 60%
				damage = 18 + (lvl * 2) # 30 bleed

				self.helper.raceTell( self, wcsPlayer, '#good%s #defgives you a #good%i%% #defchance to cause #redbleeding #deffor #good%i #defdamage' % ( knifeType, chance, damage ) )

		lvl = skills['Shrouded in Mystery']
		if ( lvl > 0 ):
			speed = 0.3  + (lvl * 0.05) # 60%
			invis = 0.24 + (lvl * 0.04) # 48%

			self.RaceTools.setSpeed( wcsPlayer, (1+speed) )
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, (1-invis) )

			self.helper.raceTell( self, wcsPlayer, '#goodShrouded in Mystery #defgrants you #good%i%% #defspeed and #good%i%% #definvis!' % ( round(speed*100), round(invis*100) ) )

		lvl = skills['Blood Lust']
		if ( lvl > 0 ):
			health = 18 + ( lvl * 2 ) # 30 health

			self.helper.raceTell( self, wcsPlayer, '#goodBlood Lust #defgrants you #good%i #defhealth when you kill a player!' % health )

		lvl = skills['Unseen Portal']
		if ( lvl > 0 ):
			wcsPlayer.infoTheRakeUltimateState = False

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		weapon   = ev['weapon']
		damage   = ev['dmg_health']

		lvl = skills['Dismemberment / Laceration']
		if ( lvl > 0 and weapon == 'weapon_knife' ):

			knifeType = self.knifeTypes[ wcsAttacker.infoTheRakeKnifeType ]
			if ( knifeType == 'Dismemberment' ):
				chance = 18 + (lvl * 3) # 36%
				rand   = randint( 1, 100 )
				if ( chance >= rand ):
					bonusDamage = damage * (0.26 + (lvl * 0.04)) # 50%

					self.RaceTools.disarm( wcsVictim, True )

					self.helper.raceTell( self, wcsAttacker, '#goodDismemberment #defdisarms #name%s #defand deals #good%i #defbonus damage!' % ( wcsVictim.player.name, round(bonusDamage) ) )
					self.helper.raceTell( self, wcsVictim  , '#goodDismemberment #name%s #defhas disarmed you.' % wcsAttacker.player.name )

					return ( damage + bonusDamage )

			else:
				chance = lvl * 10 # 60%
				rand   = randint( 1, 100 )
				if ( chance >= rand ):
					damage = 18 + (lvl * 2) # 30 bleed

					self.RaceTools.DOT( wcsAttacker, wcsVictim, 3, damage, self.BleedEffect )

					self.helper.raceTell( self, wcsAttacker, '#goodLaceration #defcauses #name%s #defto #badbleed #deffor #bad%i #defdamage!' % ( wcsVictim.player.name, damage ) )
					self.helper.raceTell( self, wcsVictim  , '#goodLaceration #name%s #defcauses you to bleed for #bad%i #defdamage.' % ( wcsAttacker.player.name, damage ) )

	def player_kill( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		# wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Blood Lust']
		if ( lvl > 0 ):
			health = 18 + ( lvl * 2 )
			attacker.health += health

			self.helper.raceTell( self, wcsAttacker, '#goodBlood Lust #defyou gain #good%i #deffor getting a kill!' % health )

	def player_ability( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Dismemberment / Laceration']
		if ( lvl > 0 ):

			if ( wcsPlayer.infoTheRakeKnifeType == 0 ):
				wcsPlayer.infoTheRakeKnifeType = 1
			else:
				wcsPlayer.infoTheRakeKnifeType = 0

			knifeType = self.knifeTypes[ wcsPlayer.infoTheRakeKnifeType ]

			self.helper.raceTell( self, wcsPlayer, 'You have changed your attack type to #good%s#def!' % knifeType )

			return True

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Unseen Portal']
		if ( lvl > 0 ):
			force = 600 + ( lvl * 50 )

			self.RaceTools.setGravity( wcsPlayer, 0.7 )
			self.RaceTools.pushToViewCoords( wcsPlayer, force )

			wcsPlayer.infoTheRakeUltimateState = True

			return True

	def player_air( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Unseen Portal']
		if ( lvl > 0 and wcsPlayer.infoTheRakeUltimateState ):
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, 0.05 )
			self.helper.raceTell( self, wcsPlayer, '#goodUnseen Portal #defYou are now #good5% #defvisible!' )

	def player_land( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]
		
		lvl = skills['Unseen Portal']
		if ( lvl > 0 and wcsPlayer.infoTheRakeUltimateState ):
			invis = 0.24 + (lvl * 0.04) # 48%

			self.RaceTools.delayed( 0.5, self.RaceTools.setColor  , ( wcsPlayer, 1, 1, 1, (1-invis) ) )
			self.RaceTools.delayed( 0.5, self.helper.raceTell     , ( self, wcsPlayer, '#goodUnseen Portal #defyour #goodinvisibility #defis now gone!' ) )
			self.RaceTools.delayed( 0.2, self.RaceTools.setGravity, ( wcsPlayer, 1 ) )

			wcsPlayer.infoTheRakeUltimateState = False

	def BleedEffect( self, attacker, victim ):
		self.RaceTools.fadeScreen( victim, 1, 255, 50, 50, 100  )
