The scripts in this project are used to pull project metrics from the [LF Edge](https://lfedge.org) projects.

## Fetch repos

Scripts that generate Git statistics use a local checkout of git repos. Before you run those scripts, you will need to fetch the latest contents from the remote repositories. This can be done manually on a per-repo basis, but if using Github or Gerrit the following can be used to pull & update them all at once.

### Github

For Github, run:

```
./fetch_github_repos.py <github_organization> --dir <repos_dir>
```

This will create a local folder at <repos_dir> with a checkout of all the organization's repositories from Github. If `--dir` is not specified, this will default to `./repos/`

**Example:**
```
./fetch_github_repos.py edgexfoundry --dir ./edgex_repos/
```

### Gerrit

For Gerrit, run:

```
./fetch_gerrit_repos.sh <gerrit_host_url>
```

This will create a local folder at `./repos/` with a checkout of all the project's repositories from Gerrit. If a repo is in a folder on Gerrit, the folder name will be appended to the repo name in this directory, so `my/projects/foo` will become `my_projects_foo`.

**Example:**
```
./fetch_gerrit_repos.sh https://gerrit.akraino.org/
```


## Commit History

To generate a monthly summary from your git repositories, you can use the `commit_histogram.py` script.

```
./commit_histogram.py <list_of_local_repos>
```

The output will be a tab-separated table showing each month's number of committers, number of authors and number of lines of code changed, as well as the cumulative totals of those three metrics.

**Example:**
```
./commit_histogram.py ./repos/*
```

If you want the metrics summarizes by quarter, rather than by month, pass the `--quarterly` flag to the script.

**Example:**
```
./commit_histogram.py --quarterly ./repos/*
```

## Contributor Metrics

To generate a list of contributors and metrics about their contributions, use the `contributor_stats.py` script.

```
./contributor_stats.py <list_of_local_repos>
```

The output will be a tab-separated table showing each unique commit author's email address, the company associated with that address, and the total number of commits and lines of code attributed to them. 

The company association is determined by two maps defined at the top of the script, `DOMAIN_MAP` which maps an email address' domain name to a company name, and `COMPANY_MAP` which maps a full email address to a company name. Use the first for company email addresses, and the second for personal or system-generated addresses that might have the same domain between contributors from different companies. You will need to update these maps in the script as new authors are found.

You can also limit the date range for these metrics by specifying a `--from` and `--to` date parameter in YYYY-MM-DD format.

**Example:**
```
./contributor_stats.py --from 2019-01-01 --to 2019-12-31 ./repos/*
```


## Release Statistics

> This script will only work with projects hosted on Github

You can generate detailed metrics from a release using the `release_metrics.py` script:

```
./release_metrics.py --from <YYYY-MM> --to <YYYY-MM> <list_of_local_repos>
```

Where the first YYYY-MM is the beginning month of the release cycle, and the second YYYY-MM is the ending month.

The output of this script will contain a list and count of the repos that had activity during the specified date range, the number of Github issues opened and closed, the number of commits, the number of lines of code changed, the number and list of commit authors, and the number of Github Pull Requests opened and closed.

> Because this script makes many API calls to Github, you will want to [get an access token from Github](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) and set it to the environment variable `GITHUB_ACCESS_TOKEN`

**Example:**
```
./release_metrics.py --from 2019-05 --to 2019-10 ./repos/*
```

You can additionally get release metrics for Github Pull Request reviews and reviewers by passing in the `--reviews` flag. This requires significantly more Github API calls, making the script run slower and requiring you to set the `GITHUB_ACCESS_TOKEN` environment variable to succeed.

## Dockerhub stats

Dockerhub provides a limited amount of download metrics for container images, you can get them using the `dockerhub-downloads.py` script.

```
./dockerhub-downloads.py <dockerhub_organization>
```

The output of this script is a tab-separated table containing the name of each Docker image published under the specified organization, and the total number of downloads it has received since being published.

**Example:**
```
./dockerhub-downloads.py edgexfoundry
```
