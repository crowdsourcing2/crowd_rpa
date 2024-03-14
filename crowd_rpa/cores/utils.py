import re
import fitz
import tldextract

from cores import providers
from settings import cfg


def find_links_in_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    links = []

    for page in doc:
        links += re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                           page.get_text())
        for link in page.get_links():
            links.append(link.get("uri"))
    doc.close()
    return max(links, key=lambda x: len(x))


def find_lookup_code_in_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    code = None
    code_patterns = [
        r'Mã tra cứu: (\w+)',
        r'\(Invoice code\):\s*([A-Z0-9]+)',
        r'Mã tra cứu HĐĐT này: (\w+)',
        r'mã tra cứu:\s*([A-Z0-9]+)'
    ]

    for page in doc:
        for pattern in code_patterns:
            temp = re.search(pattern, page.get_text())
            if temp:
                code = temp.group(1)
    doc.close()
    return code


def find_related_portal(domain, config):
    for provider, services in config['portals'].items():
        for service, data in services.items():
            for d in data['domains']:
                if domain == d or d.endswith(domain):
                    return service
    return None


def get_portal_router(input_domain):
    extracted_domain = tldextract.extract(input_domain)
    domain = extracted_domain.registered_domain
    related_portal = find_related_portal(domain, cfg.PORTALS_CONFIG)
    return related_portal


def get_portal_module(portal):
    instance = None
    for provider in providers:
        if provider.get_name().lower() == portal:
            return provider

    return instance


if __name__ == '__main__':
    # pdf_path = r"C:\Users\phduo\Downloads\crowd_electronic\evat.pdf"
    # links = find_lookup_code_in_pdf(pdf_path)
    # print("Links below the threshold on page", links)
    input_domain = "https://tracuu.evat.vn/"
    portal_name = get_portal_router(input_domain)
    ins = get_portal_module(portal_name)
    print(ins.get_name())
