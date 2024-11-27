#!/bin/bash

# backup_data.sh
# Script to back up important data

echo "Backing up important data..."

# Define the source and destination directories (replace with actual paths)
SOURCE_DIR="/path/to/your/data"
BACKUP_DIR="/path/to/your/backup"

# Create a timestamp for the backup
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="backup_$TIMESTAMP.tar.gz"

# Create a compressed backup of the data
tar -czf $BACKUP_DIR/$BACKUP_FILE -C $SOURCE_DIR .

echo "Backup completed! Backup file: $BACKUP_DIR/$BACKUP_FILE"
