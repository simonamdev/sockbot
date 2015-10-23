import praw
import OAuth2Util

from time import sleep

version = '0.1'
user_agent = 'windows:sockbot:v{} (by /u/Always_SFW)'.format(version)

def main():
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
            print(comment.body)
            if 'sock' in comment.body:
                print('[+] Sockbot found a sock!!!!')
                # add send a message function here
                sleep(5)
            sleep(0.1)
        print('[+] Sockbot has finished a cycle')
        sleep(5)

if __name__ == '__main__':
    main()
