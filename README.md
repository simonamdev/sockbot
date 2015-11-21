# sockbot
A reddit bot which checks for mentions of socks in the Elite: Dangerous subreddit and messages /u/tfaddy

Sockbot uses PRAW and PRAW-OAuth2Util to make connecting to reddit super simple. It also uses two modules I wrote myself (pysqlite3 and purrtools) to make the actual script's structure cleaner and simpler.

It works by connecting to reddit, retrieving the last 50 comments from a specific subreddit in the list (I used nearly all of the Elite: Dangerous subreddits as listed in the main subreddit wiki), then searches for variants of the word 'sock' within those comments.

Feel free to star and fork the project if you are interested in the concept, in accordance to the licence provided. Please be aware that forking the project does not include the permission I received from the main subreddit moderator SpyTec to operate this bot. Please seek relevant permissions and read the reddit API wiki before operating a reddit bot such as this one.