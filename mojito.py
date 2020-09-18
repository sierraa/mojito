#!/usr/bin/env python3
from main.capital_one_analyzer import CapitalOneAnalyzer
# from dotenv import load_dotenv
import click
import datetime


# TODO: Compare year to year
# - Allow users to change categories (review things in the "other categories")
# - Allow users to set goals and track those goals
# - Make predictions based on previous years
from main.capital_one_cleaner import CapitalOneCleaner


@click.group()
@click.argument('filename') # TODO: how to have the command appear before the file name
@click.pass_context
@click.option('-s', '--start', help="Start date of the format YYYY-MM-DD")
@click.option('-f', '--finish', help="Finish date of the format YYYY-MM-DD")
@click.option('-v', '--verbose', is_flag=True)
def cli(ctx, filename, start, finish, verbose):
    ctx.ensure_object(dict)
    start_date, finish_date = validate_dates(start, finish)
    ctx.obj['FILENAME'] = filename
    ctx.obj['START'] = start_date
    ctx.obj['FINISH'] = finish_date
    ctx.obj['VERBOSE'] = verbose


@cli.command()
@click.pass_context
def overview(ctx):
    """Get an overview of spending per category"""
    analyze_capital_one(ctx.obj['FILENAME'], ctx.obj['START'], ctx.obj['FINISH'], ctx.obj['VERBOSE'])


@cli.command()
@click.pass_context
@click.argument('output')
# TODO: debug option in here
def clean(ctx, output):
    #TODO clean up merchant categories as well
    """Clean up descriptions in the csv and write it to a file"""
    clean_capital_one(ctx.obj['FILENAME'], output)


@cli.command()
@click.pass_context
def cardholders(ctx):
    """Breakdown spending per category by cardholders"""
    analyze_capital_one_per_cardholder(ctx.obj['FILENAME'], ctx.obj['START'], ctx.obj['FINISH'], ctx.obj['VERBOSE'])


@cli.command()
@click.pass_context
@click.argument('retailer')
def retailer(ctx, retailer):
    """Breakdown spending for a specific retailer"""
    analyze_capital_one_for_retailer(ctx.obj['FILENAME'], retailer, ctx.obj['START'],
                                     ctx.obj['FINISH'], ctx.obj['VERBOSE'])


@cli.command()
@click.pass_context
@click.option('-c', '--category', help="Purchase category to filter on")
@click.option('-n', '--number_of_retailers', default=100)
def retailers(ctx, category, number_of_retailers):
    """Show overall spending for all retailers"""
    analyze_capital_one_per_retailer(ctx.obj['FILENAME'], ctx.obj['START'], ctx.obj['FINISH'],
                                     category, ctx.obj['VERBOSE'], number_of_retailers)


# TODO: add methods for analyzing per year/month/week
# TODO add a class for categorizing stuff (filterer? categorizer?)
# TODO: Add output options (even just csv for now would be nice)
def analyze_capital_one(fname, start_date, end_date, verbose):
    capital_one = CapitalOneAnalyzer(fname, start_date=start_date, end_date=end_date)
    spending_per_category = capital_one.get_spending_per_category()
    percentage_per_category = capital_one.get_percentage_per_category()
    click.secho("💸 You spent ${:.2f} total 💸".format(capital_one.get_total_spending()), bold=True, fg="green")
    for category in spending_per_category.keys():
        click.secho(format_spending_with_percent(spending_per_category[category], category, percentage_per_category[category]))


def analyze_capital_one_per_cardholder(fname, start, finish, verbose):
    capital_one = CapitalOneAnalyzer(fname, start_date=start, end_date=finish)
    spending_per_category_per_cardholder = capital_one.get_spending_per_category_per_cardholder()
    percent_per_category_per_cardholder = capital_one.get_percent_per_category_per_cardholder()
    for cardholder in spending_per_category_per_cardholder.keys():
        click.secho("💸 Analyzing for cardholder {} 💸".format(cardholder), bold=True, fg="green")
        for category in spending_per_category_per_cardholder[cardholder].keys():
            click.secho(format_spending_with_percent(spending_per_category_per_cardholder[cardholder][category], category,
                                               percent_per_category_per_cardholder[cardholder][category], name=cardholder))


def analyze_capital_one_for_retailer(fname, retailer, start, finish, verbose):
    capital_one = CapitalOneAnalyzer(fname, start_date=start, end_date=finish)
    total_spent = capital_one.get_total_spending()
    click.secho("💸 You spent ${:.2f} total 💸".format(total_spent), bold=True, fg="green")
    retailer_total = capital_one.get_total_spending_for_retailer(retailer)
    percent = retailer_total / total_spent
    print(format_spending_with_percent(retailer_total, retailer, percent))
    if verbose:
        average, count = capital_one.get_average_and_count_for_retailer(retailer)
        click.secho("You spent ${:.2f} on average over a total of {} transactions".format(average, count))


def analyze_capital_one_per_retailer(fname, start, finish, category, verbose, number_of_retailers):
    # TODO: limit by dollar amount?
    click.secho("Please hold, this could take a few minutes...", fg="white", bg="black")
    capital_one = CapitalOneAnalyzer(fname, category=category, start_date=start, end_date=finish)
    total_spent = capital_one.get_total_spending()
    total_per_retailer = capital_one.get_total_spending_per_retailer()
    retailers = list(total_per_retailer.keys())
    for i in range(min(len(retailers), number_of_retailers)):
        retailer = retailers[i]
        percent = total_per_retailer[retailer] / total_spent
        print(format_spending_with_percent(total_per_retailer[retailer], retailer, percent))


def clean_capital_one(input, output):
    capital_one_cleaner = CapitalOneCleaner(input)
    capital_one_cleaner.clean(output)


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
    cli(obj={})
