from ..tools.BaseClasses import baseRace, Skill

import es, playerlib, gamethread
from random import randint

class HumanAlliance( baseRace ):
	def __init__( self ):
		self.RaceAbbreviation         = 'Human'

		self.RaceName                 = 'Human Alliance'
		self.Coder                    = 'Mini Dude'
		self.RaceTypes                = ['human']
		self.UltimateCooldown         = 10
		self.StartingUltimateCooldown = 5
		
		self.PlayerLimit              = 0
		self.RequiredLevel            = 0
		self.ChangeRaceIndex          = 10

		self.SkillList = [
			Skill( 'Invisibility' , 'Makes you partially invisible.'                            , 8, 0 ),
			Skill( 'Devotion Aura', 'Gives you additional health.'                              , 8, 0 ),
			Skill( 'Bash'         , 'Gives you a chance to render an enemy immobile.'           , 8, 0 ),
			Skill( 'Teleport'     , '[Ultimate] Allows you to teleport to where you are aiming.', 8, 8 )
		]

	def player_spawn( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Invisibility']
		if ( lvl > 0 ):
			invis = .2 + ( lvl * .04 )
			self.RaceTools.setColor( wcsPlayer, 1, 1, 1, 1 - invis )
			self.helper.raceTell( self, wcsPlayer, '#goodInvisibility #defsets you to #good%i%% #definvis.' % int((1 - invis) * 100 ) )

		lvl = skills['Devotion Aura']
		if ( lvl > 0 ):
			health = lvl * 5
			self.RaceTools.setHealth( wcsPlayer, 100+health )
			self.helper.raceTell( self, wcsPlayer, '#goodDevotion Aura #defsets gants you #good%i #defbonus health.' % health )

	def player_attack( self, ev, skills ):
		wcsAttacker = self.helper.players[ str(ev['attacker']) ] # us
		wcsVictim   = self.helper.players[ str(ev['userid'  ]) ]

		lvl = skills['Bash']
		if ( lvl > 0 ):
			chance = 10 + ( lvl * 3 )
			rand   = randint( 1, 100 )

			if ( chance >= rand ):
				freeze = .3

				self.RaceTools.freezePlayer( wcsVictim, freeze )

				self.helper.raceTell( self, wcsAttacker, '#goodBash #deffreezes #good%s #deffor #good%s #defseconds.' % ( wcsVictim.player.name  , freeze ) )
				self.helper.raceTell( self, wcsVictim  , '#goodBash #deffreezes #good%s #deffor #good%s #defseconds.' % ( wcsAttacker.player.name, freeze ) )

	def player_ultimate( self, ev, skills ):
		wcsPlayer = self.helper.players[ str(ev['userid']) ]

		lvl = skills['Teleport']
		if ( lvl > 0 ):
			force  = 400 + ( lvl * 75 )
			self.RaceTools.pushToViewCoords( wcsPlayer, force )
			return True
