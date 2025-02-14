#!/bin/bash

# Documentation:
#
# This script manages VirtualBox virtual machines using the VBoxManage utility.
# It supports starting, stopping, pausing, checking the status of running VMs,
# listing all available VMs, and setting a target VM as the current one. 
# The ID of the current VM is stored in a configuration file located at ~/.config/virtualbox_manager/target.

# Define the path to the target configuration file
TARGET_FILE=~/.config/virtualbox_manager/target

# Ensure the directory for the target file exists
mkdir -p "$(dirname "$TARGET_FILE")"

# Function to display usage information
usage() {
    printf "Usage: $0 [command]\n\n"
    printf "start\t\t: Start the target virtual machine in headless mode.\n"
    printf "stop\t\t: Stop the currently selected virtual machine.\n"
    printf "pause\t\t: Pause the currently selected virtual machine.\n"
    printf "resume\t\t: Resume the currently selected paused virtual machine.\n"
    printf "status\t\t: Show the status of all running virtual machines.\n"
    printf "list\t\t: List all available virtual machines.\n"
    printf "target\t\t: Print the currently selected target virtual machine.\n"
    printf "set-target <name>\t: Set the target virtual machine by its name.\n"
    printf "exists <name>\t: Check if a virtual machine with the given name exists.\n"
    exit 1
}

# Function to check if a VM with the given name exists
vm_exists() {
    local vm_name="$1"
    VBoxManage list vms | grep -q "\"$vm_name\""
    if [ $? -eq 0 ]; then
        echo "Virtual machine '$vm_name' exists."
        return 0
    else
        echo "Virtual machine '$vm_name' does not exist."
        return 1
    fi
}

# Function to set the target VM and store its UUID in the configuration file
set_target() {
    local vm_name="$1"
    if vm_exists "$vm_name"; then
        local vm_uuid=$(VBoxManage showvminfo "$vm_name" --machinereadable | grep '^UUID' | cut -d '=' -f 2 | tr -d '"')
        echo "$vm_uuid $vm_name" > "$TARGET_FILE"
        echo "Target virtual machine set to: $vm_uuid $vm_name"
    else
        echo "Error: Virtual machine '$vm_name' does not exist."
        exit 1
    fi
}

# Function to check if a target VM is set
is_target_set() {
    if [ ! -f "$TARGET_FILE" ] || [ ! -s "$TARGET_FILE" ]; then
        echo "Error: No target virtual machine is set. Use 'set-target <name>' to specify one."
        exit 1
    fi
}

# Function to get the current target VM from the configuration file
get_target() {
    is_target_set
    cat "$TARGET_FILE"
}

# Function to start the target VM in headless mode
start_vm() {
    is_target_set
    local vm_id=$(get_target | awk '{print $1}')
    VBoxManage startvm "$vm_id" --type headless
}

# Function to stop the target VM
stop_vm() {
    is_target_set
    local vm_id=$(get_target | awk '{print $1}')
    VBoxManage controlvm "$vm_id" poweroff
}

# Function to pause the target VM
pause_vm() {
    is_target_set
    local vm_id=$(get_target | awk '{print $1}')
    VBoxManage controlvm "$vm_id" pause
}

# Function to resume the paused target VM
resume_vm() {
    is_target_set
    local vm_id=$(get_target | awk '{print $1}')
    VBoxManage controlvm "$vm_id" resume
}

# Function to list all available virtual machines
list_vms() {
    VBoxManage list vms
}

# Function to list running VMs
list_running_vms() {
    VBoxManage list runningvms
}

# Main script logic
if [ "$0" = "$BASH_SOURCE" ]; then
    if [ $# -lt 1 ]; then
        usage
    fi

    Command=$1
    shift

    case $Command in
        start)
            start_vm
            ;;
        stop)
            stop_vm
            ;;
        pause)
            pause_vm
            ;;
        resume)
            resume_vm
            ;;
        status)
            list_running_vms
            ;;
        list)
            list_vms
            ;;
        target)
            if [ -f "$TARGET_FILE" ] && [ -s "$TARGET_FILE" ]; then
                get_target
            else
                echo "No target virtual machine is set."
            fi
            ;;
        set-target)
            if [ $# -lt 1 ]; then
                echo "Error: Missing virtual machine name."
                usage
            fi
            set_target "$1"
            ;;
        exists)
            if [ $# -lt 1 ]; then
                echo "Error: Missing virtual machine name."
                usage
            fi
            vm_exists "$1"
            ;;
        *)
            echo "Unrecognized command: $Command"
            usage
            ;;
    esac
else
    echo "This script cannot be sourced."
    exit 1
fi
