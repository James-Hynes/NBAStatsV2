from lib.DataGather import *
import json


class TechnicalEffects:

    def __init__(self, season, file_name):
        self.Season = season
        self.file_name_season = file_name
        self.list_games = self.get_list_games(season=self.Season)
        self.get_runs_each_game()

    def get_runs_each_game(self):
        all_games = []
        for e, game in enumerate(self.list_games):
            try:
                g = Game(game, Season=self.Season)
                print(e)
                json_object = \
                    {'game': game, 'techs': [self.get_margin_change(tech_run, g) for tech_run in self.get_all_tech_runs(g)]}
                all_games.append(json_object)
            except:
                continue

        with open('tech_runs/'+self.file_name_season+'tech_runs.json', 'w') as run_file:
            json.dump(all_games, run_file, sort_keys = True, indent = 4, ensure_ascii=False)

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
    def get_list_games(counter=1000, season='2015-16'):
        return GameList(Counter=counter, Season=season).list

    @staticmethod
    def neutral_descriptions(play_list):
        for item in play_list[0]:
            if not item['HOMEDESCRIPTION'] and not item['VISITORDESCRIPTION']:
                item['NEUTRALDESCRIPTION'] = None
            elif not item['HOMEDESCRIPTION'] and item['VISITORDESCRIPTION']:
                item['NEUTRALDESCRIPTION'] = item['VISITORDESCRIPTION']
            elif item['HOMEDESCRIPTION'] and not item['VISITORDESCRIPTION']:
                item['NEUTRALDESCRIPTION'] = item['HOMEDESCRIPTION']
            else:
                item['NEUTRALDESCRIPTION'] = item['HOMEDESCRIPTION']

        return play_list

    @staticmethod
    def convert_time_to_seconds(change_time):
        sp_time = str(change_time).split(':')
        return (int(sp_time[0])*60) + int(sp_time[1])

years = ['2011-12', '2010-11', '2009-10', '2008-09', '2007-08', '2006-07', '2005-06', '2004-05', '2003-04',
         '2002-03', '2001-02', '2000-01', '1999-00', '1998-99', '1997-98', '1996-97']


TechnicalEffects('2014-15', '2014')

