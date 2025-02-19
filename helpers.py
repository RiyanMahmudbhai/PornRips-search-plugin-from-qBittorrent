import requests

def retrieve_url(url):
    """
    Retrieve the content of a given URL and return it as text.
    Handles errors gracefully.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error retrieving URL {url}: {e}")
        return None
