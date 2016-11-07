import sys
import argparse

from goodtablesio.tasks import validate_table


def main():
    parser = argparse.ArgumentParser(prog='goodtablesio')
    parser.add_argument('url', help='URL or file path to a data file')
    args = parser.parse_args()

    if not args.url:
        print('Usage: goodtablesio <url or file path>')
        sys.exit(1)

    task = validate_table.delay(args.url)

    print('Task submitted to the queue: {0}'.format(task.task_id))
