import csv
from urllib.parse import urlparse


def load_whitelist(csv_path):
  

    domains = set()

    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:

                if len(row) < 2:
                    continue

                domain = row[1].strip().lower()

                if domain:
                    domains.add(domain)

        print(f"Loaded {len(domains)} trusted domains")

    except Exception as e:
        print("Whitelist loading error:", e)

    return domains



# Load whitelist once when Flask server starts

WHITELIST_PATH = "tranco.csv"

trusted_domains = load_whitelist(WHITELIST_PATH)



# Domain Extraction

def extract_domain(url):

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain



# Whitelist Check

def is_whitelisted(url):

    domain = extract_domain(url)

    # Exact match
    if domain in trusted_domains:
        return True

    # Subdomain match
    for trusted in trusted_domains:

        if domain.endswith("." + trusted):
            return True

    return False



# Testing

if __name__ == "__main__":

    test_urls = [
        "https://google.com",
        "https://mail.google.com",
        "https://github.com",
        "https://docs.github.com",
        "https://fake-google-login.com",
        "https://unknown-domain-xyz.com"
    ]

    for url in test_urls:

        if is_whitelisted(url):
            print(url, "-> TRUSTED")
        else:
            print(url, "-> NOT TRUSTED")