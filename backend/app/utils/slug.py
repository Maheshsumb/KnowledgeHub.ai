import re


def generate_slug(name: str) -> str:
    slug = name.lower().strip()

    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    slug = slug.strip("-")

    return slug