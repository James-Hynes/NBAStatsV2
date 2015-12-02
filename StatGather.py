import requests
import simplejson.scanner


class Stat:

    def __init__(self, url, base_params, args, player=None, team=None):
        if player:
            base_params['PlayerID'] = self.get_id_from_player(player)
        if team:
            base_params['TeamID'] = self.get_id_from_team(team)
        self.data = self.get_data(url, self.create_params(base_params, args))
        self.list = self.zip_data_as_list()

    def zip_data_as_list(self):
        if self.data:
            try:
                values = self.data['resultSet']['rowSet']
                headers = self.data['resultSet']['headers']
                return [dict(zip(headers, value)) for value in values]
            except KeyError:
                try:
                    val_list = []
                    for item in self.data['resultSets']:
                        values = item['rowSet']
                        headers = item['headers']
                        val_list.append([dict(zip(headers, value)) for value in values][0])
                    return val_list
                except KeyError:
                    return None

    @staticmethod
    def get_data(url, params):
        try:
            return requests.get(url, params).json()
        except requests.RequestException:
            return None
        except simplejson.scanner.JSONDecodeError:
            print('Something went wrong with the parameters or URL')
            return None

    @staticmethod
    def remove(change_list, index):
        if change_list:
            try:
                change_list[index] = None
                return change_list
            except KeyError:
                return None

    @staticmethod
    def get(get_list, index):
        if get_list:
            try:
                return get_list[index]
            except KeyError:
                return None

    @staticmethod
    def get_id_from_player(player):
        if not player.__contains__(','):
            player = '{}, {}'.format(player.split(' ')[1], player.split(' ')[0])
        try:
            with open('playerlist.txt', 'r') as player_file:
                try:
                    return [line.split(': ')[1].replace('\n', '') for line in player_file if line.__contains__(player)][0]
                except IndexError:
                    return None
        except FileNotFoundError:
            return None

    @staticmethod
    def get_id_from_team(team):
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

"""
class TeamLineupStats(Stat):

    def __init__(self, team, **kwargs):
        params = {}
"""

print(GeneralPlayerStats('Andre Drummond').list[0])