import math
import re
from urllib.parse import urlparse
import tldextract


# ENTROPY CALCULATION

def calculate_entropy(text):
    if not text:
        return 0.0

    probabilities = [text.count(c) / len(text) for c in set(text)]

    return -sum(p * math.log2(p) for p in probabilities)



# FEATURE EXTRACTION

def extract_features(url):
    """
    Extracts the 20 features required by the phishing model.

    Returns:
        dict containing all features
    """

    parsed = urlparse(url)

    domain_info = tldextract.extract(url)

    domain = domain_info.domain
    subdomain = domain_info.subdomain

    full_domain = parsed.netloc

    # Basic lengths
  
    url_length = len(url)

    domain_length = len(domain)

    path_length = len(parsed.path)

  
    # Subdomain statistics
   
    subdomains = (
        subdomain.split(".")
        if subdomain
        else []
    )

    number_of_subdomains = len(subdomains)

    if number_of_subdomains > 0:
        average_subdomain_length = (
            sum(len(s) for s in subdomains)
            / number_of_subdomains
        )
    else:
        average_subdomain_length = 0

    
    # Entropy
    
    entropy_of_url = calculate_entropy(url)

    entropy_of_domain = calculate_entropy(full_domain)

   
    # Character counts
    
    number_of_special_char_in_url = len(
        re.findall(r'[^a-zA-Z0-9]', url)
    )

    number_of_digits_in_url = sum(
        c.isdigit() for c in url
    )

    number_of_digits_in_domain = sum(
        c.isdigit() for c in full_domain
    )

    number_of_dots_in_domain = full_domain.count(".")

    number_of_slash_in_url = url.count("/")

    number_of_dots_in_url = url.count(".")

    number_of_hyphens_in_domain = full_domain.count("-")

    number_of_hyphens_in_url = url.count("-")

    number_of_equal_in_url = url.count("=")

    number_of_questionmark_in_url = url.count("?")

    
    # Digit-related binary features
    
    having_digits_in_domain = int(
        any(ch.isdigit() for ch in full_domain)
    )

    number_of_digits_in_subdomain = sum(
        c.isdigit() for c in subdomain
    )

    # repeated digits (11,22,33,...)
    having_repeated_digits_in_domain = int(
        re.search(r'(\d)\1+', full_domain) is not None
    )

    
    # Final feature vector
    
    features = {
        "url_length": url_length,
        "average_subdomain_length": average_subdomain_length,
        "entropy_of_url": entropy_of_url,
        "entropy_of_domain": entropy_of_domain,
        "domain_length": domain_length,
        "number_of_subdomains": number_of_subdomains,
        "number_of_special_char_in_url": number_of_special_char_in_url,
        "number_of_digits_in_url": number_of_digits_in_url,
        "number_of_digits_in_domain": number_of_digits_in_domain,
        "number_of_dots_in_domain": number_of_dots_in_domain,
        "number_of_slash_in_url": number_of_slash_in_url,
        "number_of_dots_in_url": number_of_dots_in_url,
        "path_length": path_length,
        "number_of_hyphens_in_domain": number_of_hyphens_in_domain,
        "number_of_hyphens_in_url": number_of_hyphens_in_url,
        "having_digits_in_domain": having_digits_in_domain,
        "number_of_equal_in_url": number_of_equal_in_url,
        "number_of_digits_in_subdomain": number_of_digits_in_subdomain,
        "having_repeated_digits_in_domain": having_repeated_digits_in_domain,
        "number_of_questionmark_in_url": number_of_questionmark_in_url,
    }

    return features