#!/usr/bin/env python3

from main.capital_one_analyzer import CapitalOneAnalyzer
# from dotenv import load_dotenv
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.option('--cardholders/--no-cardholders', default=False)
def capitalone(filename, cardholders):
    if cardholders:
        analyze_capital_one_per_cardholder(filename)
    else:
        analyze_capital_one(filename)


# TODO: add methods for analyzing per year/month/week
# TODO add a class for categorizing stuff (filterer? categorizer?)
def analyze_capital_one(fname):
    capital_one = CapitalOneAnalyzer(fname)
    spending_per_category = capital_one.get_spending_per_category()
    percentage_per_category = capital_one.get_percentage_per_category()
    print("You spent {:.2f} total".format(capital_one.get_total_spending()))
    for category in spending_per_category.keys():
        click.echo(format_spending_with_percent(spending_per_category[category], category, percentage_per_category[category]))


def analyze_capital_one_per_cardholder(fname):
    capital_one = CapitalOneAnalyzer(fname)
    spending_per_category_per_cardholder = capital_one.get_spending_per_category_per_cardholder()
    percent_per_category_per_cardholder = capital_one.get_percent_per_category_per_cardholder()
    for cardholder in spending_per_category_per_cardholder.keys():
        print("Analyzing for cardholder {}".format(cardholder))
        for category in spending_per_category_per_cardholder[cardholder].keys():
            click.echo(format_spending_with_percent(spending_per_category_per_cardholder[cardholder][category], category,
                                               percent_per_category_per_cardholder[cardholder][category], name=cardholder))


def format_spending_with_percent(amount, category, raw_percentage, name="You"):
    percent = raw_percentage * 100
    return "{} spent {:.2f} in {} ({:.2f}% of total)".format(name, amount, category, percent)


if __name__ == "__main__":
    # load_dotenv()
    cli()
