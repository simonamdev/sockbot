import praw
import OAuth2Util
from pysqlite import Pysqlite
from html2text import html2text  # thank you Aaron Schwartz
from purrtools import pause
from time import sleep, strftime, gmtime

__author__ = 'Simon Agius Muscat, www.github.com/Winter259'

"""
Sockbot was created using assets and imagery from Elite Dangerous, with the permission of Frontier Developments plc,
for non-commercial purposes. It is not endorsed by nor reflects the views or opinions of Frontier Developments and
no employee of Frontier Developments was involved in the making of it.
"""

version = '1.0'
user_agent = 'raspberrypi:sockb0t259:v{} (by /u/Always_SFW)'.format(version)
table = 'socks'
send_delay = 4
cycle_delay = 0.5
words_to_avoid = ['Socket', 'Sockpuppet']
user = 'tfaddy'
subreddits = [
    'elitedangerous',
    'elitetraders',
    'eliteexplorers',
    'eliteminers',
    'eliteracers',
    'elitebountyhunters',
    'elitedangerouspics',
    'elitestories',
    'elitewings',
    'elitehumor',
    'eliteschool',
    'elitetankers',
    'eliteone',
    'eliteoutfitters',
    'fuelrats',
    'unknownartefact',
    'elitealliance',
    'elitemahon',
    'elitewinters',
    'elitehudson',
    'elitetorval',
    'elitelavigny',
    'elitepatreus',
    'aislingduval',
    'kumocrew',
    'eliteantal',
    'elitesirius',
    'elitelivery',
    'EiteDagerous'
]

interactive_mode = input('[?] Run Sockbot in interactive mode? (y/n): ').lower()
interactive_mode = interactive_mode.startswith('y')
testing_mode = input('[?] Run Sockbot in testing mode? (y/n): ').lower()
testing_mode = testing_mode.startswith('y')
if testing_mode:
    user = 'Always_SFW'
    table = 'test'
    subreddits = ['sockbottery']


def get_comment_id_list(db, table_name):
    comment_id_list = []
    data = db.get_db_data(table_name)
    for row in data:
        comment_id_list.append(row[1])
    return comment_id_list


def main():
    cycle = 1
    startup_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print('[!] Sockbot version {} starting at: {}'.format(version, startup_time))
    print('[!] Sockbot arguments: Testing Mode: {} Interactive Mode: {}'.format(testing_mode, interactive_mode))
    database = Pysqlite('socksdb', 'socks.db')  # initialise the database
    print('[!] Sockbot is initialising connection to Reddit...')
    r = praw.Reddit(user_agent=user_agent)
    o = OAuth2Util.OAuth2Util(r, server_mode=True)
    o.refresh(force=True)  # avoids having to refresh the token manually
    print('[!] Sockbot is now connected to Reddit')
    while True and interactive_mode:
        print('[!] Options list:')
        print('\t[1] Show messages')
        print('\t[2] Send message')
        print('\t[3] Reply to a Redditor')
        print('\t[4] Exit')
        choice = int(input('[?] What needs doing?: '))
        if choice == 1:
            print('[+] Getting messages...')
            messages = r.get_messages()  # double false keeps them unread for now
            for pm in messages:
                if 'sockbot' not in str(pm.author):
                    print('\nFrom: {}'.format(pm.author))
                    print(pm.body.strip())
        elif choice == 2:
            recipient = input('[?] Who do you want to message: ')
            if len(recipient) > 0:
                title = input('[?] What will the title be: ')
                message = input('[?] What shall I send to {}: '.format(recipient))
                try:
                    r.send_message(recipient, title, message)
                    print('[+] Successfully messaged {}'.format(recipient))
                except Exception as e:
                    print('[-] Exception occurred: {}'.format(e))
            else:
                print('[-] No recipient specified')
        elif choice == 3:
            redditor_name = input('[?] Which Redditor will I recover comments of: ')
            redditor = r.get_redditor(redditor_name)
            comment_amount = int(input('[?] How many comments shall I retrieve?: '))
            if comment_amount is None:
                comment_amount = 5
            comment_id_array = []
            try:
                comments = redditor.get_comments(limit=comment_amount)
                for comment in comments:
                    comment_id_array.append(comment)
                    print('[+] Comment Index: {} Comment ID: {} Comment permalink: {}'.format(
                        comment_id_array.index(comment),
                        comment.id,
                        comment.permalink
                    ))
            except Exception as e:
                print('[-] Unable to retrieve submission: {}'.format(e))
            finally:
                comment_id = int(input('[?] Index to reply to: '))
                comment_required = comment_id_array[comment_id]
                comment_reply_text = input('[?] Comment reply body: ')
                try:
                    print('[!] Replying to comment ID: {} with: {}'.format(
                        comment_id_array[comment_id],
                        comment_reply_text
                    ))
                    comment_required.reply(comment_reply_text)
                except Exception as e:
                    print('[-] Could not reply to the comment: {}'.format(e))
        elif choice == 4:
            print('[!] Bye! :)')
            exit()
        else:
            print('[-] Unrecognized input :(')
    while True:
        print('[+] Sockbot cycle: {}'.format(cycle))
        cycle += 1
        socks_spotted = 0  # amount of socks currently present in the comments. Also includes those already in DB
        for subreddit in subreddits:
            try:
                all_comments = r.get_comments(subreddit)
            except Exception as e:
                print('[-] Exception occurred: {}'.format(e))
            else:
                print('[+] Sockbot is checking /r/{}  '.format(subreddit))
                try:
                    for comment in all_comments:
                        print('[+] Checking comment with ID: {}    '.format(comment.id), end='\r')
                        if 'sock' in comment.body.lower() and not comment.author.name == 'sockbot259':
                            avoid_word_present = False  # check for words you are supposed to avoid, like 'Socket'
                            for bad_word in words_to_avoid:
                                if bad_word.lower() in comment.body.lower():
                                    print('[-] Comment with ID: {} is invalid'.format(comment.id))
                                    avoid_word_present = True
                                    break
                            if avoid_word_present:
                                break  # avoid extra iterations, go to the next comment
                            else:
                                # if sock is not in the database, put it in and contact the user
                                socks_spotted += 1
                                if comment.id not in get_comment_id_list(database, table):
                                    # add the comment to the database, then send the message
                                    print('[!] Sockbot found a sock! Placing ID: {} in the database'.format(comment.id))
                                    database.insert_db_data(table, '(NULL, ?, CURRENT_TIMESTAMP)', (comment.id,))
                                    pk_id = database.dbcur.execute('SELECT max(id) FROM {}'.format(table)).fetchone()[0]
                                    message_string = '<h1>Sock #{} was spotted at:</h1> {} <br><hr><br>' \
                                                     'Post contents: <p>{}</p><br>' \
                                                     'Post time: <b>{}</b><br>'.format(
                                                        pk_id,
                                                        comment.permalink,
                                                        comment.body,
                                                        strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                                     )
                                    if not subreddit == 'EiteDagerous' and not comment.body.lower() == 'sock':
                                        print('[!] Sending string about sock #{}'.format(pk_id))
                                        r.send_message(user, 'Sock #{} spotted!'.format(pk_id), html2text(message_string))  # user, title, contents
                                    reply_string = '[ಠ‿ಠ]<br><br>' \
                                                   '<h1>SOCK DETECTED</h1><br><br>' \
                                                   'tfaddy has been notified.<br>' \
                                                   '<hr><br>' \
                                                   'I am <a href=https://imgur.com/RKuioGf">an automated bot on a Raspberry Pi</a>, created and maintained by <a href ="https://www.reddit.com/user/Always_SFW">CMDR Purrcat, /u/Always_SFW</a>.<br>' \
                                                   'Click <a href="https://www.reddit.com/r/EliteDangerous/comments/3sz817/learn_how_to_get_ripped_in_4_weeks/cx261wx">here</a> to find out why I exist. You can find my source code <a href="https://github.com/Winter259/sockbot">on Github</a>.<br>' \
                                                   'Socks detected so far: <b>{}</b><br>' \
                                                   'Online since: <b>{} (GMT)</b><br>'.format(pk_id, startup_time)
                                    post_string = html2text(reply_string)
                                    post_string += 'Need something to keep your feet warm? How about some [ELITE DANGEROUS SOCKS??](https://www.frontierstore.net/merchandise/elite-dangerous-logo-socks-black.html)'
                                    if subreddit == 'EiteDagerous':
                                        post_string = 'ಠ_ಠ'
                                    # if the comment is unimaginative...
                                    if comment.body.lower() == 'sock':
                                        post_string = 'You could try to be a bit more imaginative with your post...'
                                    if comment.author.name == 'tfaddy':
                                        post_string = 'Hey man, I\' your biggest fan!'
                                    print('[!] Replying to comment with ID: {}'.format(comment.id))
                                    comment.reply(post_string)
                                    pause('Holding after sending message', send_delay)
                                else:
                                    print('[-] Comment with ID: {} is already in database'.format(comment.id))
                except Exception as e:
                    print('[-] Comment parse exception:'.format(e))
                sleep(cycle_delay)
        print('[+] Current amount of socks in DB: {}, Instances found this cycle: {}'.format(len(get_comment_id_list(database, table)), socks_spotted))

if __name__ == '__main__':
    main()
