url=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | python3 -c "import sys, json; print(next(item['browser_download_url'] for item in json.load(sys.stdin)['assets'] if 'linux64' in item.get('browser_download_url', '')))")
echo "Downloading $url..."
curl -s -L "$url" | tar -xz
chmod a+x ./geckodriver
