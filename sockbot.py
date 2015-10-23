import praw
import OAuth2Util

from time import sleep

version = '0.1'
user_agent = 'windows:sockbot:v{} (by /u/Always_SFW)'.format(version)

def main():
    r = praw.Reddit(user_agent=user_agent)
    o = OAuth2Util.OAuth2Util(r, server_mode=True)
    while True:
        o.refresh()
        print(r.get_me().comment_karma)
        sleep(3600)

if __name__ == '__main__':
    main()
