from whaaaaat import prompt

from parser.capital_one_parser import CapitalOneParser


class Categorizer:

    @staticmethod
    def categorize(filename, start, finish, category):
        parser = CapitalOneParser(filename, start_date=start, end_date=finish)
        uncategorized = parser.get_unique_transactions_for_category(category)
        categories = parser.get_categories()
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
        output_questions = [
            {
                'type': 'confirm',
                'name': 'overwrite',
                'message': "Would you like to overwrite these changes to the existing csv ({})?".format(filename),
                'default': False
            },
            {
                'type': 'input',
                'name': 'filename',
                'message': 'Enter the filename to write output to:',
                'when': lambda answers: not answers['overwrite']
            }
        ]
        output_answers = prompt(output_questions)
        if output_answers['overwrite']:
            parser.write(filename)
        else:
            parser.write(output_answers['filename'])