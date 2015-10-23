import praw
import OAuth2Util
import sqlite3

from time import sleep

version = '0.1'
user_agent = 'windows:sockbot:v{} (by /u/Always_SFW)'.format(version)
testing_mode = True  # switch to test DB
table = 'socks'
if testing_mode:
    table = 'test'

def get_old_socks(cursor, table_name=table):
    old_socks = set()
    for row in cursor.execute('SELECT * FROM {} ORDER BY id'.format(table_name)):
        old_socks.add(row[1])  # id, comment id, timestamp
    return old_socks

def main():
    dbcon = sqlite3.connect('socks.db')
    dbcur = dbcon.cursor()
    get_old_socks(dbcur, table)
    r = praw.Reddit(user_agent=user_agent)
    o = OAuth2Util.OAuth2Util(r, server_mode=True)
    o.refresh(force=True)
    while True:
        print('[+] Sockbot is starting a cycle')
        try:
            subreddit = r.get_subreddit('elitedangerous')
        except Exception:
            print('[-] ', Exception)
            exit(0)
        print('[+] Sockbot is retrieving comments')
        all_comments = r.get_comments('elitedangerous') # add other elite dangerous subreddits here
        for comment in all_comments:
            try:
                print(comment.body)
            except Exception:
                print('[-] Could not print comment!')
                print(Exception)
            else:
                if 'CMDR' in comment.body:
                    print('[+] Sockbot found a sock!!!!')
                    # check if the sock is already in the database
                    if comment.id in get_old_socks(dbcur, table):
                        print('[+] Sockbot already has a record of this entry')
                    else:
                        # add the comment to the database
                        dbcur.execute('INSERT INTO {} VALUES (NULL, ?, CURRENT_TIMESTAMP)'.format(table), (comment.id,))
                        dbcon.commit()
                        # add send a message function here
                        sleep(2)
        print('[+] Sockbot has finished a cycle')
        print('Contents of db:')
        for row in dbcur.execute('SELECT * FROM {} ORDER BY id'.format(table)):
            print(row)
        print('[+] Sockbot will start another cycle in 5 seconds')  # replace with pause function
        sleep(5)

if __name__ == '__main__':
    main()
