import argparse
import signal
import sys
import uuid

from .compilation import Compiler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('working', nargs='?', help='Temporary directory. Is restored to original state once done.')
    parser.add_argument('output', nargs='?', help='Output directory to write the SQLite database file in.')
    args = parser.parse_args()

    working_dir = args.working + '/rackfocus_{}'.format(uuid.uuid4().hex[:8])
    compiler = Compiler(working_dir, args.output)

    # Handling unexpected interruptions
    def _handle_interrupt(signum, _):
        signal.signal(signum, signal.SIG_IGN)
        compiler.cleanup_datasets(delete_db=True)
        sys.exit(signal.SIGINT)
    signal.signal(signal.SIGINT, _handle_interrupt)

    compiler.fetch_datasets()
    compiler.setup_database()
    compiler.write_database()
    compiler.close_database()
    compiler.cleanup_datasets()
