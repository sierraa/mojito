import click
from whaaaaat import prompt


class OutputHelper:

    def __init__(self):
        self.category_to_emoji = {
            "Lodging": "🧳",
            "Airfare": "✈️",
            "Other Travel": "🗺️",
            "Dining": "🍴",
            "Merchandise": "🛍️️",
            "Gas/Automotive": "⛽",
            "Phone/Cable": "☎️",
            "Health Care": "💊",
            "Entertainment": "🎤"
        }

    @staticmethod
    def echo_total(total):
        click.secho("💸 You spent ${:.2f} total 💸".format(total), bold=True, fg="green")

    @staticmethod
    def echo_time_averages(monthly, weekly, daily):
        click.secho("Your monthly average was ${:.2f}".format(monthly))
        click.secho("Your weekly average was ${:.2f}".format(weekly))
        click.secho("Your daily average was ${:.2f}\n\n".format(daily))

    @staticmethod
    def echo_analyzing_for_cardholder(cardholder):
        click.secho("💸 Analyzing for cardholder {} 💸".format(cardholder), bold=True, fg="green")

    @staticmethod
    def echo_average_of_transactions(average, count):
        click.secho("You spent ${:.2f} on average over a total of {} transactions".format(average, count))

    @staticmethod
    def echo_please_hold():
        click.secho("Please hold, this could take a few minutes...", fg="white", bg="black")

    @staticmethod
    def echo_no_transactions_in_category(category):
        click.secho("No transactions in category: {}".format(category), fg="white", bg="black")

    @staticmethod
    def confirm_overwrite(filename):
        overwrite_questions = [
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
        overwrite_answers = prompt(overwrite_questions)
        if overwrite_answers["overwrite"]:
            return filename
        return overwrite_answers["filename"]

    def echo_spending_with_percent(self, amount, category, raw_percentage, name="You"):
        click.secho(self.format_spending_with_percent(amount, category, raw_percentage, name=name))

    def format_spending_with_percent(self, amount, category, raw_percentage, name="You"):
        percent = raw_percentage * 100
        category_with_emoji = category + " " + self.category_to_emoji.get(category, "")
        return "{} spent ${:.2f} in {} ({:.2f}% of total)".format(name, amount, category_with_emoji, percent)

