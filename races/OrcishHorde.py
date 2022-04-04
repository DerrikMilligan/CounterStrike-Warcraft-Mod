from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint, choice

class OrcishHorde( baseRace ):
	def __init__( self ):
		self.RaceAbbreviation         = 'Orc'

		self.RaceName                 = 'Orcish Horde'
		self.RaceTypes                = [ 'humanoid', 'orc', 'goblin' ]
		self.Coder                    = 'Tortoise & Mini Dude'
		self.UltimateCooldown         = 30
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 0
		self.RequiredLevel            = 0

		self.SkillList = [
			Skill( 'Critical Strike', 'Gives you a chance of doing more damage.'                                , 8, 0 ),
			Skill( 'Critical Nade'  , 'Grenades will always do more damage.'                                    , 8, 0 ),
			Skill( 'Reincarnation'  , 'Gives you a chance of respawning, with your equipment where you died.'   , 8, 0 ),
			Skill( 'Chain Lightning', '[Ultimate] Discharges a bolt of lightning that jumps on up to 4 enemies.', 8, 8 )
		]

	def round_start( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Reincarnation']
		if ( lvl > 0 ):
			# setup values for later
			wcsPlayer.infoOrcishHordeRespawnInfo = {}
			wcsPlayer.infoOrcishHordeRespawned   = False

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Critical Strike']
		if ( lvl > 0 ):
			chance      =  20 + ( lvl * 2 )
			bonusDamage = 0.2 + ( lvl * 0.03 )
			self.helper.raceTell( self, wcsPlayer, '#goodCritical Strike #defgives you a #good%i%% #defchance to do #good%i%% #defbonus damage!' % ( chance, int( bonusDamage * 100 ) ) )

		lvl = skills['Critical Nade']
		if ( lvl > 0 ):
			bonusDamage = 0.2 + ( lvl * 0.05 )
			self.helper.raceTell( self, wcsPlayer, '#goodCritical Nade #defcauses your #goodGrenades #defto do #good%i%% #defbonus damage!' % int( bonusDamage * 100 ) )

		lvl = skills['Reincarnation']
		if ( lvl > 0 ):
			chance = 40 + ( lvl * 5 )
			self.helper.raceTell( self, wcsPlayer, '#goodReincarnation #defgives you a #good%i%% #defchance to #goodRespawn #defwhen you die!' % chance )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ]
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		damage   = ev['dmg_health']
		weapon   = ev['weapon']

		lvl = skills['Critical Strike']
		if ( lvl > 0 and weapon != 'weapon_hegrenade' ):
			chance = 20 + ( lvl * 2 )
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				bonusDamage = int(damage * ( 0.2 + ( lvl * 0.03 ) ))

				self.helper.raceTell( self, wcsAttacker, '#goodCritical Strike #defhits #name%s #deffor #good%i #defbonus damage!' % ( wcsVictim.player.name, bonusDamage ) )

				return ( damage + bonusDamage )

		lvl = skills['Critical Nade']
		if ( lvl > 0 and weapon == 'weapon_hegrenade' ):
			bonusDamage = int(damage * ( 0.2 + ( lvl * 0.05 ) ))

			self.helper.raceTell( self, wcsAttacker, '#goodCritical Nade #defhits #name%s #deffor #good%i #defbonus damage!' % ( wcsVictim.player.name, bonusDamage ) )
			self.helper.raceTell( self, wcsVictim  , '#name%s #defhits you for #good%i #badCritical Nade #defdamage!' % ( wcsAttacker.player.name, bonusDamage ) )

			return ( damage + bonusDamage )

	def player_hurt( self, ev, skills ):
		wcsVictim = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Reincarnation']
		if ( lvl > 0 ):
			# make sure we've not respanwed already, and that the damage will kill us
			if ( wcsVictim.infoOrcishHordeRespawned == False and (wcsVictim.player.health - ev['dmg_health']) <= 0 ):

				# save the players weapons and location for respawning
				wcsVictim.infoOrcishHordeRespawnInfo = {
					'weapons' : wcsVictim.player.getWeaponList(),
					'location': wcsVictim.player.location
				}

	def player_death( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Reincarnation']
		if ( lvl > 0 ):
			chance = 40 + ( lvl * 5 )
			rand   = randint( 1, 100 )

			if ( chance >= rand and wcsPlayer.infoOrcishHordeRespawned == False ):

				self.helper.raceTell( self, wcsPlayer, '#goodReincarnation #defwill respawn you in #good3 #defseconds!' )

				# make sure we can't respawn again!
				wcsPlayer.infoOrcishHordeRespawned = True

				# respawn the player
				self.RaceTools.delayed( 3, self.RaceTools.respawn, wcsPlayer )

				# give him back his weapons
				for weapon in wcsPlayer.infoOrcishHordeRespawnInfo['weapons']:
					self.RaceTools.delayed( 3.2, self.RaceTools.giveWeapon, ( wcsPlayer, weapon ) )

				# reset his location
				location = wcsPlayer.infoOrcishHordeRespawnInfo['location']
				command  = 'es_xsetpos %i %s %s %s' % ( wcsPlayer, location[0], location[1], location[2] )
				self.RaceTools.delayed( 3.7, es.server.queuecmd, command )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Chain Lightning']
		if ( lvl > 0 ):
			distance = 600 + lvl * 25
			damage   = 32

			targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
			targets = self.RaceTools.getPlayersInRangePlayer( wcsPlayer, targets, distance )

			if ( len(targets) == 0 ):
				self.helper.raceTell( self, wcsPlayer, '#goodChain Lightning #defNo targets in range!' )
				return False

			else:
				# make a new list to remove people from
				targetList = list( targets )
				# loop through for the number of targets or 4 targets if there are more than 4
				for i in range(min( len(targets), 4 )):

					# pick a random target
					wcsTarget = choice( targetList )

					# remove that target from the list, so he's not picked again!
					targetList.remove( wcsTarget )

					# deal the damages
					self.RaceTools.damage( wcsPlayer, wcsTarget, damage )

					# display the effect
					self.Effects.beampoints( wcsPlayer, wcsTarget, 100, 100, 255, 255, 2, 1, 'sprites/lgtning.vmt' )

					# tell the poor guy
					self.helper.raceTell( self, wcsTarget, '#name%s #defhits your for #bad%i #defdamage with #badChain Lightning#def.' % ( wcsPlayer.player.name, damage ) )

				self.helper.raceTell( self, wcsPlayer, '#goodChain Lightning #defhits #good%i #defpeople!' % len( targets ) )

				return True
