from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint, choice

class DioBrando( baseRace ):
	def __init__( self ):
		self.RaceColor                = '\x07AA0000'
		self.RaceAbbreviation         = 'Dio'

		self.RaceName                 = 'Dio Brando'
		self.RaceTypes                = ['Human']
		self.Coder                    = 'MrCoolness'
		self.UltimateCooldown         = 25
		self.StartingUltimateCooldown = 10

		self.PlayerLimit              = 0
		self.RequiredLevel            = 5
		self.ChangeRaceIndex          = 30

		self.SkillList = [
			Skill( 'Joestar Blood', 'The blood of the Joestars grants you vitality.',  5,  0 ),
			Skill( 'Narcissistic' , 'Dio\'s agility is unmatched by any.'           ,  5,  0 ),
			Skill( 'Vampire'      , 'Drain the blood of your enemies'               ,  5,  0 ),
			Skill( 'Undying'      , 'Dio does not die.'                             ,  5,  0 ),
			Skill( 'The World!'   , '[Ultimate] Stop time.'                         , 10, 10 )
		]

	def round_start( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Undying']
		if ( lvl > 0 ):
			# set info saying we've not respawned this round yet!
			wcsPlayer.infoDioBrandoRespawned = False

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Joestar Blood']
		if ( lvl > 0 ):
			health = lvl * 10
			self.RaceTools.setHealth( wcsPlayer, 100 + health )
			self.helper.raceTell( self, wcsPlayer, '#goodJoestar Blood #defgrants you #good%i #defbonus #goodhealth#def!' % health )

		lvl = skills['Narcissistic']
		if ( lvl > 0 ):
			speed = 0.1 + ( lvl * 0.05 )
			self.RaceTools.setSpeed( wcsPlayer, 1 + speed )
			self.helper.raceTell( self, wcsPlayer, '#goodNarcissistic #defgrants you #good%i%% #defbonus movement speed!' % int(speed*100) )

		lvl = skills['Vampire']
		if ( lvl > 0 ):
			vamp = 0.05 + (lvl * 0.01)
			self.helper.raceTell( self, wcsPlayer, '#redVampire #defgrants you #good%i%% #defof the damage you deal back in #goodhealth#def.' % int(vamp*100) )

		lvl = skills['Undying']
		if ( lvl > 0 ):
			chance = 35 + ( 5 * lvl )
			self.helper.raceTell( self, wcsPlayer, '#goodUndying #def grants a #good%i%% #defchance for you to revive after you die!' % chance )

		lvl = skills['The World!']
		if ( lvl > 0 ):
			# set info that we're not in our ult yet!
			wcsPlayer.infoDioBrandoTheWorld = False

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Vampire']
		if ( lvl > 0 ):
			damage = ev['dmg_health']
			vamp = damage * ( 0.05 + (lvl * 0.01) )

			if ( wcsAttacker.player.health + vamp < 250 ):
				wcsAttacker.player.health += int( vamp )
				self.helper.raceTell( self, wcsAttacker, '#redVampire steals #good%i #defhp from #name%s#def!' % ( int(vamp), wcsVictim.player.name ) )

		lvl = skills['The World!']
		if ( lvl > 0 and wcsAttacker.infoDioBrandoTheWorld ):
			freeze = 0.1
			chance = 50
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				self.RaceTools.freezePlayer( wcsVictim, freeze )
				self.helper.raceTell( self, wcsVictim  , '#name%s #deffreezes you in place for #bad%s #defseconds.' % ( wcsAttacker.player.name, freeze ) )
				self.helper.raceTell( self, wcsAttacker, '#goodThe World! #deffreezes %s in place!' % ( wcsVictim.player.name ) )

	def player_hurt( self, ev, skills ):
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ] # us
		
		lvl = skills['Undying']
		if ( lvl > 0 ):
			damage = ev['dmg_health']

			# if the damage is enough to kill us, lets save our guns in preperation for the respawn!
			if ( wcsVictim.player.health - damage <= 0 ):

				# set some temporary info for the player, it will be removed when the map changes, or when the player leaves
				wcsVictim.infoDioBrandoWeapons = wcsVictim.player.getWeaponList()

	def player_death( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Undying']
		if ( lvl > 0 ):
			chance = lvl * 10
			rand   = randint( 1, 100)

			if ( not wcsPlayer.infoDioBrandoRespawned and chance >= rand ):
				wcsPlayer.infoDioBrandoRespawned = True

				self.helper.raceTell( self, wcsPlayer, '#goodUndying #defwill respawn you in #good3 #defseconds!' )

				gamethread.delayed( 3, self.RaceTools.respawn, wcsPlayer )

				for weapon in wcsPlayer.infoDioBrandoWeapons:
					gamethread.delayed( 3.1, self.RaceTools.giveWeapon, ( wcsPlayer, weapon ) )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['The World!']
		if ( lvl > 0 ):
			duration = 2 + ( lvl * 0.5 )

			# turn it on
			wcsPlayer.infoDioBrandoTheWorld = True

			self.helper.raceTell( self, wcsPlayer, '#goodThe World! #defmakes your shots have a #good50%% #defchance to freeze people over the next #good%i #defseconds.' % duration )

			# delay to turn off
			gamethread.delayed( duration, setattr, ( wcsPlayer, 'infoDioBrandoTheWorld', False ) )

			gamethread.delayed( duration, self.helper.raceTell, ( self, wcsPlayer, '#goodThe World! #defis ending!!!' ) )

			return True
