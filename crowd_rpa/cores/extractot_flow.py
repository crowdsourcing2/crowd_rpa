import glob

from copy import deepcopy
from crowd_rpa.cores.utils import xml_to_json, read_xml_file
from crowd_rpa.cores.flow_enum import CollectorStatus, ExtractorStatus


class ExtractorFlow:
    _ITEM = {
        'parser': None,
        'status': 'SUBMITTED',
        'message': 'SUCCESS'
    }

    def __init__(self):
        self._extract_output = {}

    def reset(self):
        self._extract_output = {}

    def infer_flow(self, meta_data: dict):
        for meta in meta_data['data'].copy():
            status = meta_data['data'][meta]['status']
            if status == CollectorStatus.SUBMITTED.value:
                xml_pth = glob.glob(rf"{meta_data['data'][meta]['steps'][3]}/*.xml")
                item = deepcopy(self._ITEM)
                if len(xml_pth) > 0:
                    xml_pth = xml_pth[0]
                    try:
                        extract_data = xml_to_json(read_xml_file(xml_pth))
                        item['parser'] = extract_data
                        item['status'] = ExtractorStatus.SUBMITTED.value
                        self._extract_output[meta] = item
                    except Exception as e:
                        item['parser'] = None
                        item['status'] = ExtractorStatus.PARSER_ERROR.value
                        item['message'] = f'{e}'
                        self._extract_output[meta] = item
                else:
                    item['parser'] = None
                    item['status'] = ExtractorStatus.XML_NOT_FOUND.value
                    item['message'] = f'XML is not found'
                    self._extract_output[meta] = item

            else:
                self._extract_output[meta] = None

        return self._extract_output


extractor_ins = ExtractorFlow()

if __name__ == '__main__':
    metadata = {'root_pth': 'C:\\Users\\phduo\\Downloads\\crowd_electronic', 'data': {
        '769367.pdf': {'status': 'CREATE', 'time_process': {},
                       'steps': ['https://www.meinvoice.vn/tra-cuu/?sc=X9IDF6VBLDZ', 'X9IDF6VBLDZ',
                                 'C:\\Users\\phduo\\PycharmProjects\\master_tools\\velociti-be\\crowd_rpa\\tests\\output\\MISA\\769367',
                                 'SUBMITTED'], 'in_step': 'SUBMITTED', 'portal': 'misa'},
        '769793.pdf': {'status': 'INVALID_DOWNLOAD_INFO', 'time_process': {},
                       'steps': ['https://van.ehoadon.vn/TCHD?MTC=W5NQT02YUQ3', 'W5NQT02YUQ3', None, 3],
                       'in_step': 'DOWNLOAD_INFO', 'portal': 'bkav'},
        '769986.pdf': {'status': 'INVALID_DOWNLOAD_INFO', 'time_process': {},
                       'steps': ['http://0402131186hd.easyinvoice.com.vn', 'U6U3Y8v00760702671042141UtPB', None, 3],
                       'in_step': 'DOWNLOAD_INFO', 'portal': 'easyinvoice'},
        'evat.pdf': {'status': 'CREATE', 'time_process': {}, 'steps': ['http://tracuu.evat.vn', None, 2, 3],
                     'in_step': 'LOOKUP_INFO', 'portal': 'evat'}},
                'storage_pth': 'C:\\Users\\phduo\\PycharmProjects\\master_tools\\velociti-be\\crowd_rpa\\tests\\output'}

    print(extractor_ins.infer_flow(metadata))
