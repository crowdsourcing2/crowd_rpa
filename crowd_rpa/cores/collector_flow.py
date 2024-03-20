from pathlib import Path
from copy import deepcopy

from crowd_rpa.cores.utils import *
from crowd_rpa.cores.flow_enum import ProcessStatus, FlowName, CollectorStatus


class CollectorFlow:
    GET_PORTAL = 0
    LOOKUP_INFO = 1
    DOWNLOAD_INFO = 2
    SUBMITTED = 3
    _FLOW = [
        GET_PORTAL,
        LOOKUP_INFO,
        DOWNLOAD_INFO,
        SUBMITTED
    ]
    _METADATA = {
        'root_pth': '/',
        'data': {},
        'type': 'CREATE'
    }
    _ITEM = {
        'status': ProcessStatus.CREATE.value,
        'time_process': {},
        'steps': _FLOW,
        'in_step': 'GET_PORTAL',
    }

    def __init__(self):
        self.steps = [self.get_portal, self.lookup_code, self.download_info, self.submit]
        self.config = None
        self._val = None
        self._storage_pth = None

    def reset(self):
        self.config = None
        self._val = None
        self._storage_pth = None

    def get_portal(self):
        next_step = True
        try:
            url = find_links_in_pdf(
                f'{self.config["root_pth"]}/{self._val}')
            self.config['data'][self._val]['steps'][self.GET_PORTAL] = url
            self.config['data'][self._val]['in_step'] = FlowName.GET_PORTAL.value
            self.config['data'][self._val]['portal'] = get_portal_router(url)
            if not get_portal_router(input_domain=url):
                next_step = False
            self.config['data'][self._val]['message'] = 'SUCCESS'

        except Exception as e:
            self.config['data'][self._val]['status'] = CollectorStatus.NF_PORTAL.value
            self.config['data'][self._val]['steps'][self.GET_PORTAL] = None
            self.config['data'][self._val]['in_step'] = FlowName.GET_PORTAL.value
            self.config['data'][self._val]['portal'] = None
            self.config['data'][self._val]['message'] = e

            next_step = False

        return next_step

    def lookup_code(self):
        next_step = True
        try:
            code = find_lookup_code_in_pdf(
                f'{self.config["root_pth"]}/{self._val}')
            self.config['data'][self._val]['steps'][self.LOOKUP_INFO] = code
            self.config['data'][self._val]['in_step'] = FlowName.LOOKUP_INFO.value
            if not code:
                next_step = False
            self.config['data'][self._val]['message'] = 'SUCCESS'
        except Exception as e:
            self.config['data'][self._val]['status'] = CollectorStatus.NF_LOOKUP_INFO.value
            self.config['data'][self._val]['steps'][self.LOOKUP_INFO] = None
            self.config['data'][self._val]['in_step'] = FlowName.LOOKUP_INFO.value
            self.config['data'][self._val]['message'] = e
            next_step = False

        return next_step

    def download_info(self):
        next_step = True

        try:
            instance = get_portal_module(self.config['data'][self._val]['portal'])
            storage_path = instance.extract_data(self.config['data'][self._val]['steps'][self.GET_PORTAL],
                                                 self.config['data'][self._val]['steps'][self.LOOKUP_INFO],
                                                 self.config['storage_pth'],
                                                 self._val.split('.')[0])
            instance.reset()
            if not is_valid_download_info(storage_path):
                raise ValueError("Downloaded files are incomplete")
            self.config['data'][self._val]['steps'][self.DOWNLOAD_INFO] = storage_path
            self.config['data'][self._val]['in_step'] = FlowName.DOWNLOAD_INFO.value
            self.config['data'][self._val]['message'] = 'SUCCESS'

        except Exception as e:
            self.config['data'][self._val]['status'] = CollectorStatus.INVALID_DOWNLOAD_INFO.value
            self.config['data'][self._val]['steps'][self.DOWNLOAD_INFO] = None
            self.config['data'][self._val]['in_step'] = FlowName.DOWNLOAD_INFO.value
            self.config['data'][self._val]['message'] = e

            next_step = False
        return next_step

    def submit(self):
        self.config['data'][self._val]['steps'][self.SUBMITTED] = 'SUBMITTED'
        self.config['data'][self._val]['in_step'] = FlowName.SUBMITTED.value
        next_step = True
        return next_step

    def infer_flow(self, meta_data: dict):
        root_pth = meta_data['root_pth']
        data = meta_data['data']
        storage_path = meta_data['storage_pth']
        if not Path(storage_path).is_dir():
            os.mkdir(storage_path)
        self._storage_pth = storage_path
        if not data:
            for f in os.listdir(rf'{root_pth}/'):
                data[f] = deepcopy(self._ITEM)

        self.config = deepcopy(meta_data)

        for d in data:
            index = eval(f"self.{data[d]['in_step']}")
            if index > 0:
                start_idx = index
            else:
                start_idx = 0
            for step in self.steps[start_idx:]:
                self._val = d
                if not step():
                    break

        return self.config


collector_ins = CollectorFlow()
