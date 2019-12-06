#!/usr/bin/python3

import os, sys
import subprocess

COMPANY_MAP = {
    "darko.draskovic@gmail.com": "Mainflux",
    "drasko.draskovic@gmail.com": "Mainflux",
    "dylanhantula@gmail.com": "Hitachi Vantara",
    "ecotter@gmail.com": "Dell",
    "gkorland@gmail.com": "Redis",
    "jpwhite_mn@yahoo.com": "Dell",
    "me@michaelestrin.com": "Dell",
    "mhall119@gmail.com": "LF",
    "tonyespy@users.noreply.github.com": "Canonical",
    "trcox92@yahoo.com": "Dell",
    "sftwr2020@gmail.com": "Dell",
    "paul@paulcarver.us": "ATT",
    "anthonymbonafide@gmail.com": "Dell",
    "trevor@mykolab.com": "Dell",
    "its-jira@gerrit": "LF",
    "gerrit@akraino.org": "LF",
    "brandonforster@gmail.com": "Dell",
    "brandonforster@users.noreply.github.com": "Dell",
    "37156729+tingyuz@users.noreply.github.com": "RSA",
    "tingyuz@bbtesting.4aismw15ukyupc1jjpikartq1d.bx.internal.cloudapp.net": "RSA",
    "38766128+iain-anderson@users.noreply.github.com": "IoTech",
    "44779287+lenny-intel@users.noreply.github.com": "Intel",
    "47606926+robertIntel@users.noreply.github.com": "Intel",
    "chadbyoung@gmail.com": "Dell",
    "changdavid418@gmail.com": "IoTech",
    "cherry@iotechwork.c.vivid-memento-211611.internal": "IoTech",
    "cloudxxx8@gmail.com": "IoTech",
    "dweomer5@gmail.com": "Intel",
    "huaqiao@huaqiao.local": "VMWare",
    "jdharms@gmail.com": "Dell",
    "jeremyphelps@linux.com": "LF",
    "leonard.goodell@inyel.com": "Intel",
    "michaelestrin@users.noreply.github.com": "Dell",
    "motifmike@gmail.com": "Intel",
    "weichou1229@gmail.com": "IoTech",
    "yanghua1127@gmail.com": "Tencent",
    "45495032+eno-intel@users.noreply.github.com": "Intel",
    "43240457+FelixTing@users.noreply.github.com": "IoTech",
    "andre.srinivasan@gmail.com": "Redis",
    "jbonafide623@gmail.com": "Dell",
    "knitzsche@users.noreply.github.com": "Canonical",
    "51793905+dvintel@users.noreply.github.com": "Intel",
    "47606926+robertIntel@users.noreply.github.com": "Intel",
    
}

DOMAIN_MAP = {
    "nokia.com": "Nokia",
    "att.com": "ATT",
    "research.att.com": "ATT",
    "dell.com": "Dell",
    "amer.dell.com": "Dell",
    "redhat.com": "Redhat",
    "huawei.com": "Huawei",
    "arm.com": "ARM",
    "ericsson.com": "Ericsson",
    "linuxfoundation.org": "LF",
    "contractor.linuxfoundation.org": "LF",
    "vmware.com": "VMWare",
    "intel.com": "Intel",
    "forgerock.com": "ForgeRock",
    "redislabs.com": "Redis",
    "iotechsys.com": "IoTech",
    "canonical.com": "Canonical",
    "cavium.com": "Cavium",
    "caviumnetworks.com": "Cavium",
    "samsung.com": "Samsung",
    "rsa.com": "RSA",
    "tencent.com": "Tencent",
    "enea.com": "Enea",
    "windriver.com": "WindRiver",
    "wipro.com": "WiPro",
    "beechwoods.com": "Beechwoods",
}

def get_company(email):
    email = email.lower()
    if email in COMPANY_MAP:
        return COMPANY_MAP[email]
    domain = email.split('@')[-1]
    if domain in DOMAIN_MAP:
        return DOMAIN_MAP[domain]
    return 'Unknown'

# Retrieve the git log of the current directory with line change stats (except renames and type changes)
GIT_LOG_CMD = ['git', 'log', '--pretty=format:%aI%x20%ae', '--diff-filter=rt', '--numstat']
#print(' '.join(GIT_LOG_CMD))

stats = dict()
commits = dict()

basedir = os.getcwd()

from_date = None
if '--from' in sys.argv:
    from_date = sys.argv[sys.argv.index('--from')+1]
    #print("FROM: %s" % from_date)
    del sys.argv[sys.argv.index('--from')+1]
    del sys.argv[sys.argv.index('--from')]

to_date = None
if '--to' in sys.argv:
    to_date = sys.argv[sys.argv.index('--to')+1]
    #print("TO: %s" % to_date)
    del sys.argv[sys.argv.index('--to')+1]
    del sys.argv[sys.argv.index('--to')]


# Iterate through every local repo passed as a command-line argument
for repo in sys.argv[1:]:
    os.chdir(os.path.join(basedir, repo))
    log = os.popen(' '.join(GIT_LOG_CMD))

    author = None
    for line in log:
      args = line.split()

      if len(args) == 2:
          date = args[0][:10]
          if from_date is not None and date < from_date:
            author = None
            continue;
          if to_date is not None and date > to_date:
            author = None
            continue;

          author = args[1]
          if author not in stats:
              stats[author] = 0
          if author not in commits:
              commits[author] = 0
          commits[author] += 1

      elif len(args) == 3:
          if author is None:
            continue;

          if args[2].startswith('vendor'):
              continue
          try:
              added = abs(int(args[0]))
              if False and added >= 10000:
                  print("WARNING: Ignoring large commit by %s in %s\n\t%s" % (author, repo, line), file=sys.stderr)
              else:
                stats[author] += added
          except ValueError:
              pass

print('Author\tCompany\tCommits\tLoC')
for author in sorted(stats):
    print('%s\t%s\t%s\t%s' % (author, get_company(author), commits[author], stats[author]))



