import logging
from parsing.sector import Sector

class SectorEF(Sector):

    @staticmethod
    def reformat_2x4(sector_list):
        s = sector_list
        new_list = [[s[0][0], s[0][0], s[0][1], s[0][1]],
                    [s[2][0], s[2][0], s[2][1], s[2][1]],
                    [s[1][0], s[1][0], s[1][1], s[1][1]],
                    [s[3][0], s[3][0], s[3][1], s[3][1]]]
        return new_list

    @staticmethod
    def reformat_6x4(sector_list):
        s = sector_list
        new_list = [[s[0][0], s[0][0], s[0][3], s[0][3]],
                    [s[2][0], s[2][0], s[2][3], s[2][3]],
                    [s[1][0], s[1][0], s[1][3], s[1][3]],
                    [s[3][0], s[3][0], s[3][3], s[3][3]]]
        return new_list

    @staticmethod
    def reformat_2x2(sector_list):
        s = sector_list
        new_list = [[s[0][0], s[0][0], s[0][1], s[0][1]],
                    [s[2][0], s[2][0], s[2][1], s[2][1]],
                    [s[1][0], s[1][0], s[1][3], s[1][3]],
                    [s[2][0], s[2][0], s[2][1], s[2][1]]]
        return new_list

    @staticmethod
    def reformat_1x4(sector_list):
        s = sector_list
        new_list = [[s[0][0], s[0][0], s[0][0], s[0][0]],
                    [s[2][0], s[2][0], s[2][0], s[2][0]],
                    [s[1][0], s[1][0], s[1][0], s[1][0]],
                    [s[3][0], s[3][0], s[3][0], s[3][0]]]
        return new_list
