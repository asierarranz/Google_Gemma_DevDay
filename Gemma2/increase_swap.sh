#!/bin/bash

SWAPFILE="/var/swapfile"
SWAPSIZE_GB=32
SWAPSIZE_SPEC="32G"

if [[ $EUID -ne 0 ]]; then
   echo "Error: Must run as root (use sudo)." >&2
   exit 1
fi

echo "--- Setting up ${SWAPSIZE_SPEC} swap on Jetson Orin Nano (JP6) ---"
echo "WARNING: Needs >${SWAPSIZE_GB}GB free space. Swap on SD card is slow."

FREE_GB=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
if [[ ! "$FREE_GB" =~ ^[0-9]+$ || "$FREE_GB" -lt $(($SWAPSIZE_GB + 1)) ]]; then
    echo "Error: Insufficient disk space. Found ${FREE_GB}GB, need >${SWAPSIZE_GB}GB." >&2
    exit 1
fi

swapoff -a
if systemctl list-units --full -all | grep -q 'nvzramconfig.service'; then
    echo "Disabling nvzramconfig service..."
    systemctl stop nvzramconfig.service >/dev/null 2>&1
    systemctl disable nvzramconfig.service >/dev/null 2>&1
fi

cp /etc/fstab /etc/fstab.bak.$(date +%F_%T)
sed -i.bak "\#${SWAPFILE//\//\\/}#d" /etc/fstab
sed -i.bak "/\/dev\/zram/d" /etc/fstab

if [ -f "$SWAPFILE" ]; then
    echo "Removing existing $SWAPFILE..."
    rm -f "$SWAPFILE" || { echo "Error: Failed to remove $SWAPFILE" >&2; exit 1; }
fi

echo "Creating ${SWAPSIZE_SPEC} swap file at $SWAPFILE (can take time)..."
if ! fallocate -l "$SWAPSIZE_SPEC" "$SWAPFILE" 2>/dev/null; then
    echo "fallocate failed or not found, using dd..."
    dd if=/dev/zero of="$SWAPFILE" bs=1M count=$(($SWAPSIZE_GB * 1024)) status=progress || \
        { echo "Error: dd failed" >&2; rm -f "$SWAPFILE"; exit 1; }
fi

chmod 600 "$SWAPFILE" || { echo "Error: chmod failed" >&2; rm -f "$SWAPFILE"; exit 1; }
mkswap "$SWAPFILE" || { echo "Error: mkswap failed" >&2; rm -f "$SWAPFILE"; exit 1; }
swapon "$SWAPFILE" || { echo "Error: swapon failed" >&2; rm -f "$SWAPFILE"; exit 1; }

if ! grep -q "^${SWAPFILE}.*swap" /etc/fstab; then
    echo "$SWAPFILE none swap sw 0 0" >> /etc/fstab || \
        echo "Warning: Failed to add to /etc/fstab" >&2
fi

echo "--- Swap Setup Complete ---"
swapon --show
echo "---------------------------"
free -h
echo "---------------------------"

exit 0
