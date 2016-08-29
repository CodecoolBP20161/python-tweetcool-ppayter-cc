import argparse
import ipaddress
import json
import requests as r


parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host",
                    help="IP address of the Tweetcool server",
                    default='127.0.0.1')  # Equals 'localhost'
parser.add_argument("-P", "--port",
                    help="Post used by the Tweetcool server",
                    type=int,
                    default=9876)
args = parser.parse_args()

try:
    server = {
        'host': ipaddress.ip_address(args.host),
        'port': args.port
    }
except ValueError as e:
    print('The given host is not a valid IP address')
    exit(0)

if not(1024 < server["port"] < 65535):
    print('The given port number is not in the range between 1024 and 65535!')
    exit(0)

server["address"] = 'http://' + server["host"].compressed + ':' + str(server["port"])

# Logic starts here... somewhere..

'''Client

The client is responsible to represent the previously saved tweets and to
collect new ones from the user.

Expected behavior

The client should be a console application running until the user enters
"exit" or presses Ctrl+D.
It should run in a loop, and with every running it should perform the following:

- Query tweets from the server
- Format and print the previous tweets. Example:
    Chewbacca <1977-05-25 20:16:10>: Uuuuuuurr Ahhhhrrr Uhrrr
- Ask the user for message input. (also allow refreshing the list and exiting)
- Also handle all possible exceptions, even Ctrl+D exiting the application.'''


def write_post():
    poster = input('\nEnter your name:  \n')
    content = input('\nWrite something: \n')
    tweet = {'poster': poster, 'content': content}
    post = r.post(server['address']+'/tweet', json=tweet)


def read_posts():
    pass


def main_menu():
    header_color = '\033[95m'
    warning_color = '\033[91m'
    end_color = '\033[0m'

    warning_text = ''
    header_text = (header_color + '\nTweetCool 🐦' + end_color)
    choice = None
    try:
        while choice != '0':
            print(header_text)
            read_posts()
            print(header_text)
            print(warning_text)
            print('1: refresh tweets \n2: write a tweet \n0: quit')
            choice = input('Enter an option: ').lower().strip()
            if choice == '1':
                read_posts()
            elif choice == '2':
                write_post()
            elif choice == '0':
                print(warning_color + '\nbye-bye' + end_color)
                break
            else:
                warning_text = (warning_color + '\ninvalid option' + end_color)

    except (EOFError, KeyboardInterrupt):
        print(warning_color + '\n\nrage quit lol' + end_color)

main_menu()
