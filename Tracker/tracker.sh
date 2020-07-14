#!/bin/bash

# This is a simple tracker that requests the name of the currently active window every few seconds and
# stores it into a log file for later analysis.

CURR_DATE=$(date +'%Y-%m-%d')
ARCHIVE_FOLDER="/home/kiko/Projects/Productivity-Tracker/archive/"
TODAY_FILE=${ARCHIVE_FOLDER}${CURR_DATE}'.csv'

function curr_time()
{
  echo ` date +'%s'`
}

function get_curr_win()
{
    # Gets id of the currently active window
    win_id=`xprop -root _NET_ACTIVE_WINDOW | awk '{ print $5 }'`

    # Gets the name of a window with <win_id> id
    win_name=`xprop -id $win_id _NET_WM_NAME WM_CLASS | awk -F'"' ' {print $2 } ' | tr '\n' ';' | sed ' s/.$//'`

    echo $win_name

}

# frequency of requesting window name
EVERY_S=2

echo "Recording activity..."

PREV_WINDOW=""

while [ 1 ]
do

    CURR_WINDOW=$(get_curr_win)

    if [[ ("$PREV_WINDOW" != "$CURR_WINDOW"  ||  '10#'`date +'%S'` -lt  $EVERY_S)  &&  -n "$CURR_WINDOW" ]]
        then
        TIME=$(curr_time)

        #stores a log in format "time;Curr_window_name;curr_program"
        echo "$TIME;$CURR_WINDOW" >> $TODAY_FILE
        PREV_WINDOW=$CURR_WINDOW

    fi

    sleep $EVERY_S
done
