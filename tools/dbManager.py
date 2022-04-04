# import es # only for es.msg
import sqlite3

class DatabaseManager( object ):

	def __init__( self, helper ):

		# save the helper object for later
		self.helper = helper

		# open the connection to the databse
		self.connection = sqlite3.connect('cstrike/addons/eventscripts/wcs/data/playerData.db')

		# setup the cursor
		self.cursor = self.connection.cursor()

	def __del__( self ):
		self.save()
		self.cursor.close()
		self.connection.close()

	# commit database changes
	def save( self ):
		self.connection.commit()

	# execute a query on the DB
	def Query( self, query, values=None ):
		if values == None:
			self.cursor.execute(query)
			self.connection.commit()
		else:
			self.cursor.execute(query, values)
			self.connection.commit()

	'''
	|=====================================================================
	|	Player Table Functions
	|=====================================================================
	'''
	def AddPlayer( self, steamid, race ):
		'''
		Add the player the to database, if he's not already there,
		also initialiize the xp for that race
		'''
		self.Query( '''INSERT INTO player ( steam_id, current_race )
                       SELECT ?, race.id
                       FROM race
                       WHERE race.name = ?
                       AND NOT EXISTS ( SELECT 1 FROM player WHERE steam_id = ? );''', ( steamid, race, steamid ))

		self.InitializeXP( steamid ) #, 'Zergling', 11 )

	'''
	|=====================================================================
	|	Race Table Functions
	|=====================================================================
	'''
	def AddRace( self, race ):
		'''
		Add the race to the database if it's not present
		'''
		self.Query( '''INSERT INTO race ( name )
                       SELECT ?
                       WHERE NOT EXISTS ( SELECT 1 FROM race WHERE name = ? )''', ( race, race ) )

	'''
	|=====================================================================
	|	XP Table Functions
	|=====================================================================
	'''
	def InitializeXP( self, steamid, race=None, level=0 ):
		'''
		Initialize the xp for a race, if the xp entry does not already exist
			@param race  - Pass a RaceName, or None to use the players current race
			@param level - Level to initialize the race to
		'''
		if ( race == None ):
			self.Query( '''INSERT INTO xp ( player_id, race_id, xp, level, skill_1, skill_2, skill_3, skill_4, skill_5, skill_6, skill_7, skill_8, skill_9, skill_10 )
                           SELECT p.id, p.current_race, 0, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                           FROM player p
                           WHERE p.steam_id = ?
                           AND NOT EXISTS ( SELECT 1 FROM xp WHERE xp.player_id = p.id AND xp.race_id = p.current_race )''', ( level, steamid ) )
		else:
			self.Query( '''INSERT INTO xp ( player_id, race_id, xp, level, skill_1, skill_2, skill_3, skill_4, skill_5, skill_6, skill_7, skill_8, skill_9, skill_10 )
                           SELECT p.id, r.id, 0, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                           FROM player p
                           LEFT JOIN race r ON r.name = ?
                           WHERE p.steam_id = ?
                           AND NOT EXISTS ( SELECT 1 FROM xp WHERE xp.player_id = p.id AND xp.race_id = p.current_race )''', ( level, race, steamid ) )

	def UpdatePlayerRace( self, steamid, race ):
		'''
		Update the players cuurent race
		'''
		self.Query( '''UPDATE player
                       SET current_race = ( SELECT id FROM race WHERE name = ? )
                       WHERE steam_id = ?''',
                       ( race, steamid ) )

		self.InitializeXP( steamid, race )

	def UpdateRaceXP( self, playerID, raceID, xp, level, skillPoints ):
		'''
		Update the xp values for a given player on a specific race
			@param playerID    - The player.id
			@param raceID      - The race.id
			@param xp          - The new XP values
			@param level       - The new level
			@param skillPoints - The new set of skill points as a tuple
		'''
		self.Query( '''UPDATE xp set
                         xp       = ?,
                         level    = ?,
                         skill_1  = ?,
                         skill_2  = ?,
                         skill_3  = ?,
                         skill_4  = ?,
                         skill_5  = ?,
                         skill_6  = ?,
                         skill_7  = ?,
                         skill_8  = ?,
                         skill_9  = ?,
                         skill_10 = ?
                       WHERE
                         player_id = ? AND
                         race_id   = ?''',
                       ( xp, level ) + tuple(skillPoints) + ( playerID, raceID ) )

	def SetPlayerLevel( self, playerID, raceID, level=0 ):
		'''
		Change the level for the player on a specific race
		'''
		self.Query( '''UPDATE xp SET
                         level = ?
                       WHERE
                         player_id = ? AND
                         race_id   = ?''', ( level, playerID, raceID ) )

	def GetPlayerLevel( self, playerID, race ):
		'''
		Get the players level for a specific race
		'''
		self.cursor.execute( '''SELECT level
                                FROM xp
                                WHERE
                                player_id = ? AND
                                race_id   = ( SELECT id FROM race WHERE name = ? )''',
                                ( playerID, race ) )

		result = self.cursor.fetchone()

		if result:
			return result[0]
		else:
			return 0

	def GetPlayerLevels( self, playerID ):
		'''
		Get the players levels for each race
		'''
		self.cursor.execute( '''SELECT race.name, xp.level 
                                FROM xp
                                LEFT JOIN race ON xp.race_id = race.id
                                WHERE player_id = ?''', ( playerID, ) )

		r = {}
		for row in self.cursor:
			r[row[0]] = row[1]

		return r

	'''
	|=====================================================================
	|	Multipe Table Functions
	|=====================================================================
	'''
	def GetPlayerInformation( self, steamid, race=None ):
		'''
		Load all the information for a player on a specific race
			@param race - probably won't be used
		'''
		self.cursor.execute( '''SELECT p.id,
                                       p.current_race,
                                       r.name,
                                       xp.xp,
                                       xp.level,
                                       (SELECT SUM(level) FROM xp WHERE player_id = p.id) AS total_level,
                                       xp.skill_1,
                                       xp.skill_2,
                                       xp.skill_3,
                                       xp.skill_4,
                                       xp.skill_5,
                                       xp.skill_6,
                                       xp.skill_7,
                                       xp.skill_8,
                                       xp.skill_9,
                                       xp.skill_10
                                FROM player p
                                LEFT JOIN race r ON r.id = p.current_race 
                                LEFT JOIN xp     ON xp.player_id = p.id AND xp.race_id = p.current_race
                                WHERE p.steam_id = ?''', (steamid,) )
		
		result = self.cursor.fetchone()
		if result:
			r = {
				'player_id'    : result[0],
				'race_id'      : result[1],
				'race_name'    : result[2],
				'xp'           : result[3],
				'level'        : result[4],
				'total_level'  : result[5],
				'skill_points' : [
					result[6],
					result[7],
					result[8],
					result[9],
					result[10],
					result[11],
					result[12],
					result[13],
					result[14],
					result[15]
				]
			}

			return r
