#!/bin/bash
cd "$(dirname "$0")"
echo -e "❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️\n"
echo "JPG and RAW Photo Sync Tool 📷"
echo "👩🏻‍💻 by Danni Z. ✨ 👩🏻‍💻"
echo -e "❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️\n"

python3 sync_folders.py

echo -e "\nPress Enter to exit..."
read -n 1 -s
osascript -e 'tell application "Terminal" to close first window' & exit
