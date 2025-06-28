
import re

def extract_episode_quality(text):
    """
    Extracts episode and quality from a given text (filename or caption).
    Returns (episode_str, quality_str)
    """

    # EPISODE detection
    episode = "EP00"
    ep_match = re.search(r'(?:EP?|Episode|E|S\d{1,2}E)(\d{1,3})', text, re.IGNORECASE)
    if ep_match:
        ep_number = ep_match.group(1).zfill(2)
        episode = f"EP{ep_number}"

    # QUALITY detection
    quality = "NA"
    quality_match = re.search(r'(360p|480p|720p|1080p|2160p|HDRip|HDTV|WEBRip|BluRay|BRRip)', text, re.IGNORECASE)
    if quality_match:
        quality = quality_match.group(1).upper()

    return episode, quality
