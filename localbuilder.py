#!/usr/bin/env python
import os
import time
import commands
from optparse import OptionParser


def mtime_checker(arg, directory_name, file_list):
    """
    Check whether a list of files have been modified 
    in the previous time period and append those 
    that have to a list.
    """
    (mtime, modified_list) = arg
    for f in [os.path.join(directory_name, file) for file in file_list]:
        if not skip_filepath(f):
            if os.path.isdir(f) and __skip_extensions__:
                # if extensions are watched, don't bother with directories
                continue
            if os.path.getmtime(f) > mtime:
                modified_list.append(f)


def skip_filepath(filepath):
    """ return true if the passed filename can be skipped in the change
    checker. """
    if os.path.basename(filepath).startswith('.#') or \
      filepath.endswith('~'):
        # backup file
        return True
    
    if os.path.splitext(filepath)[-1].lower() in __skip_extensions__:
        return True
    
def get_changed_files(path, delta):
    """
    Get the list of files that have changed in 
    a given time delta.
    """
    modified_files = []
    timestamp = time.time() - delta
    os.path.walk(path, mtime_checker, (timestamp, modified_files))
    return modified_files

def run_if_changes(modified_files, command_to_run):
    """
    If we have file modifications then run the 
    specified command.
    """
    if len(modified_files):
        return commands.getoutput(command_to_run)
    else:
        return False

#global __skip_extensions__
__skip_extensions__ = []

def main(path, change_period, command, skip_extensions):
    """
    Long running application which polls for changes
    and when it finds them runs a specified command.
    """
    __skip_extensions__.extend([x.startswith('.') and x or '.'+x 
                                for x
                                in skip_extensions.replace(',',' ').split()])
    # keep the script running
    while 1:
        # get a list of files that have changed
        modified_files = get_changed_files(path, change_period)
        # if we have changes then run the specified command
        output = run_if_changes(modified_files, command)
        if output:
            # if we have some output then print it
            print output
        else:
            # if we don't then at least show we're still runnning
            print "Nothing changed since last build"
        # wait for the next build
        time.sleep(change_period)

if __name__ == "__main__":
    # instantiate the arguments parser
    parser = OptionParser()
    # set up options
    parser.add_option('--path', action='store', dest='path', default='.',
                        help='path to start looking for files'),
    parser.add_option('--period', action='store', dest='change_period', default=60, type='float',
                        help='time period to wait between checks'),
    parser.add_option('-c', '--command', action='store', dest='command',
                        help='command to execute'),
    parser.add_option('--skip-extensions', action='store', dest='skip_extensions',
                      help='extensions to skip (list by space or comma)', 
                      default="pyc html css"),
    # parse the command arguments
    (options, args) = parser.parse_args()
    
    if options.command:
        main(options.path, int(options.change_period), options.command,
             options.skip_extensions)
    else:
        print "you must pass a command to execute using the -c flag."