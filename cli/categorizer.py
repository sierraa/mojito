from whaaaaat import prompt

from cli.output_helper import OutputHelper
from parser.capital_one_parser import CapitalOneParser


class Categorizer:

    def __init__(self, filename, start, finish):
        self.filename = filename
        self.parser = CapitalOneParser(filename, start_date=start, end_date=finish)
        self.categories = self.parser.get_all_categories()

    def categorize(self, category):
        todo = True
        while todo:
            self.__update_categories()
            retailer = self.__prompt_retailer(category)
            if not retailer:
                OutputHelper.echo_no_transactions_in_category(category)
                break
            self.categorize_retailer(retailer, write=False)
            todo = self.__prompt_continue()
        write_file = OutputHelper.confirm_overwrite(self.filename)
        self.parser.write(write_file)

    def categorize_retailer(self, retailer, write=False):
        new_category = self.__prompt_categorize()
        self.parser.update_categories_for_retailer(retailer, new_category)
        if write:
            write_file = OutputHelper.confirm_overwrite(self.filename)
            self.parser.write(write_file)

    def __prompt_categorize(self):
        questions = [
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
                'choices': self.categories,
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
        return new_category_answers["category"]

    def __prompt_retailer(self, category):
        uncategorized = self.parser.get_unique_transactions_for_category(category)
        if len(uncategorized) == 0:
            return None
        question = [{
                'type': 'list',
                'name': 'retailer',
                'message': 'Select a retailer to recategorize',
                'choices': uncategorized
                }]
        return prompt(question)["retailer"]

    def __prompt_continue(self):
        to_continue = [{
                    'type': 'confirm',
                    'name': 'continue',
                    'message': "Continue categorizing?",
                    'default': False
                }]
        return prompt(to_continue)["continue"]

    def __update_categories(self):
        self.categories = self.parser.get_all_categories()