from StatGather import *
from random import choice


class Game:

    def __init__(self, team_one=None, team_two=None, **kwargs):
        self.game_params = self.edit_params({'quarters': 4, 'shot_clock': 24, 'quarter_clock': '12'}, kwargs)
        if not team_one or not team_two:
            self.team_one, self.team_two = self.handle_team_names(team_one, team_two)
        else:
            self.team_one, self.team_two = team_one, team_two

        self.team_one_obj, self.team_two_obj = Team(self.team_one), Team(self.team_two)


    def handle_team_names(self, team_one, team_two):
        team_one = self.gen_team() if not team_one else team_one
        team_two = self.gen_team() if not team_two else team_two

        return team_one, team_two

    @staticmethod
    def edit_params(base_params, kwargs):
        for item in kwargs.keys():
            if item in base_params:
                base_params[item] = kwargs[item]

        return base_params

    @staticmethod
    def gen_team():
        with open('teamlist.txt', 'r') as team_file:
            return choice([team.split(': ')[0] for team in team_file])


class Team:

    def __init__(self, name):
        self.name = name
        self.roster = self.get_roster()

    def get_roster(self):
        roster_obj = TeamRoster(self.name)
        return [player['PLAYER'] for player in roster_obj.list[0]]

Game()
