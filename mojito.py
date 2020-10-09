#!/usr/bin/env python3
from cli.analyzer import Analyzer
from cli.categorizer import Categorizer
# from dotenv import load_dotenv
import logging
import click

from cli.cleaner import Cleaner
from cli.standardizer import Standardizer
from util.transaction_date_util import TransactionDateUtil

# TODO: Compare year to year
# - Allow users to set goals and track those goals
# - Make predictions based on previous years
# TODO: Add output options (even just csv for now would be nice)
# TODO: probably makes sense to add an analyze command plus sub commands
# https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl

@click.group()
@click.argument('filename') # TODO: how to have the command appear before the file name
@click.pass_context
@click.option('-s', '--start', help="Start date of the format YYYY-MM-DD")
@click.option('-f', '--finish', help="Finish date of the format YYYY-MM-DD")
@click.option('-v', '--verbose', is_flag=True, help="Shows averages over time.")
@click.option('--debug', is_flag=True)
def cli(ctx, filename, start, finish, verbose, debug):
    ctx.ensure_object(dict)
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    if start or finish:
        TransactionDateUtil.validate_dates(start, finish)
    ctx.obj['START'] = start
    ctx.obj['FINISH'] = finish
    ctx.obj['FILENAME'] = filename
    ctx.obj['VERBOSE'] = verbose


@cli.command()
@click.pass_context
def overview(ctx):
    """Get an overview of spending per category"""
    analyzer = Analyzer(ctx.obj['FILENAME'], start_date=ctx.obj['START'], end_date=ctx.obj['FINISH'])
    analyzer.analyze(ctx.obj['VERBOSE'])


@cli.command()
@click.pass_context
@click.argument('output')
# TODO: debug option in here
def clean(ctx, output):
    """Clean up descriptions in the csv and write it to a file"""
    Cleaner.clean_capital_one(ctx.obj['FILENAME'], output)


@cli.command()
@click.pass_context
def cardholders(ctx):
    """Breakdown spending per category by cardholders"""
    analyzer = Analyzer(ctx.obj['FILENAME'], start_date=ctx.obj['START'], end_date=ctx.obj['FINISH'])
    analyzer.analyze_per_cardholder(ctx.obj['VERBOSE'])


@cli.command()
@click.pass_context
@click.argument('retailer')
def retailer(ctx, retailer):
    """Breakdown spending for a specific retailer"""
    analyzer = Analyzer(ctx.obj['FILENAME'], start_date=ctx.obj['START'], end_date=ctx.obj['FINISH'])
    analyzer.analyze_for_retailer(retailer, ctx.obj['VERBOSE'])


@cli.command()
@click.pass_context
@click.option('-c', '--category', help="Purchase category to filter on")
@click.option('-n', '--number_of_retailers', default=100)
@click.option('--order_by', type=click.Choice(['number_of_transactions', 'dollar_amount']), default='dollar_amount')
def retailers(ctx, category, number_of_retailers, order_by):
    """Show overall spending for all retailers"""
    analyzer = Analyzer(ctx.obj['FILENAME'], start_date=ctx.obj['START'], end_date=ctx.obj['FINISH'])
    analyzer.analyze_per_retailer(ctx.obj['VERBOSE'], number_of_retailers, order_by, category=None)


@cli.command()
@click.pass_context
@click.argument('output')
@click.option('--bank', type=click.Choice(['trailhead']), default='trailhead') # TODO: add more banks
@click.option('--categorize_file', help="Use string matching to categorize vendors")
def standardize(ctx, output, bank, categorize_file):
    """Standardize csv output from different banks"""
    if bank == "trailhead":
        Standardizer.standardize_trailhead(ctx.obj['FILENAME'], output, categorize_file=categorize_file)


@cli.command()
@click.pass_context
@click.argument('csv', nargs=-1) # Unlimited number of arguments
@click.argument('output')
def merge(ctx, csv, output):
    """Merge multiple CSVs into a single source of truth. Must already be in the Capital One format."""
    Cleaner.merge_data(ctx.obj['FILENAME'], csv, output)


@cli.command()
@click.pass_context
@click.argument('category')
def categorize(ctx, category):
    """Categorize entries in an existing category.
    For best results use on data that has already been cleaned using the clean command."""
    Categorizer.categorize(ctx.obj['FILENAME'], ctx.obj['START'], ctx.obj['FINISH'], category)


if __name__ == "__main__":
    # load_dotenv()
    cli(obj={})
