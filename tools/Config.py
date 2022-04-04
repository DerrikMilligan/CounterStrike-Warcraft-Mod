class ConfigOptions( object ):
	def __init__( self ):
		# XP Rates
		self.BombPlant     = 150
		self.BombExplode   = 100
		self.BombDefuse    = 200
		self.HostageRescue = 50
		self.PlayerKill    = 100
		self.HeadShotBonus = 25
		self.KnifeBonus    = 50
		self.KillLvlBonus  = 5

		# Level Rates
		self.StartingXP     = 250
		self.ExtraPerLevel  = 125
		self.levelCapRepeat = 80

		# Item Catagory Limits
		self.ItemCatLimits = {}
		self.ItemCatLimits['Attack'] = 2
		self.ItemCatLimits['XP']     = None

values = ConfigOptions()