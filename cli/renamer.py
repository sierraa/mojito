from whaaaaat import prompt

from cli.output_helper import OutputHelper
from parser.capital_one_parser import CapitalOneParser
from parser.merchant_parser import MerchantParser


class Renamer:

    @staticmethod
    def rename(filename, start, finish, term):
        parser = CapitalOneParser(filename, start_date=start, end_date=finish)
        todo = True
        while todo:
            merchant_parser = MerchantParser(parser.get_dataframe())
            matches = merchant_parser.get_similar_retailers(term)
            if len(matches) == 0:
                OutputHelper.echo_no_matches_found(term)
                break
            questions = [
                {
                    'type': 'list',
                    'name': 'retailer',
                    'message': 'Select a retailer to rename',
                    'choices': matches
                },
                {
                    'type': 'confirm',
                    'name': 'existing',
                    'message': 'Would you like to change this to an existing name?',
                    'default': True
                },
                {
                    'type': 'list',
                    'name': 'name',
                    'message': 'Select an existing name.',
                    'choices': matches,
                    'when': lambda answers: answers['existing']
                },
                {
                    'type': 'input',
                    'name': 'name',
                    'message': 'Enter a new name:',
                    'when': lambda answers: not answers['existing']
                },
                {
                    'type': 'confirm',
                    'name': 'continue',
                    'message': "Continue renaming?",
                    'default': False
                }
            ]
            # Need to write on every loop here cos matches don't get updated?
            new_name_answers = prompt(questions)
            parser.update_description_for_retailer(new_name_answers['retailer'], new_name_answers['name'])

            matches = merchant_parser.get_similar_retailers(term)
            todo = new_name_answers['continue'] and len(matches) > 0
        write_file = OutputHelper.confirm_overwrite(filename)
        parser.write(write_file)