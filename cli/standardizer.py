from parser.trailhead_parser import TrailheadParser


class Standardizer:

    @staticmethod
    def standardize_trailhead(input, output, categorize_file=None):
        trailhead_parser = TrailheadParser(input)
        trailhead_parser.standardize(output, categorize_file=categorize_file)