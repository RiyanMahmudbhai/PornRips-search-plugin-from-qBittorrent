import re
from helpers import retrieve_url
from novaprinter import prettyPrinter

class pornrips:
    url = 'https://pornrips.to/'
    name = 'PornRips'
    supported_categories = {'all': '0'}

    @staticmethod
    def search(query):
        """
        Search torrents on PornRips.
        Returns a list of dictionaries containing torrent details.
        """
        search_url = f"https://pornrips.to/search/{query.replace(' ', '%20')}"
        html = retrieve_url(search_url)
        
        if not html:
            return []

        results = []
        pattern = re.findall(r'<a href="(/torrent/\d+-[^"]+)"[^>]*>([^<]+)</a>', html)

        for link, title in pattern:
            torrent = {
                'name': title,
                'link': f"https://pornrips.to{link}",
                'size': 'Unknown',
                'seeds': 'Unknown',
                'leech': 'Unknown',
                'engine_url': 'https://pornrips.to/'
            }
            results.append(torrent)
            prettyPrinter(torrent)
        
        return results
