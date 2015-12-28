from lib.DataGather import PlayerGameLogs, AllPlayersList
from statistics import stdev, StatisticsError
from json import dump
"""
Takes the game logs for each player in the NBA who has played 2 or more games. Then it logs the standard deviation
of their Points, Assists, and Rebounds.

"""


class PlayerConsistencyInfo:

    def __init__(self):
        self.write_player_info_to_json()

    def write_player_info_to_json(self):
        overall_obj = []
        for player in AllPlayersList(IsOnlyCurrentSeason='1').list[0]:
            self.player = (player['DISPLAY_LAST_COMMA_FIRST'])
            self.player_obj = PlayerGameLogs(self.player)
            try:
                standard_dev = {'PTS': stdev(self.log_points), 'AST': stdev(self.log_assists),
                                'REB': stdev(self.log_rebounds)}
            except StatisticsError:
                standard_dev = {'PTS': None, 'AST': None, 'REB': None}
            logs = {'PTS': self.log_points, 'AST': self.log_assists, 'REB': self.log_rebounds}
            json_obj = {'logs': logs, 'standard_dev_logs': standard_dev, 'name': self.player,
                        'team': player['TEAM_CODE']}

            overall_obj.append(json_obj)

        with open('player_consistency.json', 'w') as jsonfile:
                dump(overall_obj, jsonfile, sort_keys = True, indent = 4, ensure_ascii=False)

    @property
    def logs(self):
        return self.player_obj.list[0]

    @property
    def log_points(self):
        return [game['PTS'] for game in self.logs]

    @property
    def log_rebounds(self):
        return [game['REB'] for game in self.logs]

    @property
    def log_assists(self):
        return [game['AST'] for game in self.logs]


# PlayerConsistencyInfo()