#!/usr/bin/env python3

from main.capital_one_analyzer import CapitalOneAnalyzer
# from dotenv import load_dotenv
import click


@click.group()
def cli(): # TODO: need to add options
    pass


@cli.command()
@click.argument('filename')
@click.option('--cardholders', is_flag=True)
@click.option('-r', '--retailer')
@click.option('--all_retailers', is_flag=True)
@click.option('-a', '--average', is_flag=True)
def capitalone(filename, cardholders, retailer, all_retailers, average):
    if all_retailers:
        analyze_capital_one_per_retailer(filename) # TODO: add average here
    elif retailer:
        analyze_capital_one_for_retailer(filename, retailer, average)
    elif cardholders:
        analyze_capital_one_per_cardholder(filename)
    else:
        analyze_capital_one(filename)


# TODO: add methods for analyzing per year/month/week
# TODO add a class for categorizing stuff (filterer? categorizer?)
# TODO: Add output options (even just csv for now would be nice)
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


def analyze_capital_one_for_retailer(fname, retailer, average):
    capital_one = CapitalOneAnalyzer(fname)
    total_spent = capital_one.get_total_spending()
    print("You spent {:.2f} total".format(total_spent))
    retailer_total = capital_one.get_total_spending_for_retailer(retailer)
    percent = retailer_total / total_spent
    print(format_spending_with_percent(retailer_total, retailer, percent))
    if average:
        average, count = capital_one.get_average_and_count_for_retailer(retailer)
        print("You spent {:.2f} on average over a total of {} transactions".format(average, count))


def analyze_capital_one_per_retailer(fname):
    # TODO: should have a category argument here
    capital_one = CapitalOneAnalyzer(fname)
    total_spent = capital_one.get_total_spending()
    total_per_retailer = capital_one.get_total_spending_per_retailer()
    for retailer in total_per_retailer.keys():
        percent = retailer / total_spent
        print(format_spending_with_percent(total_per_retailer[retailer], retailer, percent))


def format_spending_with_percent(amount, category, raw_percentage, name="You"):
    percent = raw_percentage * 100
    return "{} spent {:.2f} in {} ({:.2f}% of total)".format(name, amount, category, percent)


if __name__ == "__main__":
    # load_dotenv()
    cli()
