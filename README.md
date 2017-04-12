# autoupdater

Used on Windows XP

Use python 3.4 and cx_Freeze to conver to exe compatible with Windows XP

#setings.upd 
All the settings are here:
- path from/to update files
- path for self update
- extentions for files, whish one wants to include into updates

#execute.py 
Used to run the app and selfupdate.

Starts self update. If all operations while trying to update own modules were finished 
with no critical errors, then it runs the files updater.

#files_updater.py 
All update logics is here.

First it reads settings.upd file and sets variables:
- dirpath_to_update - path where files one wants to be up to date are located
- dirpath_from_update - path where new files are stored
- update_ext - file extentions list which to update

Then program gathers all files with equal extentions from this two paths and compares them by date and presence:
- if file in update path is newer than file in end directory - it will be updated
- if there is no such file in end directory - it will be added
When files to copy list is builded app tries to copy this files in a row.
If file is busy the choise will be proposed:
Kill process and update file now OR do it later.

If user decided to update file now - process will be killed and file will be updated. 
Then app displays a message, that %program_name% was updated and now you can resume using this program.

#program_lisr.py
Dictionary with filenames and program names relations as key - value respectively. 


#self_update.py
Updates modules of program.

Reads settings.upd file for path and extentions to update.
Checks for updates for itself in the path. Updates modules and returns True if updates finished sucessfully 
or there is nothing to update or False if was error occured while trying to update.

#log_to_file.py 
Used for loging.

Gets string for log name, string for message to pass to the log file.
Appends message to the log dile if it exists or creates new and then appends the message.
