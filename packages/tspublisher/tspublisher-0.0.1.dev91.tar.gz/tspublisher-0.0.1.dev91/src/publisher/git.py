# Imports
from __future__ import print_function

import sys
import os
import subprocess

# =====================================
# Define Constants
# =====================================

# Directories
HOME_DIRECTORY = os.path.expanduser("~/")
GIT_DIRECTORY = os.path.expanduser("~/git")
REPO_DIRECTORY = os.path.expanduser("~/git/content-production")

# =====================================
# Reused functions
# =====================================


def git_installed():
    try:
        subprocess.check_output(['git', '--version'])
    except OSError:
        return False

    return True


def call_command_and_print_exception(command, message):
    try:
        return subprocess.check_output(command)
    except Exception:
        print(message)
        raise


def check_and_create_directory(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except Exception:
        print("Could not find or create the directory")
        raise

# =====================================
# Command functions
# =====================================


def setup_users_machine():
    """
    User Setup for publish
        1. Check if git is installed
        2. Setup SSH
        3. Cloning the repo and git pull
    """

    """
    Part 1 - Check if git is installed
    """
    if not git_installed():
        if 'win' in sys.platform.lower():
            print(
                'Please install Github for windows '
                'from https://desktop.github.com/ '
                'before coming back and continuing '
                'and running setup again.'
            )
            sys.exit(1)

    """
    Part 2 - Setup SSH
        1. Configure .ssh/config file
        2. Change directory to <user>/git
    """
    # Change to home directory directory
    os.chdir(HOME_DIRECTORY)

    # Create .ssh directory and config file
    ssh_config_stanza = (
        'Host studio-git.touchsurgery.com\n'
        ' User ubuntu\n'
        ' IdentitiesOnly true\n'
        ' IdentityFile ~/.ssh/touchsurgery-studio.pem\n'
    )
    try:
        print("Creating .ssh and config file")
        check_and_create_directory(".ssh")

        # If the file exists, check it doesn't have the texts and if it doesn't, add it
        if os.path.exists('.ssh/config'):
            with open('.ssh/config', 'r') as config_file:
                current_config_text = config_file.read()
            with open('.ssh/config', 'a') as config_file:
                if ssh_config_stanza not in current_config_text:
                    config_file.write('\n' + '\n' + ssh_config_stanza)

        # If the file doesn't exist, make it and add text
        else:
            with open('.ssh/config', 'w+') as config_file:
                config_file.write(ssh_config_stanza)
    except OSError as e:
        print("There was a problem with the ssh config setup")
        raise e

    # Move now to <user>/git for part 2
    check_and_create_directory(GIT_DIRECTORY)
    os.chdir(GIT_DIRECTORY)

    """
    Part 3 - Cloning the repo:
        1. Install lfs
        2. Clone repo
        3. Change directory to the new repo
        4. Do a git pull
    """

    # Install lfs
    print("Install lfs")
    call_command_and_print_exception(['git', 'lfs', 'install'], "lfs install failure")

    print("Config lfs")
    call_command_and_print_exception(['git', 'config', '--global', 'lfs.url',
                                      'https://live.touchsurgery.com/api/v3/lfs'], "lfs config failure")
    call_command_and_print_exception(['git', 'config', '--global', 'lfs.activitytimeout', '60'], "lfs config failure")

    # Clone repo
    if not os.path.exists("content-production"):
        print("Cloning repo")
        call_command_and_print_exception(['git', 'lfs', 'clone', 'studio-git.touchsurgery.com:/srv/git/content-repo',
                                          'content-production'], "Clone repo failure")

    # Change directory
    print("Changing directory to new git repo")
    os.chdir(REPO_DIRECTORY)

    # Git Pull
    print("Doing git pull")
    call_command_and_print_exception(['git', 'lfs', 'pull', 'origin', 'master'], "Git pull failure")


def list_procedures():
    """ Lists all current branches of the repository
    """

    if os.path.exists(REPO_DIRECTORY):
        os.chdir(REPO_DIRECTORY)
        unwanted_branches = ['master', '*', '']
        procedure_list = filter(lambda b: b not in unwanted_branches,
                                subprocess.check_output(['git', 'branch']).split())
        print(procedure_list)
        return '\n'.join(procedure_list)

    else:
        print("You do not have the content-production repository, please run the setup command.")


def change_procedure(procedure):
    """Switches git branch to the procedure selected
    """
    try:
        os.chdir(REPO_DIRECTORY)
        subprocess.check_output(['git', 'checkout', procedure])
    except Exception:
        print("Could not find the specified procedure. Make sure you have run setup and entered the correct procedure "
              "name")
        raise
