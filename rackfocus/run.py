import uuid
import argparse

from .compilation import Compiler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('working', nargs='?', help='Temporary directory. Is restored to original state once done.')
    parser.add_argument('output', nargs='?', help='Output directory of sqlite file.')
    args = parser.parse_args()
    
    compiler = Compiler(args.working, args.output)
    compiler.fetch_datasets()
    compiler.setup_database()
    compiler.write_database()
    compiler.close_database()
    compiler.cleanup_datasets()
