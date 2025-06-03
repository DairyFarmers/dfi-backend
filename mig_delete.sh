#!/bin/bash
# filepath: delete_migrations.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting migration files cleanup...${NC}"

# Find all migrations directories
find . -type d -name "migrations" | while read -r dir; do
    echo -e "${GREEN}Processing directory: $dir${NC}"
    
    # Delete all numbered migration files but keep __init__.py
    find "$dir" -type f -name "[0-9]*.py" -exec rm -f {} \;
    
    # Verify __init__.py exists, create if it doesn't
    if [ ! -f "$dir/__init__.py" ]; then
        touch "$dir/__init__.py"
        echo -e "${GREEN}Created __init__.py in $dir${NC}"
    fi
done

echo -e "${GREEN}Migration files cleanup completed!${NC}"
