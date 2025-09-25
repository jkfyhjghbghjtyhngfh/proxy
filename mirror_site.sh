#!/bin/bash
# Mirror a site fully and serve it offline

echo "Enter the website URL (example: https://example.com/):"
read site_url

# Folder based on URL
folder_name=$(echo "$site_url" | sed 's/[^a-zA-Z0-9]/_/g')

echo "📥 Downloading full copy of $site_url ..."
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
    rm -rf "$folder_name"
    exit 1
fi

echo "✅ Download complete!"
echo "🚀 Serving $folder_name at http://localhost:8000"
cd "$folder_name" || exit
python3 -m http.server 8000
