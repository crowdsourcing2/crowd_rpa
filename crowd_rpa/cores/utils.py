import os
import re
import fitz
import xmltodict
import tldextract

from urllib.parse import urlparse
from crowd_rpa.cores import providers
from crowd_rpa.settings import cfg


def find_links_in_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    links = []

    for page in doc:
        for tbox in page.get_text_blocks():
            link = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              tbox[4])
            out_box = list(tbox)
            if len(link) > 0:
                out_box[4] = max(link, key=lambda x: len(x))
                links += [out_box]

    doc.close()
    link = max(links, key=lambda x: x[3])
    return extract_base_url(link[4])


def find_lookup_code_in_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    code = None
    code_patterns = cfg.LOOKUP_PATTERNS

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


def is_valid_download_info(storage_pth):
    files = os.listdir(storage_pth)
    count = 0
    memories = []
    xml = '.xml'
    for file in files:
        if file.lower().endswith(xml) and xml not in memories:
            count += 1
            memories.append(xml)
    return count == 1


def read_xml_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            xml_data = file.read()
        return xml_data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def xml_to_json(xml_string):
    xml_dict = xmltodict.parse(xml_string)
    return xml_dict


def find_company_code_in_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    code = None
    code_patterns = cfg.COMPANY_PATTERNS
    for page in doc:
        for pattern in code_patterns:
            temp = re.search(pattern, page.get_text())
            if temp:
                code = temp.group(1)
    doc.close()
    return code


def extract_base_url(url):
    if url.endswith('.'):
        return url[:-1]
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    return base_url


if __name__ == '__main__':
    print(find_links_in_pdf(r'C:\Users\phduo\PycharmProjects\master_tools\velociti-be\crowd_rpa\tests\data1\misa.pdf'))