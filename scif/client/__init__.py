#!/usr/bin/env python

'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import scif
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="scientific filesystem tools")

    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    description = 'actions for Scientific Filesystem'
    subparsers = parser.add_subparsers(help='scif actions',
                                       title='actions',
                                       description=description,
                                       dest="command")

    # print version and exit
    version = subparsers.add_parser("version",
                                    help="show software version")
 

    # Preview changes to the filesystem
    shell = subparsers.add_parser("shell",
                                  help="shell to interact with scientific filesystem")

    shell.add_argument("recipe", nargs='?',
                       help="recipe file or scientific filesystem base", 
                       type=str)

    # Preview changes to the filesystem
    preview = subparsers.add_parser("preview",
                                     help="preview changes to a filesytem")

    # if the user provides more than one argument here, they are apps
    preview.add_argument("recipe", nargs="*", 
                         help="recipe file for the filesystem", 
                         type=str)

    # Install a recipe to the filesystem
    install = subparsers.add_parser("install",
                                     help="install a recipe on the filesystem")

    install.add_argument("recipe", nargs="*", 
                         help="recipe file for the filesystem", 
                         type=str)

    inspect = subparsers.add_parser("inspect",
                                     help="inspect an attribute for a scif installation")

    inspect.add_argument('attribute',
                         default='a',
                         const='a',
                         nargs='?',
                         choices=['r', 'e', 'a', 'd', 'l'],
                         help='''attribute to inspect (runscript, environment, definition,
                                 labels, or all''')

    run = subparsers.add_parser("run",
                                 help="entrypoint to run a scientific filesystem")


    run.add_argument("app", nargs='?',
                     help="app to target for the entry, defaults to shell if not set.", 
                     type=str)

    write = subparsers.add_parser("write",
                                   help="write a Dockerfile (default) or Singularity Recipe.")

    write.add_argument('--write',
                       default='docker',
                       const='docker',
                       nargs='?',
                       choices=['docker', 'singularity'],
                       help='write a container build specification from the scif recipe (default: %(default)s)')
        

    return parser


def get_subparsers(parser):
    '''get_subparser will get a dictionary of subparsers, to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers



def main():
    '''main is the entrypoint to managing or interacting with an scif 
       organized filesystem.
    '''

    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        '''print help, including the software version and active client 
           and exit with return code.
        '''
        version = scif.__version__

        print("\nScientific Filesystem [v%s]" %(version))
        parser.print_help()
        sys.exit(return_code)
    
    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # if environment logging variable not set, make silent
    if args.debug is False:
        os.environ['SCIF_MESSAGELEVEL'] = "INFO"

    # Show the version and exit
    if args.command == "version":
        print(scif.__version__)
        sys.exit(0)

    # Does the user want a shell?
    if args.command == "install": from .install import main
    if args.command == "preview": from .preview import main
    if args.command == "shell": from .shell import main
    if args.command == "inspect": from .inspect import main
    if args.command == "run": from .run import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args,
             parser=parser,
             subparser=subparsers[args.command])
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)

if __name__ == '__main__':
    main()