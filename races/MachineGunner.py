from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class MachineGunner( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = [ 'M249', 'Knife', 'Grenades' ]

		self.RaceColor                = '\x077E079A'
		self.RaceAbbreviation         = 'MacGunna'

		self.RaceName                 = 'Machine Gunner'
		self.RaceTypes                = ['human', 'heavy']
		self.Coder                    = 'Mini Dude & Tortoise'
		self.UltimateCooldown         = 10
		self.StartingUltimateCooldown = 5
		self.AbilityCooldown          = 1

		self.RequiredLevel            = 8 #500
		self.PlayerLimit              = 0
		self.ChangeRaceIndex          = 0

		self.SkillList = [
			Skill( 'Machine Gun' , 'Grab an M249.'                                               , 0, 0 ),
			Skill( 'Armored Suit', 'Gain up to 50 HP and 200 armor.'                             , 5, 0 ),
			Skill( 'Mixed Murder', '[Ability] Choose from a variety of bullets.'                 , 5, 0 ),
			Skill( 'Entrenchment', '[Ultimate] Bunker down for low recoil and damage resistance.', 5, 5 )
		]

	_bulletTypes = [ 'Explosive', 'Burn', 'Freeze', 'Silver' ]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		# lvl = skills['Machine Gun']
		self.RaceTools.giveWeapon( wcsPlayer, 'm249' )
		self.helper.raceTell( self, wcsPlayer, '#goodMachine Gun #defprovides you with your #goodBOOM STICK#def!' )

		lvl = skills['Armored Suit']
		if ( lvl > 0 ):
			health =  5 * lvl
			armor  = 10 * lvl

			self.RaceTools.setHealth( wcsPlayer, 100 + health )
			wcsPlayer.player.armor = 100 + armor

			self.helper.raceTell( self, wcsPlayer, '#goodArmored Suit #defgrants #good%i #defbonus health, and #good%i #defbonus armor!' % ( health, armor ) )
		
		lvl = skills['Mixed Murder']
		if ( lvl > 0 ):
			if ( not hasattr( wcsPlayer, 'infoMachineGunnerBullet' ) ):
				wcsPlayer.infoMachineGunnerBullet = 0

			self.helper.raceTell( self, wcsPlayer, '#goodMixed Muder #defYour bullet type is set to #good%s#def.' % self._bulletTypes[wcsPlayer.infoMachineGunnerBullet] )

		lvl = skills['Entrenchment']
		if ( lvl > 0 ):
			wcsPlayer.infoMachineGunnerEntrenched = 0

	def player_hurt( self, ev, skills ):
		wcsVictim = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Entrenchment']
		if ( lvl > 0 ):
			if ( wcsVictim.infoMachineGunnerEntrenched ):
				return ( ev['dmg_health'] / 2 )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Mixed Murder']
		if ( lvl > 0 ):
			bulletType = self._bulletTypes[ wcsAttacker.infoMachineGunnerBullet ]
			rand       = randint( 1, 100 )
			damage     = ev['dmg_health']

			if ( bulletType == 'Burn' ):
				chance = 5 * lvl
				if ( chance >= rand ):
					burnDamage = 10
					duration = 5
					self.RaceTools.DOT( wcsAttacker, wcsVictim, duration, burnDamage, self.Effects.Burn )
					# es.server.queuecmd( 'sm_burn #%s %s' % ( victim, duration ) )

			if ( bulletType == 'Freeze' ):
				chance = 5 * lvl
				if ( chance >= rand ):
					duration = 0.25
					self.RaceTools.freezePlayer( wcsVictim, duration )
					self.helper.raceTell( self, wcsAttacker, '#goodMixed Murder #defFroze #name%s #deffor #good%s #defseconds!' % ( wcsVictim.player.name, duration ) )
					self.helper.raceTell( self, wcsVictim  , '#name%s #defFroze you #deffor #good%s #defseconds!' % ( wcsAttacker.player.name, duration ) )

			if ( bulletType == 'Silver' ):
				race  = self.helper.races.raceList[ wcsVictim.race ]

				if ( 'undead' in race.RaceTypes ):
					chance = 5 * lvl
					if ( chance >= rand ):
						self.helper.raceTell( self, wcsAttacker, '#goodMixed Murder #graySilver Bullets #defdid #good10 #defbonus damage to #name%s#def!' % wcsVictim.player.name )
						return (damage + 10)

	def bullet_impact( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Mixed Murder']
		if ( lvl > 0 ):
			bulletType = self._bulletTypes[ wcsPlayer.infoMachineGunnerBullet ]
			rand       = randint( 1, 100 )

			if ( bulletType == 'Explosive' ):
				rand   = randint( 1, 100 )
				chance = 5 * lvl
				if ( chance >= rand ):
					x = float( ev['x'] )
					y = float( ev['y'] )
					z = float( ev['z'] ) - 50

					self.Effects.explosion( x, y, z )

					targets = '#ct,#alive' if ( wcsPlayer.player.teamid == 2 ) else '#t,#alive'
					targets = self.RaceTools.getPlayersInRangePoint( x, y, z, targets, 75 )

					damage = lvl
					for wcsTarget in targets:
						self.RaceTools.damage( wcsPlayer, wcsTarget, damage )

	def player_ability( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Mixed Murder']
		if ( lvl > 0 ):

			wcsPlayer.infoMachineGunnerBullet += 1

			if ( wcsPlayer.infoMachineGunnerBullet > len( self._bulletTypes ) - 1 ):
				wcsPlayer.infoMachineGunnerBullet = 0

			self.helper.raceTell( self, wcsPlayer, '#goodMixed Muder #defYour bullet type has been set to #good%s#def.' % self._bulletTypes[wcsPlayer.infoMachineGunnerBullet] )

			return True

		return None

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Entrenchment']
		if ( lvl > 0 ):
			# are we entrenched or not?
			if ( not wcsPlayer.infoMachineGunnerEntrenched ):
				# make sure we're on the ground
				if ( wcsPlayer.player.onGround() ):
					# and not crouched!
					if ( not es.getplayerprop( wcsPlayer.player.userid, 'CBasePlayer.localdata.m_Local.m_bDucked' ) ):
						player.freeze(1)
						x,y,z = wcsPlayer.player.location
						z -= 50
						command = 'es_xsetpos %s %s %s %s' % ( wcsPlayer, x, y, z )

						# multiple positionings to ensure you get in the ground propperly!
						es.server.queuecmd( command )
						gamethread.delayed( 0.1, es.server.queuecmd, command )
						gamethread.delayed( 0.2, es.server.queuecmd, command )
						gamethread.delayed( 0.4, es.server.queuecmd, command )
						gamethread.delayed( 0.6, es.server.queuecmd, command )
						gamethread.delayed( 0.8, es.server.queuecmd, command )
						gamethread.delayed( 1.0, es.server.queuecmd, command )

						self.helper.raceTell( self, wcsPlayer, '#goodEntrenchment #defYou are now #goodEntrenched#def, and take #good50% #defless damage!' )

						wcsPlayer.infoMachineGunnerEntrenched = True

						return True
					else:
						self.helper.raceTell( self, wcsPlayer, '#goodEntrenchment #defYou can\'t #goodEntrench #defif you\'re #goodcrouched#def!' )
						return False
				else:
					self.helper.raceTell( self, wcsPlayer, '#goodEntrenchment #defYou can\'t #goodEntrench #defif you\'re not on the #goodground#def!' )
					return False
			else:
				wcsPlayer.player.freeze(0)
				x,y,z = wcsPlayer.player.location
				z    += 70

				es.server.queuecmd( 'es_xsetpos %s %s %s %s' % ( wcsPlayer, x, y, z ) )

				self.helper.raceTell( self, wcsPlayer, '#goodEntrenchment #defYou are no longer #goodEntrenched!' )

				wcsPlayer.infoMachineGunnerEntrenched = False

				return True

	def weapon_fire( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Entrenchment']
		if ( lvl > 0 ):
			if ( wcsPlayer.infoMachineGunnerEntrenched ):
				self.RaceTools.noRecoil( wcsPlayer )