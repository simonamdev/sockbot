import config
import praw

version = '0.1'

def main():
    r = praw.Reddit(user_agent=config.user_agent)

if __name__ == '__main__':
    main()