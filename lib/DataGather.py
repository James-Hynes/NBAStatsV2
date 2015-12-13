import requests
import simplejson.scanner


class Stat:
    """Super class to handle general stat gathering from stats.nba.com


    """

    def __init__(self, url, base_params, args, player=None, team=None):
        """Get data and sort it into a list of stat values

        :param url: The JSON library to retrieve data from -- provided by the subclasses
        :param base_params: The required parameters for the JSON request -- provided by the subclasses
        :param args: User-defined arguments to push in the request
        :param player: User-defined argument to define a specific player to get statistics for -- only used some classes
        :param team: User-defined argument to define a specific team to get statistics for -- only used in some classes
        :return: None
        """
        if player:
            base_params['PlayerID'] = self.get_id_from_player(player)
        if team:
            base_params['TeamID'] = self.get_id_from_team(team)
        self.data = self.get_data(url, self.create_params(base_params, args))
        self.list = self.zip_data_as_list()

    def zip_data_as_list(self):
        """Takes the data that has already been received and converts it into [dict] format

        :return: A list of statistics sorted into a list
        """
        if self.data:
            try:
                values = self.data['resultSet']['rowSet']
                headers = self.data['resultSet']['headers']
                return [dict(zip(headers, value)) for value in values]
            except KeyError:
                try:
                    val_list = []
                    for item in self.data['resultSets']:
                        try:
                            values = item['rowSet']
                            headers = item['headers']
                            val_list.append([dict(zip(headers, value)) for value in values])
                        except TypeError:
                            values = (self.data['resultSets']['rowSet'])
                            headers = (self.data['resultSets']['headers'][1])
                            print(headers)
                            return [dict(zip(headers['columnNames'], value)) for value in values]
                    return val_list
                except KeyError:
                    return None

    @staticmethod
    def get_data(url, params):
        """Get the data from the JSON library provided

        :param url: The JSON library to retrieve data from -- provided by the subclasses
        :param params: The required parameters for the JSON request -- provided by the subclasses
        :return: The actual unsorted data from the JSON library
        """
        try:
            return requests.get(url, params).json()
        except requests.RequestException:
            return None
        except simplejson.scanner.JSONDecodeError:
            print(requests.get(url, params).url)
            print('Something went wrong with the parameters or URL')
            return None

    @staticmethod
    def remove(change_list, index):
        """Remove an item from the list

        :param change_list: the list that will be changed
        :param index: The index of the removed item
        :return: The list post-removal
        """
        if change_list:
            try:
                change_list[index] = None
                return change_list
            except KeyError:
                return None

    @staticmethod
    def get(get_list, index):
        """Get a certain item from the given list

        :param get_list: the list that will provide the item
        :param index: The index of the item
        :return: The item you are receiving
        """
        if get_list:
            try:
                return get_list[index]
            except KeyError:
                return None

    @staticmethod
    def get_id_from_player(player):
        """Method to convert a player's name into their player ID -- used for all player stats

        :param player: Name of the player, can be provided in either FirstName LastName format, or LastName, FirstName
        :return: The ID of the specified player
        """
        if not player.__contains__(','):
            player = '{}, {}'.format(player.split(' ')[1], player.split(' ')[0])
        try:
            with open('playerlist.txt', 'r') as player_file:
                try:
                    return [line.split(': ')[1].replace('\n', '') for line in player_file
                            if line.__contains__(player)][0]
                except IndexError:
                    return None
        except FileNotFoundError:
            return None

    @staticmethod
    def get_id_from_team(team):
        """Method to convert a team's name into their team ID -- used for all team stats

        :param team: Name of the team
        :return: The ID of the team
        """
        try:
            with open('teamlist.txt', 'r') as team_file:
                try:
                    return [line.split(': ')[1].replace('\n', '') for line in team_file if line.__contains__(team)][0]
                except IndexError:
                    return None
        except FileNotFoundError:
            return None

    @staticmethod
    def create_params(base_params, args):
        """Method to take any user-specified parameters and insert them into the base_params, used before every request

        :param base_params: The original parameters as provided by the subclass
        :param args: The user-specified parameters
        :return: The parameters - with the user specified ones changed
        """
        for key in args.keys():
            if key in base_params:
                base_params[key] = args[key]

        return base_params


class LeagueLeaders(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00', 'PerMode': 'PerGame', 'Scope': 'S', 'Season': '2015-16',
                  'SeasonType': 'Regular Season', 'StatCategory': 'PTS'}

        super().__init__('http://stats.nba.com/stats/leagueleaders?', params, kwargs)


class AllPlayersList(Stat):

    def __init__(self, **kwargs):
        params = {'IsOnlyCurrentSeason': '0', 'LeagueID': '00', 'Season': '2015-16'}
        super().__init__('http://stats.nba.com/stats/commonallplayers?', params, kwargs)
        self.write_to_file()

    def write_to_file(self):
        if self.list:
            try:
                with open('playerlist.txt', 'w') as player_list:
                    for player in list(self.list):
                        player_list.write('{}: {}\n'.format(player['DISPLAY_LAST_COMMA_FIRST'], player['PERSON_ID']))
            except FileNotFoundError:
                return None
            except KeyError:
                return None


class GeneralPlayerStats(Stat):

    def __init__(self, player, **kwargs):
        params = {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
                  'MeasureType': 'Base', 'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0',
                  'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/playerdashboardbygeneralsplits?', params, kwargs, player=player)


class PlayerShotTracking(Stat):

    def __init__(self, player, **kwargs):
        params = {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
                  'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'TeamID': '0', 'Season': '2015-16', 'SeasonSegment': '',
                  'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/playerdashptshots?', params, kwargs, player=player)


class LeaguePlayerNormalStats(Stat):

    def __init__(self, **kwargs):
        params = {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
                  'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0',
                  'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'OpponentTeamID': '0',
                  'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
                  'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N', 'Season': '2015-16',
                  'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '', 'StarterBench': '',
                  'TeamID': '0', 'VsConference': '', 'VsDivision': '', 'Weight': ''}
        super().__init__('http://stats.nba.com/stats/leaguedashplayerstats?', params, kwargs)
        print(self.list)

    """
    # TODO: FIX THIS LATER
    def sort_list(self, stat):
        try:
            return sorted([item for item in self.list[0]], key=lambda x: item[stat])
        except IndexError:
            return None
        except AttributeError:
            return None
    """


class LeaguePlayerClutchStats(Stat):

    def __init__(self, **kwargs):
        params = {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
                  'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0',
                  'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'OpponentTeamID': '0',
                  'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
                  'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N', 'Season': '2015-16',
                  'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '', 'StarterBench': '',
                  'TeamID': '0', 'VsConference': '', 'VsDivision': '', 'Weight': '', 'AheadBehind': 'Ahead or Behind',
                  'ClutchTime': 'Last 5 Minutes', 'PointDiff': '5'}
        super().__init__('http://stats.nba.com/stats/leaguedashplayerclutch?', params, kwargs)

        print(self.list[0][0])

"""

class LeaguePlayerShotStats(Stat):

    def __init__(self, **kwargs):
        params = {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
                  'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0',
                  'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'OpponentTeamID': '0',
                  'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
                  'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N', 'Season': '2015-16',
                  'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '', 'StarterBench': '',
                  'TeamID': '0', 'VsConference': '', 'VsDivision': '', 'Weight': '', 'AheadBehind': 'Ahead or Behind',
                  'ClutchTime': 'Last 5 Minutes', 'PointDiff': '5', 'DistanceRange': '5ft Range'}
        super().__init__('http://stats.nba.com/stats/leaguedashplayershotlocations?', params, kwargs)

        print(self.list[0])

# TODO: fix the problem with the above class -- the problem is that instead of storing the values in individual dicts,
# they stored them in just one dict, which breaks the last part -- can be fixed by checking the length of the dict
# before I take the info.

"""


class LeaguePlayerBios(Stat):

    def __init__(self, **kwargs):
        params = {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
                  'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0',
                  'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'OpponentTeamID': '0',
                  'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
                  'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N', 'Season': '2015-16',
                  'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '', 'StarterBench': '',
                  'TeamID': '0', 'VsConference': '', 'VsDivision': '', 'Weight': '', 'AheadBehind': 'Ahead or Behind',
                  'ClutchTime': 'Last 5 Minutes', 'PointDiff': '5', 'DistanceRange': '5ft Range'}
        super().__init__('http://stats.nba.com/stats/leaguedashplayerbiostats?', params, kwargs)

        print(self.list[0][0])


class LeagueGameLogs(Stat):

    def __init__(self, **kwargs):
        params = {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
                  'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0',
                  'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0', 'OpponentTeamID': '0',
                  'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
                  'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N', 'Season': '2015-16',
                  'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '', 'StarterBench': '',
                  'TeamID': '0', 'VsConference': '', 'VsDivision': '', 'Weight': '', 'AheadBehind': 'Ahead or Behind',
                  'ClutchTime': 'Last 5 Minutes', 'PointDiff': '5', 'DistanceRange': '5ft Range', 'Counter': '1000',
                  'Direction': 'DESC',  'PlayerOrTeam': 'P', 'Sorter': 'PTS'}
        super().__init__('http://stats.nba.com/stats/leaguegamelog?', params, kwargs)

        print(self.list[0][0])


class PlayerReboundTracking(Stat):

    def __init__(self, player, **kwargs):
        params = {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
                  'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'TeamID': '0', 'Season': '2015-16', 'SeasonSegment': '',
                  'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/playerdashptreb?', params, kwargs, player=player)


class PlayerPassTracking(Stat):

    def __init__(self, player, **kwargs):
        params = {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
                  'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'TeamID': '0', 'Season': '2015-16', 'SeasonSegment': '',
                  'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/playerdashptpass?', params, kwargs, player=player)


class PlayerDefenseTracking(Stat):

    def __init__(self, player, **kwargs):
        params = {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
                  'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'TeamID': '0', 'Season': '2015-16', 'SeasonSegment': '',
                  'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/playerdashptshotdefend?', params, kwargs, player=player)


class PlayerShotLogTracking(Stat):

    def __init__(self, player, **kwargs):
        params = {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
                  'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'TeamID': '0', 'Season': '2015-16', 'SeasonSegment': '',
                  'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/playerdashptshotlog?', params, kwargs, player=player)


class PlayerReboundLogTracking(Stat):

    def __init__(self, player, **kwargs):
        params = {'DateFrom': '', 'DateTo': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
                  'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'TeamID': '0', 'Season': '2015-16', 'SeasonSegment': '',
                  'SeasonType': 'Regular Season', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/playerdashptreboundlogs?', params, kwargs, player=player)


class PlayerGameLogs(Stat):

    def __init__(self, player, **kwargs):
        params = {'LeagueID': '00', 'Season': '2015-16', 'SeasonType': 'Regular Season'}
        super().__init__('http://stats.nba.com/stats/playergamelog?', params, kwargs, player=player)


class PlayerCareerStats(Stat):

    def __init__(self, player, **kwargs):
        params = {'LeagueID': '00', 'PerMode': 'PerGame', 'Season': '2015-16', 'SeasonType': 'Regular Season'}
        super().__init__('http://stats.nba.com/stats/playercareerstats?', params, kwargs, player=player)


class AllTeamsList(Stat):

    def __init__(self, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}

        super().__init__('http://stats.nba.com/stats/leaguedashteamstats?', params, kwargs)

        self.write_to_file()

    def write_to_file(self):
        if self.list:
            try:
                with open('teamlist.txt', 'w') as team_list:
                    for team in list(self.list[0]):
                        team_list.write('{}: {}\n'.format(team['TEAM_NAME'], team['TEAM_ID']))
            except FileNotFoundError:
                return None
            except KeyError:
                return None


class TeamGeneralStats(Stat):

    def __init__(self, team, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/teamdashboardbygeneralsplits?', params, kwargs, team=team)


class TeamLineupStats(Stat):

    def __init__(self, team, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameID': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': '', 'GroupQuantity': '5'}
        super().__init__('http://stats.nba.com/stats/teamdashlineups?', params, kwargs, team=team)


class TeamPlayerStats(Stat):

    def __init__(self, team, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/teamplayerdashboard?', params, kwargs, team=team)

        print(self.list[1][0])


class TeamOnOffStats(Stat):

    def __init__(self, team, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'Per48',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/teamplayeronoffdetails?', params, kwargs, team=team)


class TeamGameLogs(Stat):

    def __init__(self, team, **kwargs):
        params = {'LeagueID': '00', 'Season': '2015-16', 'SeasonType': 'Regular Season'}
        super().__init__('http://stats.nba.com/stats/teamgamelog?', params, kwargs, team=team)

        print(self.list[0][0])


class TeamHistoryStats(Stat):

    def __init__(self, team, **kwargs):
        params = {'LeagueID': '00', 'PerMode': 'Totals', 'SeasonType': 'Regular Season'}
        super().__init__('http://stats.nba.com/stats/teamyearbyyearstats?', params, kwargs, team=team)

        print(self.list[0][0])


class TeamShotTracking(Stat):

    def __init__(self, team, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/teamdashptshots?', params, kwargs, team=team)


class TeamReboundTracking(Stat):

    def __init__(self, team, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/teamdashptreb?', params, kwargs, team=team)

        print(self.list[0])


class TeamPassTracking(Stat):

    def __init__(self, team, **kwargs):
        params = {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
                  'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': 'Base', 'Month': '0',
                  'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
                  'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
                  'Season': '2015-16', 'SeasonSegment': '', 'SeasonType': 'Regular Season', 'ShotClockRange': '',
                  'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
        super().__init__('http://stats.nba.com/stats/teamdashptpass?', params, kwargs, team=team)


class TeamRoster(Stat):

    def __init__(self, team, **kwargs):
        params = {'LeagueID': '00', 'Season': '2015-16'}
        super().__init__('http://stats.nba.com/stats/commonteamroster?', params, kwargs, team=team)


class TeamGeneralInfo(Stat):

    def __init__(self, team, **kwargs):
        params = {'LeagueID': '00', 'SeasonType': 'Regular Season', 'season': '2015-16'}
        super().__init__('http://stats.nba.com/stats/teaminfocommon?', params, kwargs, team=team)


class PlayoffPicture(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00', 'SeasonID': '22015'}
        super().__init__('http://stats.nba.com/stats/playoffpicture?', params, kwargs)


class FranchiseHistory(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00'}
        super().__init__('http://stats.nba.com/stats/franchisehistory?', params, kwargs)

        print(self.list[1][0])


class DraftCombineGeneralStats(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00', 'SeasonYear': '2015-16'}
        super().__init__('http://stats.nba.com/stats/draftcombinestats?', params, kwargs)

        print(self.list[0][0])


class DraftCombineSpotUpStats(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00', 'SeasonYear': '2015-16'}
        super().__init__('http://stats.nba.com/stats/draftcombinespotshooting?', params, kwargs)

        print(self.list[0][0])


class DraftCombineNonStationaryStats(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00', 'SeasonYear': '2015-16'}
        super().__init__('http://stats.nba.com/stats/draftcombinenonstationaryshooting?', params, kwargs)

        print(self.list[0][0])


class DraftCombineStrengthAgilityStats(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00', 'SeasonYear': '2015-16'}
        super().__init__('http://stats.nba.com/stats/draftcombinedrillresults?', params, kwargs)

        print(self.list[0][0])


class DraftCombineBodyStats(Stat):

    def __init__(self, **kwargs):
        params = {'LeagueID': '00', 'SeasonYear': '2015-16'}
        super().__init__('http://stats.nba.com/stats/draftcombineplayeranthro?', params, kwargs)

        print(self.list[0][0])


class DraftHistory(Stat):

    def __init__(self, **kwargs):
        params = {'College': '', 'LeagueID': '00', 'OverallPick': '', 'RoundNum': '', 'RoundPick': '', 'Season': '2015',
                  'TeamID': '0', 'TopX': ''}
        super().__init__('http://stats.nba.com/stats/drafthistory?', params, kwargs)

        print(self.list[0][0])


# Draft Combine Stats work from my end -- but the stats are very incomplete from an NBA end, many of the values are left
# unfilled -- so don't expect these to work very well for real usage.


class NBAScores(Stat):

    def __init__(self, **kwargs):
        params = {'DayOffset': '', 'LeagueID': '00'}
        super().__init__('http://stats.nba.com/stats/scoreboardV2?', params, kwargs)

    @staticmethod
    def get_date():
        return None

# ~~ News Stuff ~~ #


class News:

    def __init__(self, url, base_params=None):
        self.data = self.get_data(url, base_params)
        self.list = self.create_sorted_news()

    def create_sorted_news(self):
        if self.data:
            try:
                return [{'Caption': item['ListItemCaption'], 'Image': item['ListItemImageURL'],
                         'Date': item['ListItemPubDate'], 'Link': item['ListItemLink'],
                         'Abstract': item['ListItemAbstract']} for item in self.data['ListItems']]
            except KeyError:
                return None
            except IndexError:
                return None
            except AttributeError:
                return None

    @staticmethod
    def get_data(url, params):
        try:
            return requests.get(url, params).json()
        except requests.RequestException:
            return None
        except simplejson.scanner.JSONDecodeError:
            print(requests.get(url, params).url)
            print('Something went wrong with the parameters or URL')
            return None


class BeyondTheNumbers(News):

    def __init__(self):
        super().__init__('http://stats.nba.com/feeds/StatsBeyondTheNumbersV2-594371/json.js')


class StatHeadlines(News):

    def __init__(self):
        super().__init__('http://stats.nba.com/feeds/StatsV2Headlnes-589800/json.js')


class StatsGlossary(News):

    def __init__(self):
        super().__init__('http://stats.nba.com/feeds/statsv2-glossary-585341/json.js')


class StatsSynergyIntro(News):

    def __init__(self):
        super().__init__('http://stats.nba.com/feeds/StatsV2Synergy-618597/json.js')


class HistoricalStats(News):

    def __init__(self):
        super().__init__('http://stats.nba.com/feeds/StatsV2History-589801/json.js')

        print(self.list[0])


# For some reason, it seems as if the NBA/people maintaining this site have stopped updating the box score stuff
# So it's stuck on November 25th...

# EDIT: FIXED AS OF 12/8/15


class BoxScores(News):

    def __init__(self):
        super().__init__('http://stats.nba.com/feeds/StatsV2BoxScores-589802/json.js')

        print(self.list[0])


class ShotCharts(News):

    def __init__(self):
        super().__init__('http://stats.nba.com/feeds/NBAStatsShotCharts-559380/json.js')

        print(self.list[0])


# ~~ Reddit Highlights/News/Updates Stuff ~~ #


class Subreddit:

    def __init__(self):
        pass


class Post:

    def __init__(self, info):
        self.info = info


class Highlight(Post):

    def __init__(self, info):
        super().__init__(info)


class NewsPost(Post):

    def __init__(self, info):
        super().__init__(info)


class Update(Post):

    def __init__(self, info):
        super().__init__(info)


# ~~ Play By Play Stuff ~~ #

class GameList(Stat):

    def __init__(self, **kwargs):
        params = {'Counter': '1000', 'Direction': 'DESC', 'LeagueID': '00', 'PlayerOrTeam': 'T', 'Season': '2015-16',
                  'SeasonType': 'Regular Season', 'Sorter': 'PTS'}
        super().__init__('http://stats.nba.com/stats/leaguegamelog?', params, kwargs)

        self.list = self.remove_duplicates(self.list[0])

    @staticmethod
    def remove_duplicates(game_list):
        fixed_list = []
        if game_list:
            for item in game_list:
                if not item['GAME_ID'] in fixed_list:
                    fixed_list.append(item['GAME_ID'])

        return fixed_list


class Game(Stat):

    def __init__(self, gameID, **kwargs):
        params = {'EndPeriod': '10', 'EndRange': '55800', 'GameID': gameID, 'RangeType': '2', 'Season': '2015-16',
                  'SeasonType': 'Regular Season', 'StartPeriod': '1', 'StartRange': '0'}
        super().__init__('http://stats.nba.com/stats/playbyplayv2?', params, kwargs)

    @property
    def tech_list(self):
        tech_list = []
        for item in self.list[0]:
            if item['VISITORDESCRIPTION'] and item['VISITORDESCRIPTION'].__contains__('T.Foul'):
                tech_list.append(item)
            elif item['HOMEDESCRIPTION'] and item['HOMEDESCRIPTION'].__contains__('T.Foul'):
                tech_list.append(item)
        return tech_list
