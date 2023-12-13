#!/bin/bash

select_applications() {
    mysql -s -N -e "SELECT id FROM wordpress.wp_recruitment WHERE seen=0 AND date <= '2023-07-01';"
    exit 0
}

update_applications() {
    echo "[*] Updating $1"
    mysql -e "UPDATE wordpress.wp_recruitment SET seen=1 WHERE id=$1"
    exit 0
}

while getopts "su:" opt; do
	case "$opt" in

    s) select_applications
    ;;

    u) update_applications $OPTARG
    ;;

	esac
done
