from random import randint, uniform

import es
import spe_effects
import playerlib
import gamethread
import usermsg

class Effects( object ):
	# Effects
	# sprites/laser.vmt
	# sprites/lgtning.vmt
	# sprites/fire.vmt
	# sprites/FlyingEmber.vmt
	# sprites/smoke.vmt
	def __init__( self, helper ):
		self.helper = helper

	# Effect Methods
	def explosion( self, x, y, z, delay=0 ):
		coords = (x,y,z)
		fDelay = delay
		vDirection = (0,0,0)
		vOrigin = coords
		iModelIndex = 0
		fScale = 0.1
		iFrameRate = 20
		iFlags = 0
		iRadius = 50
		iMagnitude = 0.1
		vNormal = 0
		szMaterialType = 'C'
		spe_effects.explosion('#all', fDelay, vOrigin, iModelIndex, fScale, iFrameRate, iFlags, iRadius, iMagnitude, vNormal, szMaterialType)

	def beampoints(
		self,
		player1,
		player2,
		r,
		g,
		b,
		a,
		duration=5,
		speed=1,
		model='sprites/laser.vmt',
		delay=0,
		width=4,
		endwidth=3,
		amplitude=0,
		fadelength=0
	):
		startPlayer  = self.helper.players[ str(player1) ] # playerlib.getPlayer( player1 )
		endPlayer    = self.helper.players[ str(player2) ] # playerlib.getPlayer( player2 )

		x,y,z        = startPlayer.player.getLocation()
		x1,y1,z1     = endPlayer  .player.getLocation()

		# because its between two players, get the points closer to their chests
		z           += 40
		z1          += 40

		vStartOrigin = ( x , y , z  )
		vEndOrigin   = ( x1, y1, z1 )
		iRed         = r
		iGreen       = g
		iBlue        = b
		iAlpha       = a
		fLife        = duration
		szModelPath  = model
		iSpeed       = speed

		fDelay       = delay

		iHaloIndex   = 0
		iStartFrame  = 0
		iFrameRate   = 255
		fWidth       = width
		fEndWidth    = endwidth
		fFadeLength  = fadelength
		fAmplitude   = amplitude

		spe_effects.beamPoints( '#all', fDelay, vStartOrigin, vEndOrigin, szModelPath, iHaloIndex, iStartFrame, iFrameRate,
			fLife, fWidth, fEndWidth, fFadeLength, fAmplitude, iRed, iGreen, iBlue, iAlpha, iSpeed)

	def beamringpoint(
		self,
		player,
		r,
		g,
		b,
		a,
		duration=5,
		speed=20,
		model='sprites/fire.vmt',
		delay=0,
		startRadius=0,
		endRadius=100
	):
		wcsPlayer    = self.helper.players[str(player)] # playerlib.getPlayer( player )
		x,y,z        = wcsPlayer.player.getLocation()
		vOrigin      = ( x, y, z )

		szModelPath  = model
		fLife        = duration

		iRed         = r
		iGreen       = g
		iBlue        = b
		iAlpha       = a
		iSpeed       = speed

		fDelay       = delay

		fStartRadius = startRadius
		fEndRadius   = endRadius

		iHaloIndex   = 0
		iStartFrame  = 0
		iFrameRate   = 255
		fWidth       = 5
		iSpread      = 0
		fAmplitude   = 0.5
		iFlags       = 0

		spe_effects.beamRingPoint('#all', fDelay, vOrigin, fStartRadius, fEndRadius, szModelPath, iHaloIndex,
			iStartFrame, iFrameRate, fLife, fWidth, iSpread, fAmplitude, iRed, iGreen, iBlue, iAlpha, iSpeed, iFlags)


	# Effects
	def Burn( self, attacker, victim ):
		fDelay = 0
		x,y,z = es.getplayerlocation( victim )
		# szModelPath = 'sprites/floorfire4_.vmt'
		szModelPath = 'sprites/fire.vmt'
		# fSize = 0.25
		# fSize = 1
		# iBrightness = 255

		# spe_effects.sprite( '#all', fDelay, (x,y,z+39),       szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x+10,y+10,z+25), szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x+10,y,z+30),    szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x+10,y-10,z+15), szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x,y+10,z+25),    szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x,y-10,z+30),    szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x-10,y+10,z+15), szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x-10,y,z+25),    szModelPath, fSize, iBrightness )
		# spe_effects.sprite( '#all', fDelay, (x-10,y-10,z+20), szModelPath, fSize, iBrightness )

		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x,y,z+60),       szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x+20,y+20,z+50), szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x+20,y,z+40),    szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x+20,y-20,z+30), szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x,y+20,z+50),    szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x,y-20,z+40),    szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x-20,y+20,z+30), szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x-20,y,z+50),    szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )
		# spe_effects.sprite( '#all', uniform( 0, 0.2 ), (x-20,y-20,z+40), szModelPath, uniform( 0.5, 0.8 ), randint( 175, 255 ) )

		# random fire is nice, hopefully not somthing that causes lag
		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		x1, y1, z1 = ( x + randint( -30, 30 ), y + randint( -30, 30 ), z + randint( 20, 80 ) )
		spe_effects.sprite( '#all', uniform( 0, 0.3 ), ( x1, y1, z1 ), szModelPath, uniform( 0.5, 1 ), randint( 50, 255 ) )

		# usermsg.fade( victim.userid, 1, 500, 0, 255, 50, 50, 75 )

	def Explode( self, player, distance ):
		# player = playerlib.getPlayer(player)
		wcsPlayer = self.helper.players[str(player)]

		# Effect
		self.beamringpoint( wcsPlayer, 255, 0, 0, 255, 0.5, 1000, 'sprites/lgtning.vmt',   0, 0, distance )
		self.beamringpoint( wcsPlayer, 255, 0, 0, 255, 0.5, 1000, 'sprites/lgtning.vmt', 0.2, 0, distance )
		self.beamringpoint( wcsPlayer, 255, 0, 0, 255, 0.5, 1000, 'sprites/lgtning.vmt', 0.4, 0, distance )
		self.beamringpoint( wcsPlayer, 255, 0, 0, 255, 0.5, 1000, 'sprites/lgtning.vmt', 0.6, 0, distance )
		# beamringpoint( player, 255, 0, 0, 255, 0.5, 1000, 'sprites/lgtning.vmt', 0.8, 0, distance )

		# Random Sound
		rand = randint(1,6)
		if   rand == 1 : sound = 'weapons\explode3.wav'
		elif rand == 2 : sound = 'weapons\explode4.wav'
		elif rand == 3 : sound = 'weapons\explode5.wav'
		elif rand == 4 : sound = 'weapons\mortar\mortar_explode1.wav'
		elif rand == 5 : sound = 'weapons\mortar\mortar_explode2.wav'
		elif rand == 6 : sound = 'weapons\mortar\mortar_explode3.wav'

		# 0.0 - 1.0: 0 is whole server
		es.emitsound( 'player', wcsPlayer.player.userid, sound, 1.0, 0.75 )