from lib.DataGather import *


class TechnicalEffects:

    def __init__(self):
        self.list_games = self.get_list_games()

        test_game = Game(self.list_games[3])

        self.all_tech_runs = self.get_all_tech_runs(test_game)

        for tech in self.all_tech_runs:
            print(self.get_margin_change(tech, test_game))

    def get_all_tech_runs(self, game_obj):
        return [self.get_plays_after_tech(self.neutral_descriptions(game_obj.list),
                                          [tech['PCTIMESTRING'], tech['PERIOD']]) for tech in game_obj.tech_list]

    def get_plays_after_tech(self, game, tech_info, time_after=120):
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

        if orig_margin == 'TIE':
            orig_margin = 0
        if final_margin == 'TIE':
            final_margin = 0

        return (int(final_margin) * change_margin) - (int(orig_margin) * change_margin)

    @staticmethod
    def get_list_games(counter=1000):
        return GameList(Counter=counter).list

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

TechnicalEffects()
