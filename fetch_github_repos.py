#!/usr/bin/python3

import os, sys
import subprocess
import requests

root_dir = os.getcwd()

GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN', '')
GITHUB_ORG_URL = 'https://api.github.com/orgs/%(org)s/repos?page=%(page)s'

repos_dir = "./repos"
if '--dir' in sys.argv:
    repos_dir = sys.argv[sys.argv.index('--dir')+1]
    if not repos_dir.startswith("/"):
        repos_dir = os.path.join(os.getcwd(), repos_dir)
    del sys.argv[sys.argv.index('--dir')+1]
    del sys.argv[sys.argv.index('--dir')]

try:
    os.stat(repos_dir)
except FileNotFoundError:
    os.makedirs(repos_dir)

fetch_branch = "master"
if '--branch' in sys.argv:
    fetch_branch = sys.argv[sys.argv.index('--branch')+1]
    del sys.argv[sys.argv.index('--branch')+1]
    del sys.argv[sys.argv.index('--branch')]

fetch_org = sys.argv[1]

repos_page = 1
while(repos_page):
    repos_url = GITHUB_ORG_URL % {"org": fetch_org, "page": repos_page}
    #print(repos_url)
    repos_resp = requests.get(repos_url)

    if repos_resp.status_code == 200:
        repos = repos_resp.json()
        if len(repos) < 1:
            break;

        for repo in repos:
            repo_path = os.path.join(root_dir, repos_dir, repo['name'])
            try:
                os.stat(repo_path)
                print("Updating: %s" % repo['name'])
                os.chdir(repo_path)
                proc = subprocess.run(["git", "checkout", fetch_branch])
                proc = subprocess.run(["git", "fetch", "--all"])
                proc = subprocess.run(["git", "pull"])
            except FileNotFoundError:
                print("Cloning %(name)s from %(clone_url)s" % repo)
                proc = subprocess.run(["git", "clone", "--branch", fetch_branch, repo["clone_url"], repo_path])
        repos_page += 1
    else:
        break
