#!/bin/bash

# Script to remove API key from Git history
# WARNING: This will rewrite Git history!

echo "⚠️  WARNING: This script will rewrite Git history!"
echo "This will remove the API key from all commits."
echo ""
echo "Before running this script:"
echo "1. Make sure you have a backup of your repository"
echo "2. If this is a shared repository, coordinate with your team"
echo "3. All collaborators will need to re-clone the repository"
echo ""
read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing API key from Git history..."
    
    # Remove the API key from all commits
    git filter-branch --force --index-filter \
        'git ls-files -z | xargs -0 sed -i "" "s/a1dff23520mshe54eca80fd7e266p171832jsn90f79381d0b9/YOUR_API_KEY_REMOVED/g"' \
        --prune-empty --tag-name-filter cat -- --all
    
    echo ""
    echo "✅ API key removed from Git history!"
    echo ""
    echo "Next steps:"
    echo "1. Force push to remote: git push --force --all"
    echo "2. Force push tags: git push --force --tags"
    echo "3. Notify collaborators to re-clone the repository"
    echo "4. Consider regenerating your API key for security"
else
    echo "Operation cancelled."
fi 