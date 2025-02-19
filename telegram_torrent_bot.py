import os
import sys
import requests
import importlib.util
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up your bot token (Replace with your actual token)
TOKEN = "7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y"

# Plugin paths
PLUGIN_URL = "https://raw.githubusercontent.com/Larsluph/qbittorrent-search-plugins/prt/nova3/engines/pornrips.py"
PLUGIN_PATH = "pornrips.py"
HELPERS_URL = "https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/searchengine/nova3/engines/helpers.py"
HELPERS_PATH = "helpers.py"

# Ensure required files are downloaded
def download_file(url, path):
    if not os.path.exists(path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            print(f"Failed to download {url}")

download_file(PLUGIN_URL, PLUGIN_PATH)
download_file(HELPERS_URL, HELPERS_PATH)

# Adjust Python path for local module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load the helpers module
spec_helpers = importlib.util.spec_from_file_location("helpers", HELPERS_PATH)
helpers = importlib.util.module_from_spec(spec_helpers)
spec_helpers.loader.exec_module(helpers)

# Load the PornRips plugin
import importlib.util
import sys

PLUGIN_PATH = "/root/PornRips-search-plugin-from-qBittorrent/pornrips.py"

spec_plugin = importlib.util.spec_from_file_location("pornrips", PLUGIN_PATH)
pornrips = importlib.util.module_from_spec(spec_plugin)
sys.modules["pornrips"] = pornrips  # Register in sys.modules
spec_plugin.loader.exec_module(pornrips)


def search_torrent(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        update.message.reply_text("Please provide a search term! Example: /search Ubuntu")
        return
    
    # Call the search function from the plugin
    try:
        results = pornrips.search(query)
    except Exception as e:
        update.message.reply_text(f"Error fetching torrents: {str(e)}")
        return
    
    if not results:
        update.message.reply_text("No torrents found")
        return
    
    response = "\n".join([f"{r['title']} - {r['link']}" for r in results[:5]])  # Send top 5 results
    update.message.reply_text(response)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("search", search_torrent))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
