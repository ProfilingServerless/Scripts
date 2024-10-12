#!/usr/bin/python

from datetime import datetime, timezone, timedelta
import argparse
import pandas as pd


EXPERIMENT_DURATION = 480
INVOCATIONS_CSV = os.path.joint(os.getenv('LOADER_DIR', '~/loader'), f'data/out/experiment_kn_stats_{EXPERIMENT_DURATION}.csv')

def epoch_micro2formated(microseconds):
    dt = datetime.fromtimestamp(microseconds / 1_000_000, tz=timezone.utc)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def export_durations():
    df = pd.read_csv(INVOCATIONS_CSV, skiprows=1) 
    col1 = df.iloc[:, 2]
    start = col1.min()
    end = col1.max()
    
    export_message = f"""
        Start: {epoch_micro2formated(start)}
        End: {epoch_micro2formated(end)}
    """



def show_help():
    help_message = """
    Toolset Command Line Interface

    Commands:
        export-durations   Export durations data.
        help               Show this help message.
    
    Usage:
        ./toolset.py <command>
    
    Example:
        ./toolset.py export-durations
        ./toolset.py help
    """
    print(help_message)

def main():
    parser = argparse.ArgumentParser(description='Toolset Command Line Interface')
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    export_parser = subparsers.add_parser('export-durations', help='Export durations data.')
    help_parser = subparsers.add_parser('help', help='Show help message.')

    args = parser.parse_args()

    if args.command == 'export-durations':
        export_durations()
    elif args.command == 'help':
        show_help()

if __name__ == '__main__':
    main()


print(formatted_date)
