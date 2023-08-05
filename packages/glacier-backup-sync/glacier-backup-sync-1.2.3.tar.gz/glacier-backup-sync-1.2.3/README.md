# python-glacier-sync
A python-script that allows you to automatically manage and synchronize your local backups.

**Usage: glacier_sync [OPTIONS] FOLDER VAULT_NAME**

**Options:**

    --mode TEXT         Set the sync-mode for glacier, can be 'daily' or 'weekly' (default)
    --account_id TEXT   Set the id of your AWS account
    --skip / --no-skip  Only simulate the sync run, skip the actual cleanup and sync.
    --pattern TEXT      The file pattern to search for
    --week-cycle NUMBER Defines after how many weeks the weekly backups are being removed (default = infinite retention).
    --help              Show this message and exit.

Make sure you configure AWS CLI before running this tool (`pip install awscli` and `aws configure`)
to make sure the script can successfully connect to your AWS account.

# TODO
* actually implement 'mode' flag (currently locked on weekly)
* implement e-mail option to receive the sync-log by e-mail