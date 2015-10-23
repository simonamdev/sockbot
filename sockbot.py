import praw

version = '0.1'
user_agent = '/r/elitedangerous sockbot v{} by /u/Always_SFW'.format(version)

def main():
    r = praw.Reddit(user_agent=user_agent)

if __name__ == '__main__':
    main()