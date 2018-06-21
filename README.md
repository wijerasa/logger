# logger

## What this does:

This script collects system logs saved in `/var/log/syslog` and Anti-Virus logs from **Sophos**

## Install Dependencies 

```bash
pip install fabric
```

## How to run the logger:


### Scripts

1. **fabfile.py** - Script that runs the logger

### Inputs

Script will ask the following set of questions before it collects the information.

2. **Name of the person runing this script:** - provide your name
3. **Data on this machine is backed up? Yes\/No** - Mention whether you have backed up the data or not (**Answer: Yes/No**)
4. **Do you want to update system now? Yes/No** - You have the choice to run updates and patches now. If you want to continue type **"Yes"**, otherwise. type **"No"**

### Outputs

5. Script will creat a compressed-archived file like this: `samwilly-fakecompany-2018-06-12-Data_bk_Yes.tar.gz`

- *samwilly* - Name of the person who ran the script
- *fakecompany* - Machine name
- *2018-06-12* - Date of this file created
- *Data_bk_Yes* - Data is backed up or not. **Yes:** indicates data has been backed up and **No:** indicates data has not been backed up

### Step 1:

Clone `git` repository to your local machine

```bash
git clone https://github.com/wijerasa/logger.git
cd logger

```

### Step 2:

Run the following code,

```bash
fab check_status

```

This will collect system-logs and Anti-Virus logs and archive them to one file.
### Step 3:

Upload the final compressed-archived file (`samwilly-fakecompany-2018-06-12-Data_bk_Yes.tar.gz`) to your Box folder
