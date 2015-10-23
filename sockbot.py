import praw
import OAuth2Util
import sqlite3

from time import sleep

version = '0.1'
user_agent = 'windows:sockbot:v{} (by /u/Always_SFW)'.format(version)
testing_mode = True  # switch to test DB
verbose_mode = False
word = 'sock'
table = 'socks'
user = 'tfaddy'
if testing_mode:
    table = 'test'
    word = 'CMDR'
    user = 'Always_SFW'

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
        all_comments = r.get_comments('elitedangerous') # add other elite dangerous subreddits here
        print('[+] Sockbot is looking through the comments for: ', word)
        instances = 0
        for comment in all_comments:
            if verbose_mode:
                try:
                    print(comment.body)
                except Exception:
                    print('[-] Could not print comment!')
                    print(Exception)
            if word in comment.body:
                # if sock is not in the database, put it in and contact the user
                instances += 1

                if not comment.id in get_old_socks(dbcur, table):
                    # add the comment to the database
                    print('[+] Sockbot found a sock! Placing ID: {} in the database'.format(comment.id))

                    dbcur.execute('INSERT INTO {} VALUES (NULL, ?, CURRENT_TIMESTAMP)'.format(table), (comment.id,))
                    dbcon.commit()
                    # send message
                    pk_id = dbcur.execute('SELECT max(id) FROM {}'.format(table)).fetchone()[0]
                    message_string = 'Sock #{} was spotted at: {}. If I broke somehow, contact /u/Always_SFW!'.format(pk_id, comment.submission.url)
                    r.send_message(user, 'Sock #{} spotted!'.format(pk_id), message_string)
                    pause(2)
        cycle += 1
        print('[+] Current amount of socks in DB: {}, Instances found this cycle: {}'.format(len(get_old_socks(dbcur, table)), instances))
        pause(5)

if __name__ == '__main__':
    main()
