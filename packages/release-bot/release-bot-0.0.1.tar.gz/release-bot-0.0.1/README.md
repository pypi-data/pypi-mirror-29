Release bot
============
This is a bot that helps maintainers deliver their software to users. It is meant to watch github repositories for 
release pull requests. The PR must be named in this format `0.1.0 release`. No other format is supported yet. Once 
this PR is closed (and merged) bot will create a new github release. Changelog will be pulled from root of the 
repository and must be named `CHANGELOG.md`. Changelog for the new version must begin with version heading, i.e `# 0.1.0`
. Everything between this heading and the heading for previous version will be pulled into the changelog. 

Once a release is complete, bot will upload this release to PyPi. Note that you have to setup your login details (see [Requirements](#requirements)). This is subject 
to change, but right now bot will build sdist and then wheels for python2 and for python3 and upload them.

After PyPi release, bot will try to release on Fedora dist-git, on `master` branch and branches specified in configuration. 
This is only possible, if there won't be no merge conflicts, if they arise, you have to solve them first  before attempting the release again.
You can enable releases to Fedora by running with `--fedora` argument. 
A `release-conf.yaml` file is required. See [Configuration](#configuration) section for details.

# Configuration
Configuration is in a form of a yaml file. You can specify your config using `-c file.yaml` or `--configuration file.yaml`. If you do not specify it using an argument, bot will try to find `conf.yaml` in current working directory.
Here are the configuration options:

| Option        | Meaning       | Required      |
|------------- |-------------|-------------| 
| `repository_name`     | Name of your Github repository  | Yes |
| `repository_owner`    | Owner of the repository    	  | Yes |
| `github_token`		| [Github personal access token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)   | Yes |
| `refresh_interval`	| Time in seconds between checks on repository. Default is 180 | No |

Sample config can be found in this repository.

Best option for this is creating a github account for this bot so you can keep track of what changes were made by bot and what are your own.

If you want to release in Fedora, you also have to have a `release-conf.yaml` file in the root of your project repository. 
This file has to be updated with every release as it is a source of information for updating spec file.
Here are the possible options:

| Option        | Meaning       | Required      |
|---------------|---------------|---------------| 
| `version`     | Version number | Yes |
| `changelog`   | List of changelog entries. If empty, changelog defaults to `$version release` | No |
| `author_name`	| Author name for changelog. If not set, author of the merge commit is used	    | No |
| `author_email`| Author email for changelog. If not set, author of the merge commit is used	| No |
| `fedora_branches`     | List of branches that you want to release on. Master is always implied | No |  

Sample config can be found in this repository.

# Requirements
Releasing to PyPi requires to have `wheel` package both for python 2 and python 3, therefore please install `requirements.txt` with both versions of `pip`.
You also have to setup your PyPi login details in `$HOME/.pypirc` as described in [PyPi documentation](https://packaging.python.org/tutorials/distributing-packages/#create-an-account)
If you are releasing to Fedora, you will need to have an active kerberos ticket while the bot runs.
