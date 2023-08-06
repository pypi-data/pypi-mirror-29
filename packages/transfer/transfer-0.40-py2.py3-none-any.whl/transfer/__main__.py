import sys
import argparse
import os
import readline
import glob

import yaml
from colorama import init
from termcolor import colored
try:
    import tensorflow
except ModuleNotFoundError:
    print(colored('Tensorflow not installed!', 'red'))
    print('Note: there are too many system specific things with this module')
    print('Please look up how to install it for your system:')
    print('')
    print(colored('https://www.tensorflow.org/install/', 'yellow'))
    print('')
    raise ModuleNotFoundError
import keras

from transfer.project import configure, configure_server, select_project, update_config, import_config, export_config
from transfer import images_to_array, pre_model
from transfer.model import train_model
from transfer.predict_model import predict_model
from transfer.augment_arrays import augment_arrays
from transfer.input import model_input, model_individual_input, str_input
from transfer.server import start_server


class Completer(object):
    def path_completer(self, text, state):
        return [os.path.join(x, '') if os.path.isdir(x) else x for x in glob.glob(os.path.expanduser(text) + '*')][state]


def main(args = None):
    '''
    Main entry point for transfer command line tool.

    This essentially will marshall the user to the functions they need.
    '''

    parser = argparse.ArgumentParser(description = 'Tool to perform transfer learning')

    parser.add_argument('-c','--configure',
                        action = 'store_true',
                        help = 'Configure transfer')

    parser.add_argument('-e','--export',
                        action = 'store_true',
                        dest = 'export_config',
                        help = 'Export configuration and models')

    parser.add_argument('-i','--import',
                        action = 'store',
                        type = str,
                        default = None,
                        dest = 'import_config',
                        help = 'Import configuration and models')

    parser.add_argument('-p','--project',
                        action = 'store',
                        type = str,
                        default = None,
                        dest = 'project',
                        help = 'Specify a project, if not supplied it will be picked from configured projects')

    parser.add_argument('-r','--run',
                        action = 'store_true',
                        help = 'Run all transfer learning operations')

    parser.add_argument('-f','--final',
                        action = 'store_true',
                        help = 'Run final training on all layers: Warning SLOW!')

    parser.add_argument('-l','--last-weights',
                        action = 'store_true',
                        dest = 'last',
                        help = 'Restart from the last weights, rather than the best intermediate weights')

    parser.add_argument('--predict',
                        action = 'store',
                        type = str,
                        default = None,
                        const = 'default',
                        dest = 'predict',
                        nargs='?',
                        help = 'Predict model on file or directory')

    parser.add_argument('--prediction-rest-api',
                        action = 'store_true',
                        dest = 'rest_api',
                        help = 'Start rest api to make predictions on files or directories')

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.import_config is not None:
        import_config(args.import_config)
        return
    elif args.export_config:
        project = select_project(args.project)
        weights = model_input(project)
        ind = model_individual_input(project, weights)
        export_config(project, weights, ind)
        return
    elif args.configure:
        configure()
        return
    else:
        project = select_project(args.project)

    if args.run:

        if project['is_array'] == False:
            project = images_to_array(project)
            update_config(project)

        if project['is_augmented'] == False:
            project = augment_arrays(project)
            update_config(project)

        if project['is_pre_model'] == False:
            project = pre_model(project)
            update_config(project)

        project = train_model(project, final = args.final, last = args.last)
        update_config(project)

        print('')
        print(colored('Completed modeling round: ' + str(project['model_round']), 'cyan'))
        print('')
        print('Best current model: ', colored(project['best_weights'], 'yellow'))
        print('Last current model: ', colored(project['last_weights'], 'yellow'))
        print('')
        print('To further refine the model, run again with:')
        print('')
        print(colored('    transfer --run --project ' + project['name'], 'green'))
        print('')
        print('To make predictions:')
        print('')
        print(colored('    transfer --predict [optional dir or file] --project ' + project['name'], 'yellow'))
        print('')

    elif args.rest_api:
        if project['server_weights'] is not None:
            start_server(project, 'server_weights')

        elif project['best_weights'] is not None:
            weights = model_input(project)
            start_server(project, weights)

        else:
            print('Model is not trained.  Please first run your project:')
            print('')
            print(colored('    transfer --run', 'green'))
            print('')
    elif args.predict is not None:
        if args.predict == 'default':

            completer = Completer()
            readline.set_completer_delims('\t')
            readline.parse_and_bind('tab: complete')
            readline.set_completer(completer.path_completer)
            args.predict = str_input('Enter a path to file(s): ')
        if project['server_weights'] is not None:
            predict_model(project, 'server_weights', args.predict)

        elif project['best_weights'] is not None:
            weights = model_input(project)
            print('Predicting on image(s) in: ', colored(args.predict, 'yellow'))
            predict_model(project, weights, args.predict)

        else:
            print('Model is not trained.  Please first run your project:')
            print('')
            print(colored('    transfer --run', 'green'))
            print('')
