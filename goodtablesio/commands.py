import sys
import argparse

from goodtablesio import create_task, get_task


def main():
    parser = argparse.ArgumentParser(prog='goodtablesio')
    parser.add_argument('url', help='URL or file path to a data file')
    args = parser.parse_args()

    if not args.url:
        print('Usage: goodtablesio <url or file path>')
        sys.exit(1)

    task_id = create_task(args.url)

    print('Task submitted to the queue: {0}'.format(task_id))


def status():
    parser = argparse.ArgumentParser(prog='goodtablesio')
    parser.add_argument('id', help='Validation task id')
    args = parser.parse_args()

    if not args.id:
        print('Usage: goodtablesio-status <id>')
        sys.exit(1)

    print(get_task(args.id))
