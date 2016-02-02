import praw
import OAuth2Util
import csv

version = '1.0'
user_agent = 'raspberrypi:sockb0t259:v{} (by /u/Always_SFW)'.format(version)
print('Initialising')
print('Connecting to Reddit')
r = praw.Reddit(user_agent=user_agent)
o = OAuth2Util.OAuth2Util(r, server_mode=True)
o.refresh(force=True)
print('Connected to reddit')
sockbot = r.get_redditor('sockbot259')
comments = sockbot.get_comments(limit=1024)
comments_list = []
karma_sum = 0
print('Counting karma by comments...')
for row in comments:
    comments_list.append([row.score, row.created_utc])
    karma_sum += row.score
print('Total comments: {}'.format(len(comments_list)))
print('Total karma: {}'.format(karma_sum))
print('Average karma: {}'.format(karma_sum / len(comments_list)))
print('Writing to CSV...')
with open('socks.csv', 'w', newline='') as csvfile:
    sockwriter = csv.writer(csvfile, delimiter=',')
    sockwriter.writerows(comments_list)
    csvfile.close()
print('All done :)')