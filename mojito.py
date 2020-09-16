#!/usr/bin/env python3
from main.capital_one_analyzer import CapitalOneAnalyzer
# from dotenv import load_dotenv
import click


# TODO: colorize me :-) and add emojis
# - Add data by month
# - Compare year to year
@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename')
def overview(filename):
    analyze_capital_one(filename)


@cli.command()
@click.argument('filename')
def cardholders(filename):
    analyze_capital_one_per_cardholder(filename)

@cli.command()
@click.argument('filename')
@click.argument('retailer')
@click.option('-a', '--average', is_flag=True) # TODO: consider making this a verbose flag
def retailer(filename, retailer, average):
    analyze_capital_one_for_retailer(filename, retailer, average)

@cli.command()
@click.argument('filename')
@click.option('-c', '--category')
@click.option('-n', '--number_of_retailers', default=100)
def retailers(filename, category, number_of_retailers):
    # TODO: add average parameters here
    analyze_capital_one_per_retailer(filename, category, number_of_retailers)


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


def analyze_capital_one_per_retailer(fname, category, number_of_retailers):
    # TODO: limit by dollar amount?
    print("Please hold, this could take a few minutes...")
    capital_one = CapitalOneAnalyzer(fname, category=category)
    total_spent = capital_one.get_total_spending()
    total_per_retailer = capital_one.get_total_spending_per_retailer()
    retailers = list(total_per_retailer.keys())
    for i in range(number_of_retailers):
        retailer = retailers[i]
        percent = total_per_retailer[retailer] / total_spent
        print(format_spending_with_percent(total_per_retailer[retailer], retailer, percent))


def format_spending_with_percent(amount, category, raw_percentage, name="You"):
    percent = raw_percentage * 100
    return "{} spent {:.2f} in {} ({:.2f}% of total)".format(name, amount, category, percent)


if __name__ == "__main__":
    # load_dotenv()
    cli()
