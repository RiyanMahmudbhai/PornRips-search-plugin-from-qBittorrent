import os
import sys
import importlib.util
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Set up your bot token
TOKEN = "7933218460:AAFbOiu04bmACRQh43eh7VfazGesw01T0-Y"

# Plugin paths
PLUGIN_PATH = "pornrips.py"
HELPERS_PATH = "helpers.py"

# Ensure required files are available
def download_file(url, path):
    if not os.path.exists(path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            print(f"Failed to download {url}")

# Load the helpers module
spec_helpers = importlib.util.spec_from_file_location("helpers", HELPERS_PATH)
helpers = importlib.util.module_from_spec(spec_helpers)
spec_helpers.loader.exec_module(helpers)

# Load the PornRips plugin
spec_plugin = importlib.util.spec_from_file_location("pornrips", PLUGIN_PATH)
pornrips = importlib.util.module_from_spec(spec_plugin)
sys.modules["pornrips"] = pornrips
spec_plugin.loader.exec_module(pornrips)

async def search_torrent(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a search term! Example: /search Ubuntu")
        return
    
    try:
        results = pornrips.search(query)
    except Exception as e:
        await update.message.reply_text(f"Error fetching torrents: {str(e)}")
        return
    
    if not results:
        await update.message.reply_text("No torrents found")
        return
    
    response = "\n".join([f"{r['name']} - {r['link']}" for r in results[:5]])
    await update.message.reply_text(response)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("search", search_torrent))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
