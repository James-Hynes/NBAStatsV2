import requests
import simplejson.scanner

class Stat:

    def __init__(self, url, base_params, args):

        self.data = self.get_data(url, self.create_params(base_params, args))
        self.list = self.zip_data_as_list()

    def get_data(self, url, params):
        try:
            return requests.get(url, params).json()
        except requests.RequestException:
            return None
        except simplejson.scanner.JSONDecodeError:
            return None

    def create_params(self, base_params, args):
        for key in args.keys():
            if key in base_params:
                base_params[key] = args[key]

        return base_params

    def get(self, list, index):
        if list:
            try:
                return list[index]
            except KeyError:
                return None

    def remove(self, list, index):
        if list:
            try:
                list[index] = None
                return list
            except KeyError:
                return None
    def zip_data_as_list(self):
        if self.data:
            try:
                values = self.data['resultSet']['rowSet']
                headers = self.data['resultSet']['headers']
                return [dict(zip(headers, value)) for value in values]
            except KeyError:
                try:
                    values = self.data['resultSets'][0]['rowSet']
                    headers = self.data['resultSets'][0]['headers']
                    return [dict(zip(headers, value)) for value in values]
                except KeyError:
                    return None

class LeagueLeaders(Stat):

    def __init__(self, **kwargs):
        params = { 'LeagueID': '00', 'PerMode': 'PerGame', 'Scope': 'S', 'Season': '2015-16',
                   'SeasonType': 'Regular Season', 'StatCategory': 'PTS' }

        super().__init__('http://stats.nba.com/stats/leagueleaders?', params, kwargs)

class AllPlayersList(Stat):

    def __init__(self, **kwargs):
        params = { 'IsOnlyCurrentSeason': '0', 'LeagueID': '00', 'Season': '2015-16'}
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
        pass
        #super().__init__()
