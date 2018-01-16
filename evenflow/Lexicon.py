# -*- coding: utf-8 -*-


class Lexicon:

    @staticmethod
    def if_condition(line, args):
        if args[0]:
            return line['enter']
        return line['exit']

    def unless_condition(line, args):
        if args[0]:
            return line['exit']
        return line['enter']
