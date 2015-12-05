from StatGather import *


class Player:

    def __init__(self, name):
        self.name = name

    @property
    def basic_stats(self):
        return GeneralPlayerStats(player=self.name).list[0][0]

    @property
    def advanced_stats(self):
        return GeneralPlayerStats(self.name, MeasureType='Advanced').list[0][0]


class ComparePlayers:

    def __init__(self, player_one, player_two):
        self.player_one, self.player_two = Player(player_one), Player(player_two)

        stat_compare = self.compare_stats(self.player_one.basic_stats, self.player_two.basic_stats)
        tally_compare = self.tally_compare(stat_compare)

        print(self.return_formatted_player_comp(stat_compare, tally_compare))
    def compare_stats(self, stats_one, stats_two):
        stats_one = self.change_negative_stats(self.strip_non_stats(stats_one))
        stats_two = self.change_negative_stats(self.strip_non_stats(stats_two))
        compare_dict = {}
        try:
            for item in stats_one.keys():
                try:
                    compare_dict[item] = self.player_one.name if stats_one[item] > stats_two[item] else \
                        self.player_two.name
                except AttributeError:
                    continue
                except KeyError:
                    continue
                except TypeError:
                    continue
        except TypeError:
            return None

        return compare_dict

    def tally_compare(self, compare_dict):
        tally = {self.player_one.name: 0, self.player_two.name: 0}
        for item in compare_dict:
            tally[compare_dict[item]] += 1

        return tally

    def return_formatted_player_comp(self, stat_compare, tally_compare=None):
        if not tally_compare:
            tally_compare = self.tally_compare(stat_compare)
        sentence_form = '{} is better in {} of {} statistical categories, {} scores more, {} gets more assists, and {}' \
                        ' gets more rebounds.'
        return sentence_form.format(max(tally_compare), tally_compare[max(tally_compare)], sum(tally_compare.values()),
                                    stat_compare['PTS'], stat_compare['AST'], stat_compare['REB'])

    @staticmethod
    def strip_non_stats(stat_dict):
        non_stats = ['GROUP_SET', 'GROUP_VALUE', 'TD3', 'CFID', 'CFPARAMS']
        for item in non_stats:
            if item in stat_dict:
                stat_dict.pop(item)
        return stat_dict

    @staticmethod
    def change_negative_stats(stat_dict):
        negative_stats = ['TOV', 'PF']
        for item in negative_stats:
            if item in stat_dict:
                stat_dict[item] *= -1

        return stat_dict



ComparePlayers('Stephen Curry', 'LeBron James')