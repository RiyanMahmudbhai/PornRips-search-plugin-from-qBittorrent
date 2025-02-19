def prettyPrinter(data):
    """
    Simulate qBittorrent's prettyPrinter function.
    Expected dictionary keys:
    - link: The torrent link (magnet or direct)
    - name: Torrent name
    - size: File size
    - seeds: Number of seeds
    - leech: Number of leeches
    - engine_url: Source URL
    """
    print(f"Name: {data['name']}")
    print(f"Link: {data['link']}")
    print(f"Size: {data['size']}")
    print(f"Seeds: {data['seeds']}")
    print(f"Leeches: {data['leech']}")
    print(f"Engine URL: {data['engine_url']}")
    print("-")
