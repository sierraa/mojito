## Mojito

Mojito aspires to be a mint-like budgeting tool minus Intuit. Currently it is a CLI tool I built to help with budgeting. 

```bash
% python3 mojito.py                                     
Usage: mojito.py [OPTIONS] FILENAME COMMAND [ARGS]...

Options:
  -s, --start TEXT   Start date of the format YYYY-MM-DD
  -f, --finish TEXT  Finish date of the format YYYY-MM-DD
  -v, --verbose      Shows averages over time.
  --debug
  --help             Show this message and exit.

Commands:
  cardholders  Breakdown spending per category by cardholders
  categorize   Categorize entries in an existing category.
  clean        Clean up descriptions in the csv and write it to a file
  merge        Merge multiple CSVs into a single source of truth.
  overview     Get an overview of spending per category
  retailer     Breakdown spending for a specific retailer
  retailers    Show overall spending for all retailers
  standardize  Standardize csv output from different banks
```

## Example Workflow

Go to your banks and download CSV files of your transactions for the month or year. It should look something like this:

```csv
Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit
2000-09-29,2000-09-30,1234,chevron,Gas/Automotive,33.11,
...
```

As of October 2020, mojito uses Capital One's transaction file format shown above. 

### Cleaning your data

You can get another bank in this format using the *standardize* command. Only Trailhead Credit Union is currently supported. 

Use the *clean* command to clean up transaction details. This removes transaction/merchant/store IDs makes it easier to group similar transactions into retailers.

Use the *categorize* command for additional cleanup if you'd like. This is useful for moving mis-categorized transactions into the correct categories.

You can then *merge* your CSVs into one master file. 

### Analyzing your data

After all your transaction data is in a buttoned-up format, you are now ready to analyze it. 

```bash
python3 mojito.py 92020.csv overview
```

You can then further inspect your spending for the month by using the *retailers* command. 
