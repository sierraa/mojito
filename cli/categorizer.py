from whaaaaat import prompt

from cli.output_helper import OutputHelper
from parser.capital_one_parser import CapitalOneParser


class Categorizer:

    @staticmethod
    def categorize(filename, start, finish, category):
        parser = CapitalOneParser(filename, start_date=start, end_date=finish)
        uncategorized = parser.get_unique_transactions_for_category(category)
        # TODO: add q to quit
        # Add a while loop
        if len(uncategorized) == 0:
            OutputHelper.echo_no_transactions_in_category(category)
            return
        categories = parser.get_all_categories()
        questions = [
            {
                'type': 'list',
                'name': 'retailer',
                'message': 'Select a retailer to recategorize',
                'choices': uncategorized
            },
            {
                'type': 'confirm',
                'name': 'existing',
                'message': 'Would you like to add this to an existing category?',
                'default': True
            },
            {
                'type': 'list',
                'name': 'category',
                'message': 'Select an existing category.',
                'choices': categories,
                'when': lambda answers: answers['existing']
            },
            {
                'type': 'input',
                'name': 'category',
                'message': 'Enter a new category:',
                'when': lambda answers: not answers['existing']
            }
        ]
        new_category_answers = prompt(questions)
        parser.update_categories_for_retailer(new_category_answers['retailer'], new_category_answers['category'])
        write_file = OutputHelper.confirm_overwrite(filename)
        parser.write(write_file)
