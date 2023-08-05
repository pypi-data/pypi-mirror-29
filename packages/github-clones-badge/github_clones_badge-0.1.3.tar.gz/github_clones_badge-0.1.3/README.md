![alt text](http://apmechev.com/img/git_repos/github_clones_badge_clones.svg "github clones")
[![PyPI version](https://badge.fury.io/py/github-clones-badge.svg)](https://badge.fury.io/py/github-clones-badge)
[![Build Status](https://travis-ci.org/apmechev/github_clones_badge.svg?branch=master)](https://travis-ci.org/apmechev/github_clones_badge)

# github_clones_badge

Script to auto-create a badge of number of clones for your github repositories. Since GitHub's API only tracks the past 2 weeks of traffic, this tool saves all clone statistics into a dictionary and sums total number of clones starting 14 days before first run. 

# Installing:

```bash

pip install github_clones_badge
```

# Running for one repo (That you own), once:

```python
>>> from github_clones_badge import get_github_clones as ghc
>>> help(ghc)

>>> bc=ghc.badge_creator(repo='GRID_LRT')
7 Number of new entries
>>> bc.download_badge('/var/www/example.com/public_html/where_you_store_your_badges/') 
# These have to be stored on your server of course

```

# Running for a repo that you are a collaborator of but don't own, once

In this case, the repouser's name is appended to the beginning of the badge name. This means one reponame for multiple users can be 'tracked'. 
```python
>>> from github_clones_badge import get_github_clones as ghc
>>> help(ghc)

>>> bc=ghc.badge_creator(repo='DDFacet', repouser='cyriltasse')
7 Number of new entries
>>> bc.download_badge('/var/www/example.com/public_html/where_you_store_your_badges/')
# These have to be stored on your server of course

```


