from lib.DataGather import *


class TechnicalEffects:

    def __init__(self):
        self.list_games = self.get_list_games()

        Test_game = Game(self.list_games[2])

        self.all_tech_runs = self.get_all_tech_runs(Test_game)

        print(self.get_margin_first_last(self.all_tech_runs[0]))

    def get_all_tech_runs(self, game_obj):
        return [self.get_plays_after_tech(self.neutral_descriptions(game_obj.list), tech['EVENTNUM']) for tech in game_obj.tech_list]

    def get_plays_after_tech(self, game, tech_index, plays_after=30):
        plays_list = []
        for item in game[0]:
            if tech_index <= item['EVENTNUM'] <= tech_index+plays_after:
                plays_list.append(item)

        return plays_list

    def get_margin_first_last(self, tech_run):
        return ([(item['PLAYER1_TEAM_ABBREVIATION'], item['SCORE'],
                  item['SCOREMARGIN']) for item in tech_run if item['SCORE']])
        # print(tech_run[0]['SCORE'], tech_run[len(tech_run)-1]['SCORE'])

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

TechnicalEffects()