from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class Lurker( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['Usp','Grenades']

		self.RaceColor                = '\x07888589'
		self.RaceAbbreviation         = 'Lurker'

		self.RaceName                 = 'Lurker'
		self.Coder                    = 'Fuzzy & Mini Dude'
		self.RaceTypes                = ['human']
		
		self.PlayerLimit              = 2
		self.RequiredLevel            = 0

		self.SkillList = [
			Skill( 'Cloak of Hiding', 'Put on a cloak to become almost completely invisible.', 8, 0 ),
			Skill( 'Undead Legs'    , 'Gives you more speed.'                                , 8, 0 ),
			Skill( 'Silent Strike'  , 'Chance when hitting to do more damage.'               , 8, 0 ),
			Skill( 'Sneak Attack'   , 'Chance when hitting to do a lot more damage.'         , 8, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.giveWeapon( wcsPlayer, 'usp' )

		lvl = skills['Cloak of Hiding']
		if ( lvl > 0 ):
			invis = 0.5 + ( lvl * 0.05 )
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, 1 - invis, False )
			self.helper.raceTell( self, wcsPlayer, '#goodCloak of Hiding #defsets you to #good%i%% #definvis.' % round((1 - invis) * 100 ) )

		lvl = skills['Undead Legs']
		if ( lvl > 0 ):
			speed = 1.1 + ( lvl * .05 )
			self.RaceTools.setSpeed( wcsPlayer, speed )
			self.helper.raceTell( self, wcsPlayer, '#goodUndead Legs #defgives you #good%i%% #defbonus movement speed.' % round(speed*100) )

		lvl = skills['Silent Strike']
		if ( lvl > 0 ):
			chance      = 12 + lvl # 20%
			bonusDamage = 0.8
			self.helper.raceTell( self, wcsPlayer, '#goodSilent Strike #defgives you a #good%i%% #defchance to deal #good%i%% bonus damage!' % ( chance, bonusDamage*100 ) )

		lvl = skills['Sneak Attack']
		if ( lvl > 0 ):
			chance      = 80
			bonusDamage = 0.06 + ( lvl * .03 )
			self.helper.raceTell( self, wcsPlayer, '#goodSneak Attack #defgives you a #good%i%% #defchance to deal #good%i%% bonus damage!' % ( chance, bonusDamage*100 ) )


	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us

		weapon = ev['weapon']
		damage = ev['dmg_health']

		lvl = skills['Sneak Attack']
		if ( lvl > 0 and weapon == 'weapon_usp' ):
			chance = 12 + lvl # 20%
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				bonusDamage = damage * 0.8
				self.helper.raceTell( self, wcsAttacker, '#goodSneak Attack #defdeals #good%i #defbonus damage!' % round(bonusDamage) )
				return ( damage + bonusDamage )

		lvl = skills['Silent Strike']
		if ( lvl > 0 and weapon == 'weapon_usp' ):
			# 40 / 100
			chance = 80
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				bonusDamage = damage * ( 0.06 + ( lvl * .03 ) )
				self.helper.raceTell( self, wcsAttacker, '#goodSilent Strike #defdeals #good%i #defbonus damage!' % round(bonusDamage) )
				return ( damage + bonusDamage )
