'''
Script to manually execute actions on the AI Side client. Mainly used for debugging purposes.
'''

import dolphin_client_api as dca
import argparse

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='AI Side client manual execution')
    parser.add_argument('--action', type=str, help='The action to perform')
    args = parser.parse_args()

    # Perform the action
    if args.action == 'reset':
        dca.reset()
    elif args.action == 'get_observation':
        dca.get_observation()
    else:
        print('Invalid action')
    