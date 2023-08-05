# Jira Tracker

This Python script allows you to automatically track your time in Jira based on your
Git checkout history.

The script supports working with several projects at a time.

It does not spy on you, it just counts how many branches you've checked out today,
and tracks them by evenly dividing the amount of branches you was working on.

## Usage
1. Clone the distribution
```bash
git clone https://github.com/dor-denis/JiraTracker
```
2. Install git checkout hook which will store your checkout log to .git/logs/checkout_history
```bash
cd JiraTracker
pip install -r requirements.txt
python install.py PATH_TO_YOUR_REPOSITORY
cp settings.example.yml settings.yml
```
3. Set up your Jira connection (`settings.yml` file)
```YAML
hours: 6
projects:
  - jira_name: YOUR_PROJECT_JIRA_CODE
    path: ABSOLUTE_PATH_TO_YOUR_REPO
    jira_url: https://domain.jira.com
    username: YOUR_JIRA_USERNAME
    password: YOUR_JIRA_PASSWORD
```
* *hours* setting is overall amount of working hours in your company
* each *projects* array entry is a project you need to keep track of
4. To track your branches for today, call `python JiraTracker/JiraTracker.py settings.yml`
5. (optional) Add this script to your Cron so it will run every work day at 17:30, so you won't need to run it manually:
```cron
30 17 * * 1-5 /bin/python {path_to_repo}/tracker.py {path_to_settings.yml}
```

------
If you want to track your time for some day in the past, supply this date as a second agrgument to JiraTracker.py, for example:
```bash
cd {JiraTracker folder}
python track.py settings.yml 2018-02-17
