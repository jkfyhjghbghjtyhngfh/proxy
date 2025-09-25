#!/bin/bash
# Script to mirror a site and serve it locally

echo "Enter the website URL (example: https://example.com/):"
read site_url

# Folder name based on URL
folder_name=$(echo "$site_url" | sed 's/[^a-zA-Z0-9]/_/g')

echo "📥 Downloading full site from $site_url ..."
wget \
    --mirror \
    --convert-links \
    --adjust-extension \
    --page-requisites \
    --no-parent \
    -P "$folder_name" \
    "$site_url"

if [ $? -ne 0 ]; then
    echo "❌ Download failed!"
    exit 1
fi

echo "✅ Done! Site saved in folder: $folder_name"

# Start local server
echo "🚀 Serving $folder_name at http://localhost:6767"
cd "$folder_name/$site_url" 2>/dev/null || cd "$folder_name"
python3 -m http.server 6767
