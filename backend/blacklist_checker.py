from urllib.parse import urlparse



# NORMALIZE DOMAIN

def normalize_domain(url):


    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain



# LOAD BLACKLIST

def load_blacklist(file_path):

    domains = set()

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            for line in f:

                domain = line.strip().lower()

                if domain:
                    domains.add(domain)

        print(f"Loaded {len(domains)} blacklist domains")

    except Exception as e:

        print("Blacklist loading error:", e)

    return domains



# LOAD ONCE AT STARTUP

BLACKLIST_FILE = "blacklist.txt"

blacklist_domains = load_blacklist(BLACKLIST_FILE)


# BLACKLIST CHECK

def is_blacklisted(url):
  

    domain = normalize_domain(url)

    # Check domain and parent domains
    while domain:

        if domain in blacklist_domains:
            return True

        if "." not in domain:
            break

        domain = domain.split(".", 1)[1]

    return False



# TESTING

if __name__ == "__main__":

    test_urls = [

        "https://google.com",

        "https://login.google.com",

        "coinbasessupport.com",

        "https://secure.login.phishing-site.com"
    ]

    for url in test_urls:

        if is_blacklisted(url):
            print(f"[BLACKLISTED] {url}")

        else:
            print(f"[SAFE] {url}")