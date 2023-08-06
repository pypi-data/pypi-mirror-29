# What is this?

A tool to create cross-linked PRs.

# How do I install it?

`pip install git+https://github.com/bwarren2/create-prs`

Note: you will need a version of git that supports the -C flag.  Casual googling says this is git version >= 1.8, but check yourself with `man git`.

Set some env vars:

    `JIRA_PASSWD`: Jira password, ex 'sooperseekritpass'
    `JIRA_USER`: Jira username, ex 'warrenb'
    `GITHUB_TOKEN`: A github API token (from your settings).  ex 'nicetry'.
    `PROJECTS`: Where you have your eab repos checked out.  ex 'PROJECTS=/Users/warrenb/Projects'

If you need to make a github token, try [the github page](https://github.com/settings/tokens/).  You want `repo` privileges.  YES, I do in fact mean it.  (It's the privilege level that lets you interact with private PRs.)  For a tale of the woe that befalls you if you don't do this, ask @eabmahoney.

# How do I use it?

`create-prs -h` for help.  By default, we only change local settings.

## Example usage:

### Basic

`create-prs --branch some-name --ticket NAV-5000`

Which translates to:
 * Create branches in each of the projects
 * Name the branch `feature/NAV-5000-some-name`

### Basic, short names

`create-prs -b some-name -t NAV-5000`

Same as above, just using shorter flags.

### Picking bases

`create-prs -pb -b some-name -t NAV-5000`

Which translates to:
 * Pick the base branches with an autocompleter
 * Create branches in each of the projects
 * Name the branch `feature/NAV-5000-some-name`

This will start an autocompleter that looks through your local branches to use one as a base.  Useful for bugfixes that need to base off of release branches.

### Change all reqs

`create-prs --all-reqs -b some-name -t NAV-5000`

Which translates to:
 * Change ALL the reqs files, not just local
 * Create branches in each of the projects
 * Name the branch `feature/NAV-5000-some-name`

# Contributing

PRs welcome.

