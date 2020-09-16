#!/usr/bin/env python3
from main.capital_one_analyzer import CapitalOneAnalyzer
# from dotenv import load_dotenv
import click
import datetime


# TODO: Add data by month
# - Compare year to year
@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename')
@click.option('-s', '--start')
@click.option('-f', '--finish')
def overview(filename, start, finish):
    start_date, finish_date = validate_dates(start, finish)
    analyze_capital_one(filename, start_date, finish_date)


@cli.command()
@click.argument('filename')
def cardholders(filename):
    analyze_capital_one_per_cardholder(filename)

@cli.command()
@click.argument('filename')
@click.argument('retailer')
@click.option('-v', '--verbose', is_flag=True)
def retailer(filename, retailer, verbose):
    analyze_capital_one_for_retailer(filename, retailer, verbose)

@cli.command()
@click.argument('filename')
@click.option('-c', '--category')
@click.option('-n', '--number_of_retailers', default=100)
def retailers(filename, category, number_of_retailers):
    # TODO: add verbose parameters here
    analyze_capital_one_per_retailer(filename, category, number_of_retailers)


# TODO: add methods for analyzing per year/month/week
# TODO add a class for categorizing stuff (filterer? categorizer?)
# TODO: Add output options (even just csv for now would be nice)
def analyze_capital_one(fname, start_date, end_date):
    capital_one = CapitalOneAnalyzer(fname, start_date=start_date, end_date=end_date)
    spending_per_category = capital_one.get_spending_per_category()
    percentage_per_category = capital_one.get_percentage_per_category()
    click.secho("💸 You spent ${:.2f} total 💸".format(capital_one.get_total_spending()), bold=True, fg="green")
    for category in spending_per_category.keys():
        click.secho(format_spending_with_percent(spending_per_category[category], category, percentage_per_category[category]))


def analyze_capital_one_per_cardholder(fname):
    capital_one = CapitalOneAnalyzer(fname)
    spending_per_category_per_cardholder = capital_one.get_spending_per_category_per_cardholder()
    percent_per_category_per_cardholder = capital_one.get_percent_per_category_per_cardholder()
    for cardholder in spending_per_category_per_cardholder.keys():
        click.secho("💸 Analyzing for cardholder {} 💸".format(cardholder), bold=True, fg="green")
        for category in spending_per_category_per_cardholder[cardholder].keys():
            click.secho(format_spending_with_percent(spending_per_category_per_cardholder[cardholder][category], category,
                                               percent_per_category_per_cardholder[cardholder][category], name=cardholder))


def analyze_capital_one_for_retailer(fname, retailer, verbose):
    capital_one = CapitalOneAnalyzer(fname)
    total_spent = capital_one.get_total_spending()
    click.secho("💸 You spent ${:.2f} total 💸".format(total_spent), bold=True, fg="green")
    retailer_total = capital_one.get_total_spending_for_retailer(retailer)
    percent = retailer_total / total_spent
    print(format_spending_with_percent(retailer_total, retailer, percent))
    if verbose:
        average, count = capital_one.get_average_and_count_for_retailer(retailer)
        click.secho("You spent ${:.2f} on average over a total of {} transactions".format(average, count))


def analyze_capital_one_per_retailer(fname, category, number_of_retailers):
    # TODO: limit by dollar amount?
    click.secho("Please hold, this could take a few minutes...", fg="white", bg="black")
    capital_one = CapitalOneAnalyzer(fname, category=category)
    total_spent = capital_one.get_total_spending()
    total_per_retailer = capital_one.get_total_spending_per_retailer()
    retailers = list(total_per_retailer.keys())
    for i in range(number_of_retailers):
        retailer = retailers[i]
        percent = total_per_retailer[retailer] / total_spent
        print(format_spending_with_percent(total_per_retailer[retailer], retailer, percent))


# TODO: probably move this utilities into their own classes
def format_spending_with_percent(amount, category, raw_percentage, name="You"):
    category_to_emoji = {
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
    percent = raw_percentage * 100
    category_with_emoji = category + " " + category_to_emoji.get(category, "")
    return "{} spent ${:.2f} in {} ({:.2f}% of total)".format(name, amount, category_with_emoji, percent)


def validate_dates(start, finish):
    start_date = validate_date(start)
    finish_date = validate_date(finish)
    return start_date, finish_date


def validate_date(dt):
    if dt is None:
        return None
    date_format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(dt, date_format)
        return dt
    except ValueError:
        click.secho("Invalid date provided: {}. Ignoring.".format(dt), fg="red", bold=True)
        return None


if __name__ == "__main__":
    # load_dotenv()
    cli()
