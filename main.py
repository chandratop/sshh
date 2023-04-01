import argparse, json, os
from simple_term_menu import TerminalMenu
from subprocess import run

# ANSI escape codes for different colors
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\u001b[33m'
RESET = '\033[0m'

def coloredInput(s, color, e='\n'):
    """
    This function prints the text in a particular color
    Choose one of red, green, blue or yellow

    :param s: The string you want to print
    :param color: The color you want to print with
    """

    colors = {'red': RED, 'green': GREEN, 'blue': BLUE, 'yellow': YELLOW}
    return input(f'{colors[color]}{s}{RESET}')

def coloredPrint(s, color, e='\n'):
    """
    This function prints the text in a particular color
    Choose one of red, green, blue or yellow

    :param s: The string you want to print
    :param color: The color you want to print with
    """

    colors = {'red': RED, 'green': GREEN, 'blue': BLUE, 'yellow': YELLOW}
    print(f'{colors[color]}{s}{RESET}')

def optionizer(options, prompt, show=True):
    """
    This function displays a menu on the terminal screen which can be
    navigated using up & down arrow keys and enter for selection

    :param options: A list of string texts as valid options to choose from
    :param prompt: The text prompt for the options menu
    :param show(=True): Choice to display the option selected

    :return: The option chosen
    """

    menu = TerminalMenu(options, title=prompt)
    index = menu.show()
    if show:
        coloredPrint(prompt, 'blue', e= ' ')
        print(options[index])
    return options[index]

def getHome():
    """
    This function returns the absolute path to the home directory
    """

    return os.path.expanduser('~')

def setPath(path, item):
    """
    This function creates the path

    :param path: The absolute path
    :param item: The directory name of the current item

    :return: constructed absolute path
    """

    return os.path.join(path, item)

def setOptions(current, dirs):
    """
    This function is used in the traverse function to return a list of directories

    :param current: The current folder name
    :param dirs: The directories list

    :return: list of directories for optionizer
    """

    dirs.sort()
    return ['Go Back'] + dirs + [f'Select [{current}]?']

def getDirs(path):
    """
    This function returns a list of directories in a directory path

    :param path: The path of the directory whose directories we want

    :return: list of directories for inside the path
    """

    dirs = list()
    for item in os.listdir(path):
        item_path = setPath(path, item)
        if os.path.isdir(item_path):
            dirs.append(item)
    return dirs

def traverse(prompt, path=getHome()):
    """
    This function creates a options menu and helps the user navigate their directories

    :param prompt: A string to display on top
    :param path: Home directory path [default args]

    :return: a dictionary with the current and previous directories in the traversal stack
    """

    current = ['', path]
    stack = list([current])
    while (choice := optionizer(setOptions(current[0], getDirs(current[1])), prompt, show=False)) != f'Select [{current[0]}]?':
        if choice == 'Go Back':
            if len(stack) > 1:
                removed = stack.pop(-1)
                current = stack[-1]
        else:
            current = [choice, setPath(stack[-1][1], choice)]
            stack.append(current)
    return {'current': current, 'prev': stack[-2]}

def do(args):
    """
    This function resolves the arguments and performs the ssh commands

    :param args: The arguments from argparse
    """

    # Open the config.json file as a dict
    with open(__file__.replace('main.py', 'configs.json'), 'r+') as configs_file:
        configs = json.load(configs_file)
    if configs['pem'] == '':
        configs['pem'] = traverse('Navigate to the folder where you are storing your pem files ')['current'][1]
    with open(__file__.replace('main.py', 'configs.json'), 'w') as configs_file:
        json.dump(configs, configs_file, indent=4)
    if args.add != None:
        friendlyName = args.add
        ip = coloredInput('Enter the IP: ', 'blue')
        files = [f for f in os.listdir(configs['pem']) if f[-4:] == '.pem']
        pem = optionizer(files, f'Choose the pem file for {friendlyName} ')
        # Check if the friendly name has been used already
        if friendlyName in configs['names']:
            if optionizer(['yes', 'no'], 'The friendly name you entered already exists, do you want to overwrite it? ') == 'yes':
                configs['names'][friendlyName] = f'ssh -i {configs["pem"]}/{pem} ubuntu@{ip}'
                configs['ips'][ip] = f'ssh -i {configs["pem"]}/{pem} ubuntu@{ip}'
        else:
            configs['names'][friendlyName] = f'ssh -i {configs["pem"]}/{pem} ubuntu@{ip}'
            configs['ips'][ip] = f'ssh -i {configs["pem"]}/{pem} ubuntu@{ip}'
        with open(__file__.replace('main.py', 'configs.json'), 'w') as configs_file:
            json.dump(configs, configs_file, indent=4)
        if optionizer(['yes', 'no'], f'Do you want to ssh into {friendlyName}?') == 'yes':
            run(configs['names'][friendlyName], shell=True)
    elif args.ip != None:
        if args.ip in configs['ips']:
            run(configs['ips'][args.ip], shell=True)
        else:
            coloredPrint('IP not present, to register this IP run sshh -a/--add', 'red')
    elif args.name != None:
        if args.name in configs['names']:
            run(configs['names'][args.name], shell=True)
        else:
            coloredPrint('Friendly name not present, to register this name run sshh -a/--add', 'red')
    else:
        keys = list(configs['names'].keys())
        if len(keys) == 0:
            coloredPrint('No ssh instances configured, exiting...', 'green')
            exit(0)
        choice = optionizer(keys, 'Choose the ssh instance name ')
        run(configs['names'][choice], shell=True)

def main():
    parser = argparse.ArgumentParser(description='An ssh helper when you have too many ssh hosts')
    parser.add_argument('-i', '--ip', type=str, required=False, help='The IP for the instance')
    parser.add_argument('-n', '--name', type=str, required=False, help='A friendly name for the instance')
    parser.add_argument('-a', '--add', type=str, required=False, help='Add a new ssh')
    args = parser.parse_args()
    do(args)

if __name__ == '__main__':
    main()