from ..tools.BaseClasses import baseRace, Skill

import es, playerlib
from random import randint, choice
 
class CryptLord( baseRace ):
	def __init__( self ):
		self.RaceName                 = 'Crypt Lord'
		self.RaceTypes                = ['undead', 'monster']
		self.Coder                    = 'MrCoolness & Mini Dude'
		self.UltimateCooldown         = 25
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 0
		self.RequiredLevel            = 3
		self.ChangeRaceIndex          = 50
	
		self.SkillList = [
			Skill( 'Impale'         , 'Shake and push the enemy.'                                                                      , 5, 0 ),
			Skill( 'Spiked Carapace', 'Gain armor on spawn, chance to deal mirror damage.'                                             , 5, 0 ),
			Skill( 'Carrion Beetles', 'You have a chance to deal additional damage.'                                                   , 5, 0 ),
			Skill( 'Locust Swarm'   , '[Ultimate] A swarm of locusts steals hp and armor \nfrom one random enemy [max 150hp/200armor].', 5, 0 )
		]
	
	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Spiked Carapace']
		if ( lvl > 0 ):
			wcsPlayer.player.armor = 40 * lvl
			self.helper.raceTell( self, wcsPlayer, '#goodSpiked Carapace #defgrants #good%i armor#def, and has a chance to #goodreflect damage#def!' % int( 40 * lvl ) )

	def player_hurt( self, ev, skills ):
		wcsVictim = self.helper.players[ str(ev['userid']) ]

		wcsAttacker = False
		if ( str(ev['attacker']) in self.helper.players ):
			wcsAttacker = self.helper.players[ str(ev['attacker']) ]

		lvl = skills['Spiked Carapace']
		if ( lvl > 0 and wcsAttacker ):
			# 40 / 100
			chance = 8 * lvl
			rand = randint( 1, 100 )
			if ( chance >= rand ):
				damage = ev['dmg_health']
				reflect = damage * (lvl * .08) # 40%
				self.RaceTools.damage( wcsVictim, wcsAttacker, reflect )
				self.helper.raceTell( self, wcsAttacker, '#name%s #defhits you for #bad%i #defmirror damage!' % (wcsVictim.player.name, int(reflect)) )
				self.helper.raceTell( self, wcsVictim  , '#goodSpiked Carapace #defreflects #good%i #defas mirror damage to #name%s#def!' % (int(reflect), wcsAttacker.player.name) )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Impale']
		if ( lvl > 0 ):
			# 20 / 100
			chance = lvl * 4
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				# x and y can be negative
				x = randint( -100, 100 )
				y = randint( -100, 100 )
				# we want to bump them into the air a bit, so z is only positive
				z = randint(  200, 300 )
				self.RaceTools.pushToPoint( wcsVictim, x, y, z )

		lvl = skills['Carrion Beetles']
		if ( lvl > 0 ):
			# 40 / 100
			chance = lvl * 8
			rand   = randint( 1, 100 )
			if ( chance >= rand ) :
				damage = ev['dmg_health']
				bonusdamage = damage * ( lvl * .03 )
				self.helper.raceTell( self, wcsAttacker, '#goodCarrion Beetles #defdeals #good%i #defbonus damage!' % int(bonusdamage) )
				return ( damage + bonusdamage )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Carrion Beetles']
		if ( lvl > 0 ):
			bonusdamage = 5 * lvl
			bonusarmor  = 6 * lvl
			wcsPlayer.player.health += bonusdamage
			wcsPlayer.player.armor  += bonusarmor

			# prep the team we're picking from
			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'

			# pick a random victim
			wcsVictim = choice( self.helper.getPlayerList( targets ) )

			if ( es.exists( 'userid', str(wcsVictim) ) ):
				self.RaceTools.damage( wcsPlayer, wcsVictim, bonusdamage )
				self.helper.raceTell( self, wcsVictim, '#goodLocust Swarm #defsteals #bad%i #defhp!' % bonusdamage )
				self.helper.raceTell( self, wcsPlayer, '#goodLocust Swarm #defsteals #good%i hp #defand #good%i armor#def from #bad%s#def!' % ( bonusdamage, bonusarmor, wcsVictim.player.name ) )
				return True
			else:
				self.helper.raceTell( self, wcsPlayer, '#goodLocust Swarm #deffailed to hit someone!' )
				return False
