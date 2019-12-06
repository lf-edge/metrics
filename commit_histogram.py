#!/usr/bin/python3

import os, sys
import subprocess

# Retrieve the git log of the current directory with line change stats (except renames and type changes)
GIT_LOG_CMD = ['git', 'log', '--pretty=format:%aI%x20%ae', '--diff-filter=rt', '--numstat']
#print(' '.join(GIT_LOG_CMD))

quarterly = False
quarter = {
    "01": "Q1",
    "02": "Q1",
    "03": "Q1",
    "04": "Q2",
    "05": "Q2",
    "06": "Q2",
    "07": "Q3",
    "08": "Q3",
    "09": "Q3",
    "10": "Q4",
    "11": "Q4",
    "12": "Q4",
}
if '--quarterly' in sys.argv:
    quarterly = True
    del sys.argv[sys.argv.index('--quarterly')]

stats = dict()
commits = dict()
authors = dict()

basedir = os.getcwd()

# Iterate through every local repo passed as a command-line argument
for repo in sys.argv[1:]:
    os.chdir(os.path.join(basedir, repo))
    log = os.popen(' '.join(GIT_LOG_CMD))

    month = None
    for line in log:
      args = line.split()
      if len(args) == 2:
          if quarterly:
              month = args[0][:5] + quarter[args[0][5:7]]
          else:
              month = args[0][:7]
          if month not in stats:
              stats[month] = 0
          if month not in commits:
              commits[month] = 0
          commits[month] += 1

          if month not in authors:
              authors[month] = dict()
          author = args[1]
          if author not in authors[month]:
            authors[month][author] = 1

      elif len(args) == 3:
          if args[2].startswith('vendor'):
              continue
          try:
              added = abs(int(args[0]))
              removed = abs(int(args[1]))
              stats[month] += max(added, removed)# the larger value
          except ValueError:
              pass

cumulative_commits = 0
cumulative_stats = 0
cumulative_authors = set()
print('Month\t\tCommits\t\tLoC\t\tAuthors')
for month in sorted(stats):
    cumulative_commits += commits[month]
    cumulative_stats += stats[month]
    author_count = 0
    for author in authors[month]:
        author_count += authors[month][author]
        cumulative_authors.add(author)
    print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (month, commits[month], cumulative_commits, stats[month], cumulative_stats, author_count, len(cumulative_authors)))



