import sys
import uuid

from .compilation import Compiler

def show_help():
    print (
        "Usage: rackfocus ./path/to/working/dir ./path/to/output/dir\n"
        "    (working directory is restored to original state)"
    )

def main():
    if len(sys.argv) != 3:
        show_help()
        sys.exit(1)

    working_dir = sys.argv[1] + '/rackfocus_{}'.format(uuid.uuid4().hex[:8])
    output_dir = sys.argv[2]

    compiler = Compiler(working_dir, output_dir)
    compiler.fetch_datasets()
    compiler.setup_database()
    compiler.write_database()
    compiler.close_database()
    compiler.cleanup_datasets()
