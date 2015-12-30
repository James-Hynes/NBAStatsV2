from lib.DataGather import *
from json import dump, JSONDecodeError
from statistics import stdev, StatisticsError
import concurrent.futures


class ManageData:
    @staticmethod
    def write_data_to_json_file(fp, data, form=True):
        try:
            with open(fp, 'w') as json_file:
                try:
                    if form:
                        dump(data, json_file, sort_keys=True, indent=4, ensure_ascii=False)
                    else:
                        dump(data, json_file)
                except JSONDecodeError:
                    return None
        except FileNotFoundError:
            return None


class TechnicalEffects(ManageData):
    def __init__(self, season):
        self.season = season
        self.fp = 'Data/tech_runs/{}tech_runs.json'.format(season)
        self.list_games = GameList(season=self.season).list
        self.write_data_to_json_file(self.fp, self.get_runs_each_game())

    def get_runs_each_game(self):
        all_games = []
        executor = concurrent.futures.ThreadPoolExecutor(10)
        r_list = [executor.submit(self.create_json_object, game=game, full_list=all_games) for game in self.list_games]
        concurrent.futures.wait(r_list)
        return all_games

    def create_json_object(self, game, full_list):
        g = Game(game, Season=self.season)
        print(game)
        full_list.append({'game': game, 'techs': [self.get_margin_change(tech_run, g) for tech_run in
                                                  self.get_all_tech_runs(g)]})

    def get_all_tech_runs(self, game_obj):
        return [self.get_plays_after_tech(self.neutral_descriptions(game_obj.list),
                                          [tech['PCTIMESTRING'], tech['PERIOD']]) for tech in game_obj.tech_list]

    def get_plays_after_tech(self, game, tech_info, time_after=240):
        plays_list = []
        for item in game[0]:
            if (item['PERIOD'] == tech_info[1]) and self.convert_time_to_seconds(tech_info[0]) >= \
                    self.convert_time_to_seconds(item['PCTIMESTRING']) >= self.convert_time_to_seconds(tech_info[0]) - \
                    time_after:
                plays_list.append(item)

        return plays_list

    @staticmethod
    def get_margin_change(tech_run, game):
        team_tech = tech_run[0]['PLAYER1_TEAM_ABBREVIATION']
        change_margin = -1 if team_tech == game.away_home[0] else 1
        orig_margin = [item['SCOREMARGIN'] for item in tech_run if item['SCOREMARGIN']][0]
        final_margin = [item['SCOREMARGIN'] for item in tech_run[::-1] if item['SCOREMARGIN']][0]
        orig_score = [item['SCORE'] for item in tech_run if item['SCORE']][0]
        final_score = [item['SCORE'] for item in tech_run[::-1] if item['SCORE']][0]

        if orig_margin == 'TIE':
            orig_margin = 0
        if final_margin == 'TIE':
            final_margin = 0

        return {'team': team_tech, 'margin_change': (int(final_margin) * change_margin) -
                                                    (int(orig_margin) * change_margin), 'original_score': orig_score,
                'final_score': final_score, 'time_committed': tech_run[0]['PCTIMESTRING']}

    @staticmethod
    def neutral_descriptions(play_list):
        for item in play_list[0]:
            if not item['HOMEDESCRIPTION'] and not item['VISITORDESCRIPTION']:
                item['NEUTRALDESCRIPTION'] = None
            elif item['VISITORDESCRIPTION']:
                item['NEUTRALDESCRIPTION'] = item['VISITORDESCRIPTION']
            elif item['HOMEDESCRIPTION']:
                item['NEUTRALDESCRIPTION'] = item['HOMEDESCRIPTION']

        return play_list

    @staticmethod
    def convert_time_to_seconds(change_time):
        sp_time = str(change_time).split(':')
        return (int(sp_time[0]) * 60) + int(sp_time[1])


class PlayerConsistencyInfo(ManageData):
    def __init__(self):
        self.player = None
        self.player_obj = None
        self.write_data_to_json_file('Data/player_consistency.json', self.collect_player_info())

    def collect_player_info(self):
        overall_obj = []
        executor = concurrent.futures.ThreadPoolExecutor(10)
        r_list = [executor.submit(self.create_json_object, player=player, full_list=overall_obj)
                  for player in AllPlayersList(IsOnlyCurrentSeason='1').list[0]]
        concurrent.futures.wait(r_list)

        return overall_obj

    @staticmethod
    def create_json_object(player, full_list):
        player_name = (player['DISPLAY_LAST_COMMA_FIRST'])
        player_obj = PlayerGameLogs(player_name)
        log_pts = [game['PTS'] for game in player_obj.list[0]]
        log_ast = [game['AST'] for game in player_obj.list[0]]
        log_reb = [game['REB'] for game in player_obj.list[0]]

        try:
            standard_dev = {'PTS': stdev(log_pts), 'AST': stdev(log_ast),
                            'REB': stdev(log_reb)}
        except StatisticsError:
            standard_dev = {'PTS': None, 'AST': None, 'REB': None}
        logs = {'PTS': log_pts, 'AST': log_ast, 'REB': log_reb}
        json_obj = {'logs': logs, 'standard_dev_logs': standard_dev, 'name': player_name,
                    'team': player['TEAM_CODE']}

        full_list.append(json_obj)


if __name__ == '__main__':
    PlayerConsistencyInfo()
