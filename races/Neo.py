from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class Neo( baseRace ):
	def __init__( self ):
		self.WeaponsCanOnlyUse        = ['mp5navy','fiveseven','knife','grenades' ]

		self.RaceColor                = '\x0700FF33'
		self.RaceAbbreviation         = 'Neo'

		self.RaceName                 = 'Neo, The One'
		self.RaceTypes                = ['human', 'theone']
		self.Coder                    = 'MiniDude'
		self.UltimateCooldown         = 40
		self.StartingUltimateCooldown = 15

		self.PlayerLimit              = 1
		self.RequiredLevel            = 13
		self.ChangeRaceIndex          = 100

		self.isSubscriber             = 1

		self.SkillList = [
			Skill( 'Guns. Lots of Guns', 'Neo gets an MP5, and his clip has a chance to refill while shooting.', 10,  0 ),
			Skill( 'Dodge Them Bullets', 'Neo can dodge some bullets because of his training.'                 , 10,  0 ),
			Skill( 'Kung-Fu Master'    , 'Neo has trained his body do endure more pain than the average man.'  , 10,  0 ),
			Skill( 'Bullet Time'       , '[Ultimate] Neo causes everyone except himself to enter Bullet Time!' , 10, 10 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		self.RaceTools.giveWeapon( wcsPlayer, 'mp5navy' )
		self.RaceTools.giveWeapon( wcsPlayer, 'fiveseven' )

		lvl = skills['Guns. Lots of Guns']
		if ( lvl > 0 ):
			chance = 20 + ( lvl * 3 )
			self.helper.raceTell( self, wcsPlayer, '#goodGuns. Lots of Guns #defprovides a #good%i%% #defchance to #goodrefill your clip #defwhile shooting!' % chance )

		lvl = skills['Dodge Them Bullets']
		if ( lvl > 0 ):
			chance = 10 + lvl
			self.helper.raceTell( self, wcsPlayer, '#goodDodge Them Bullets #defprovides a #good%i%% #defchance to #goodevade#def!' % chance )

		lvl = skills['Kung-Fu Master']
		if ( lvl > 0 ):
			reduction = 0.1 + ( lvl * 0.02 )
			self.helper.raceTell( self, wcsPlayer, '#goodKung-Fu Master #defreduces all damage by #good%i%%#def!' % int( reduction * 100 ) )

		lvl = skills['Bullet Time']
		if ( lvl > 0 ):
			wcsPlayer.infoNeoBulletTime = False

	def weapon_fire( self, ev, skills ):
		player    = playerlib.getPlayer( ev['userid'] )
		wcsPlayer = self.helper.getPlayer( player )

		lvl = skills['Guns. Lots of Guns']
		if ( lvl > 0 ):
			chance = 20 + ( lvl * 3 )
			rand   = randint( 1, 100 )
			if ( chance >= rand and player.primary and player.clip.primary == 5 ):

				player.clip.primary = 30
				self.helper.raceTell( self, player, '#goodGuns. Lots of Guns #defhas #goodrefilled #defyour MP5!' )

	def player_hurt( self, ev, skills ):
		victim = playerlib.getPlayer( ev['userid'] )
		damage = ev['dmg_health']

		lvl = skills['Dodge Them Bullets']
		if ( lvl > 0 ):
			chance = 10 + lvl
			rand   = randint( 1, 100 )
			if ( chance >= rand ):
				self.helper.raceTell( self, victim, '#goodDodge Them Bullets #defallows you to dodge #good%i #defdamage!' % ( damage ) )
				return 0

		lvl = skills['Kung-Fu Master']
		if ( lvl > 0 ):
			reduction = 0.1 + ( lvl * 0.02 )

			return ( damage * ( 1 - reduction ) )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Bullet Time']
		if ( lvl > 0 ):
			duration  = 3 + round( lvl / 2 )

			# make sure cheats are enabled
			self.RaceTools.cheatsOn()

			# change the timescale
			es.server.queuecmd( 'es_xflags remove notify host_timescale' )
			es.server.queuecmd( 'host_timescale 0.3' )
			es.server.queuecmd( 'es_xflags add notify host_timescale' )

			# message for the whole server
			es.centermsg( 'Bullettime Activated!' )

			self.helper.raceTell( self, wcsPlayer, '#goodBullet Time #defactivated, you get #good100 #def rounds in your #goodMP5#def!' )

			# set his clip
			self.RaceTools.setPrimaryClip( wcsPlayer, 100 )

			# modify the player stats
			wcsPlayer.player.speed = 3
			self.RaceTools.setGravity( wcsPlayer, 0.5 )
			wcsPlayer.setWeaponRateOfFire( 'mp5navy'  , 0.1 )
			wcsPlayer.setWeaponRateOfFire( 'fiveseven', 0.1 )

			# set this to true, for the faster bullet shots
			wcsPlayer.infoNeoBulletTime = True

			gamethread.delayedName( duration, 'NeoUlt', self.BulletTimeOff, ( wcsPlayer ) )

			return True

	def round_end( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Bullet Time']
		if ( lvl > 0 and wcsPlayer.infoNeoBulletTime ):

			# cancel the delay
			gamethread.cancelDelayed( 'NeoUlt' )
			self.BulletTimeOff( wcsPlayer )

	def BulletTimeOff( self, wcsPlayer ):

		# revert the timescale
		es.server.queuecmd( 'es_xflags remove notify host_timescale' )
		es.server.queuecmd( 'host_timescale 1' )
		es.server.queuecmd( 'es_xflags add notify host_timescale' )

		# disable cheats
		self.RaceTools.cheatsOff()

		# server message
		es.centermsg( 'Bullettime Ending!' )

		# player info
		wcsPlayer.player.speed = 1
		self.RaceTools.setGravity( wcsPlayer, 1 )
		wcsPlayer.setWeaponRateOfFire( 'mp5navy'  , None )
		wcsPlayer.setWeaponRateOfFire( 'fiveseven', None )

		wcsPlayer.infoNeoBulletTime = False
