#!/bin/bash

usage()
{
    printf "Usage: $0 [command]\n\n"
    printf "start\n\t\t: start target virtual machine in headless mode\n"
    printf "status\n\t\t: show status of running virtual machines\n"
    printf "target\n\t\t: print TARGET virtual machine\n"
    exit 1
}

TARGET_ID='fc377297-5112-4455-ba43-d367e65f4e49'
TARGET_NAME='ubuntu18'
TARGET="$TARGET_ID $TARGET_NAME"

[ "$0" = "$BASH_SOURCE" ] || { echo "Couldn't be sourced!"; exit 1; }
[ $# -lt 1 ] && usage

Command=$1
case $Command in
    start)
        VBoxManage startvm $TARGET_ID --type headless
        ;;
    status)
        VBoxManage list runningvms
        ;;
    target)
        echo $TARGET
        ;;
    *)
        echo "Unrecognized command: $Command"
        ;;
esac