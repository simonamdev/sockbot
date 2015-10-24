import praw
import OAuth2Util
import sqlite3

from time import sleep

"""
Sockbot was created using assets and imagery from Elite Dangerous, with the permission of Frontier Developments plc,
for non-commercial purposes. It is not endorsed by nor reflects the views or opinions of Frontier Developments and
no employee of Frontier Developments was involved in the making of it.
"""

version = '0.3'
user_agent = 'windows:sockbot:v{} (by /u/Always_SFW)'.format(version)
testing_mode = False  # switch to test DB and criteria
verbose_mode = False
words = ['sock', 'SOCK']
avoid_words = ['socket', 'SOCKET']
table = 'socks'
user = 'tfaddy'
send_delay = 5
cycle_delay = 10

def pause(time=5):
    time_left = time
    while time_left >= 0:
        print('[+] Sockbot will continue in: {}  '.format(time_left), end='\r')
        time_left -= 1
        sleep(1)

def get_old_socks(cursor, table_name=table):
    old_socks = set()
    for row in cursor.execute('SELECT * FROM {} ORDER BY id'.format(table_name)):
        old_socks.add(row[1])  # id, comment id, timestamp
    return old_socks

def main():
    cycle = 1
    dbcon = sqlite3.connect('socks.db')
    dbcur = dbcon.cursor()
    get_old_socks(dbcur, table)
    r = praw.Reddit(user_agent=user_agent)
    o = OAuth2Util.OAuth2Util(r, server_mode=True)
    o.refresh(force=True)
    while True:
        print('[+] Sockbot cycle: ', cycle)
        try:
            subreddit = r.get_subreddit('elitedangerous')
        except Exception:
            print('[-] ', Exception)
            exit(0)
        try:
            all_comments = r.get_comments('elitedangerous') # add other elite dangerous subreddits here
        except Exception:
            print('[-] ', Exception)
        else:
            print('[+] Sockbot is looking through the comments for: ', words)
            instances = 0  # of the word present in the comments. Also includes those already in DB
            for comment in all_comments:
                if verbose_mode:
                    try:
                        print(comment.body)
                    except Exception:
                        print('[-] Could not print comment!')
                        print(Exception)
                for word in words:
                    if word in comment.body and not word in avoid_words and not 'I am a bot!' in comment.body:  # need to make a list of actual non sock references
                        # if sock is not in the database, put it in and contact the user
                        instances += 1
                        if not comment.id in get_old_socks(dbcur, table):
                            # add the comment to the database, then send the message
                            print('[!] Sockbot found a sock! Placing ID: {} in the database'.format(comment.id))
                            dbcur.execute('INSERT INTO {} VALUES (NULL, ?, CURRENT_TIMESTAMP)'.format(table), (comment.id,))
                            dbcon.commit()
                            pk_id = dbcur.execute('SELECT max(id) FROM {}'.format(table)).fetchone()[0]
                            message_string = 'Sock #{} was spotted at: {}.  If I broke somehow, contact /u/Always_SFW! or get /u/SpyTec13 to ban me!'.format(pk_id, comment.permalink)
                            print('[!] Sending string:')
                            print('\t', message_string)
                            r.send_message(user, 'Sock #{} spotted!'.format(pk_id), message_string)
                            reply_string = 'I see you mentioned socks in some way. I have notified /u/tfaddy. I am a bot! You can find my source code here: https://github.com/Winter259/sockbot'
                            print('[!] Replying with:')
                            print('\t', reply_string)
                            comment.reply(reply_string)
                            pause(send_delay)
            cycle += 1
            print('[+] Current amount of socks in DB: {}, Instances found this cycle: {}'.format(len(get_old_socks(dbcur, table)), instances))
            pause(cycle_delay)

if __name__ == '__main__':
    main()
