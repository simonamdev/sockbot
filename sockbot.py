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
        print('[+] Sockbot is alive!')
        try:
            subreddit = r.get_subreddit('elitedangerous')
        except Exception:
            print('[-] ', Exception)
            exit(0)
        print('[+] Sockbot is retrieving submissions')
        submissions = subreddit.get_hot(limit=10)  # Set limit in config
        for submission in submissions:
            print('[+] Sockbot found thread: ', submission)
            comments = praw.helpers.flatten_tree(submission.comments)
            print('[+] Sockbot is going to check the comments for the word sock')
            for comment in comments:
                print(comment.body)
                if 'sock' in comment.body:  # TODO: check for uppercase SOCK
                    print('[+] Sockbot found a sock!!!!!')
                    sleep(10)
                sleep(1)
            sleep(5)
        sleep(5)

if __name__ == '__main__':
    main()
