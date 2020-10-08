from parser.trailhead_parser import TrailheadParser


class Standardizer:

    @staticmethod
    def standardize_trailhead(input, output):
        trailhead_parser = TrailheadParser(input)
        trailhead_parser.standardize(output)