from __future__ import with_statement
from fabric.api import *
from fabric.api import run, env
import logging
import datetime
import sys, os
import ConfigParser
import re, glob, shutil



# Logging parameters
ANTI_VIRUS_NAME = "Sophos"
hostname = local("hostname", capture=True)
date =  datetime.datetime.now().date()
CFAES_LOG_FILENAME = "CFAES-Log-{0}-{1}".format(hostname, date)

# Default Log Level
DEFAULT_LOG_LEVEL = 'info'

# Other Log levels
LEVELS = {

    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# Create a Folder for Logs

log_folder =  "{0}-{1}".format(hostname,date )
if (os.path.isdir(log_folder)):
    shutil.rmtree(log_folder)
    os.mkdir(log_folder)
else:
    os.mkdir(log_folder)



# Start logging with given filename and level.
logging.basicConfig(filename = os.path.join(log_folder, CFAES_LOG_FILENAME), level=LEVELS[DEFAULT_LOG_LEVEL])




# Check Anti-Virus Status

def check_status():
    # Get the username who is running this script

    username = raw_input("Name of the person running this script: ")
    databackups = raw_input("Data on this machine is backed up? Yes/No ")

    if databackups:
        databackups == "No"
    # This section will check Anti-virus status and copy log files to ANTI-Virus-Logs.log
    logging.info('Start Anti-Virus On-access Scan Status Check Logging')
    on_access_status_reboot=local('sudo /opt/sophos-av/bin/savconfig query EnableOnStart', capture=True)

    if on_access_status_reboot:
        logging.info('On-access Scanning will be started automatically: {0}'.format(on_access_status_reboot))
    else:
        logging.info('On-access Scanning will be started automatically on next reboot: {0}'.format("Enabled"))
        sudo("/opt/sophos-av/bin/savconfig set EnableOnStart true")

    logging.info('Start Copying Anti-Virus Logs')
    local('sudo /opt/sophos-av/bin/savlog > {0}/ANTI-Virus-Logs.log'.format(log_folder))
    logging.info('Finished Copying Anti-Virus Logs')

    # Collect system logs
    logging.info('Start Copying System Log-files')
    local('sudo cp /var/log/syslog  {0}/'.format(log_folder))
    logging.info('Finished Copying System Log-files')

    # This section will apply updates and patches for the system.
    logging.info('Applying Patches and Updates')
    updates_applied = raw_input("Do you want to update the system now? Yes/No ")
    if (updates_applied == "Yes" or updates_applied == "Y" or updates_applied == "yes"):
        local('sudo apt-get upgrade')
        local('sudo apt-get update')
        logging.info('Applying Patches and Updates completed')
    else:
        logging.info('{0} did not apply patch at this time.'.format(username))

    # Bundle log files into one archive file

    local('tar -czvf {0} {1}'.format("{0}-{1}-Data_bk_{3}{2}".format(username,log_folder,".tar.gz", databackups), log_folder))

    # Remove log-folder

    shutil.rmtree(log_folder)

