import praw
import OAuth2Util
import csv
import os
from time import sleep
from pprint import pprint
from tqdm import tqdm


version = '1.0'
user_agent = 'raspberrypi:sockb0t259:v{} (by /u/Always_SFW)'.format(version)
print('Initialising')
commenter_counts = dict()
if not os.path.isfile('commenters.csv'):
    print('Connecting to Reddit')
    r = praw.Reddit(user_agent=user_agent)
    o = OAuth2Util.OAuth2Util(r, server_mode=True)
    o.refresh(force=True)
    print('Connected to reddit')
    sockbot = r.get_redditor('sockbot259')
    print('Getting comments')
    comments = sockbot.get_comments(limit=1024)
    print('Getting parent IDs for comments')
    parent_ids = [comment.parent_id for comment in comments]
    print('Determining parent comment authors')
    for parent_id in tqdm(parent_ids):
        parent = r.get_info(thing_id=parent_id)
        # print(parent.author)
        try:
            commenter_counts[str(parent.author)] += 1
        except KeyError:
            commenter_counts[str(parent.author)] = 1
        sleep(1)
    with open('commenters.csv', 'w', newline='') as csvfile:
        sockwriter = csv.writer(csvfile, delimiter=',')
        for commenter, count in commenter_counts.items():
            sockwriter.writerow([commenter, count])
        csvfile.close()
else:
    with open('commenters.csv', 'r', newline='') as csvfile:
        sockreader = csv.reader(csvfile, delimiter=',')
        for name, count in sockreader:
            commenter_counts[name] = count
sorted_dict = [(key, int(value)) for key, value in commenter_counts.items()]
print(type(sorted_dict))
print(type(sorted_dict[0]))
pprint(sorted(sorted_dict, key=lambda comm: comm[1]))
