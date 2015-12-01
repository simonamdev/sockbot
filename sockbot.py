import praw
import OAuth2Util
from pysqlite import Pysqlite
from html2text import html2text  # thank you Aaron Schwartz
from purrtools import pause
from time import sleep, strftime, gmtime

"""
Sockbot was created using assets and imagery from Elite Dangerous, with the permission of Frontier Developments plc,
for non-commercial purposes. It is not endorsed by nor reflects the views or opinions of Frontier Developments and
no employee of Frontier Developments was involved in the making of it.
"""

version = '0.7.1'
user_agent = 'windows:sockb0t259:v{} (by /u/Always_SFW)'.format(version)
testing_mode = False  # switch to test DB and criteria
words = ['sock', 'SOCK', 'Sock']
avoid_words = ['socket', 'SOCKET']
table = 'socks'
user = 'tfaddy'
send_delay = 5
cycle_delay = 1
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
    'elitelivery'
]


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
    database = Pysqlite('socksdb', 'socks.db')
    r = praw.Reddit(user_agent=user_agent)
    o = OAuth2Util.OAuth2Util(r, server_mode=True)
    o.refresh(force=True)  # avoids having to refresh the token manually
    while True:
        print('[+] Sockbot cycle: {}. Searching for: {}'.format(cycle, words))
        cycle += 1
        socks_spotted = 0  # amount of socks currently present in the comments. Also includes those already in DB
        for subreddit in subreddits:
            try:
                all_comments = r.get_comments(subreddit)
            except Exception as e:
                print('[-] Exception occurred:', e)
            else:
                print('[+] Sockbot is checking /r/{}'.format(subreddit))
                try:
                    for comment in all_comments:
                        for word in words:
                            if word in comment.body and word not in avoid_words and 'tfaddy has been notified' not in comment.body:  # need to make a list of actual non sock references
                                # if sock is not in the database, put it in and contact the user
                                socks_spotted += 1
                                if comment.id not in get_comment_id_list(database, table):
                                    # add the comment to the database, then send the message
                                    print('[!] Sockbot found a sock! Placing ID: {} in the database'.format(comment.id))
                                    database.insert_db_data(table, '(NULL, ?, CURRENT_TIMESTAMP)', (comment.id,))
                                    pk_id = database.dbcur.execute('SELECT max(id) FROM {}'.format(table)).fetchone()[0]
                                    message_string = 'Sock #{} was spotted at: {}. If I broke somehow, contact /u/Always_SFW! or get /u/SpyTec13 to ban me! I have been online since: {}'.format(pk_id, comment.permalink, startup_time)
                                    print('[!] Sending string:')
                                    print('\t', message_string)
                                    r.send_message(user, 'Sock #{} spotted!'.format(pk_id), message_string)
                                    reply_string = '<h1>SOCK DETECTED</h1><br><br>' \
                                                   'tfaddy has been notified.<br><hr><br>' \
                                                   '<i>I am a bot, created and maintained by <a href ="https://www.reddit.com/user/Always_SFW">CMDR Purrcat</a><br>' \
                                                   'Click <a href="https://www.reddit.com/r/EliteDangerous/comments/3sz817/learn_how_to_get_ripped_in_4_weeks/cx261wx">here</a> to find out why I exist.<br>' \
                                                   'You can find my source code <a href="https://github.com/Winter259/sockbot">on github</a><br>' \
                                                   'Socks detected so far: <b>{}</b><br>' \
                                                   'Online since: <b>{}</b> (GMT)<br>' \
                                                   'SOCKBOT IS HYPED FOR HORIZONS!! ARE YOU??<br>' \
                                                   'Sockbot current version: <b>{}</b></i>'.format(pk_id, startup_time, version)
                                    post_string = html2text(reply_string)
                                    print('[!] Replying with:')
                                    print(post_string)
                                    comment.reply(post_string)
                                    pause('Holding after sending message', send_delay)
                except Exception as e:
                    print('[-] Exception occurred whilst attempting to parse the comments')
                    print('[-] Exception:', e)
                sleep(cycle_delay)
        print('[+] Current amount of socks in DB: {}, Instances found this cycle: {}'.format(len(get_comment_id_list(database, table)), socks_spotted))

if __name__ == '__main__':
    main()
