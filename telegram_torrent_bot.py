import os
import requests
import importlib.util
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up your bot token
TOKEN = "7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y"

# Load the PornRips search plugin
PLUGIN_URL = "https://raw.githubusercontent.com/Larsluph/qbittorrent-search-plugins/prt/nova3/engines/pornrips.py"
PLUGIN_PATH = "pornrips.py"

# Download the plugin if not already present
if not os.path.exists(PLUGIN_PATH):
    response = requests.get(PLUGIN_URL)
    with open(PLUGIN_PATH, "w", encoding="utf-8") as f:
        f.write(response.text)

# Load the plugin as a module
spec = importlib.util.spec_from_file_location("pornrips", PLUGIN_PATH)
pornrips = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pornrips)

def search_torrent(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        update.message.reply_text("Please provide a search term! Example: /search Ubuntu")
        return
    
    # Call the search function from the plugin
    results = pornrips.search(query)
    
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
