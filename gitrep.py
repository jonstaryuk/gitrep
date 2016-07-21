#!/usr/bin/env python

import os
import sys
from blessings import Terminal
from git import Repo


t = Terminal()


def parse(directory):
    """Find paths to all the git repos in the given directory."""
    repos = []
    os.path.walk(directory, visit, repos)
    return repos


def visit(repos, dirname, names):
    """Process a directory encountered while walking the hierarchy. Skip module
    directories on the fly. If a git repo is detected, add its path to `repos`
    and skip the .git directory."""

    # Skip module directories
    SKIP_DIRS = ['node_modules', 'bower_components']
    for skip_dir in SKIP_DIRS:
        try:
            names.remove(skip_dir)
        except:
            pass

    # Detect git repo
    if '.git' in names:
        repos.append(dirname)
        names.remove('.git')


def repos(paths):
    """Generate a list of Repo objects from the given paths."""
    return [Repo(path) for path in paths]


def print_repo_info(repo):
    """Formats and prints the number of remotes and the repo's path."""
    # Get absolute path to the parent directory of .git
    abspath = os.path.split(repo.git_dir)[0]
    # Get and the relative path and split it
    path = os.path.split(os.path.relpath(abspath))
    # Make the basename bold
    title = path[0] + '/' + t.bold(path[1])

    # See if it has any remotes
    n = len(repo.remotes)
    if n > 1:
        symbol = t.bold_blue(' ' + str(n) + ' ')
    elif n == 1:
        symbol = ' 1 '
    else:
        symbol = t.yellow(' 0 ')

    print symbol, title


if __name__ == '__main__':
    # Check presence of arguments
    if len(sys.argv) < 2:
        # Use current directory path
        path = os.curdir
    else:
        # Get directory path from arguments
        path = sys.argv[1]

    # Check that the path is indeed a directory
    if not os.path.isdir(path):
        print 'error:', path, 'is not a directory.'

    for repo in repos(parse(path)):
        print_repo_info(repo)
