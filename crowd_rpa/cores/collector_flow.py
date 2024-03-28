import time
from pathlib import Path
from copy import deepcopy

from crowd_rpa.cores.utils import *
from crowd_rpa.cores.flow_enum import ProcessStatus, FlowName, CollectorStatus


class CollectorFlow:
    GET_PORTAL = 0
    LOOKUP_INFO = GET_PORTAL + 1
    ADDITIONAL_CODE = LOOKUP_INFO + 1
    DOWNLOAD_INFO = ADDITIONAL_CODE + 1
    SUBMITTED = DOWNLOAD_INFO + 1
    _FLOW = [
        GET_PORTAL,
        LOOKUP_INFO,
        ADDITIONAL_CODE,
        DOWNLOAD_INFO,
        SUBMITTED
    ]
    SUCCESS = 'SUCCESS'
    _METADATA = {
        'root_pth': '/',
        'data': {},
        'type': 'CREATE'
    }
    _ITEM = {
        'status': ProcessStatus.CREATE.value,
        'time_process': 0,
        'steps': _FLOW,
        'in_step': 'GET_PORTAL',
    }

    def __init__(self):
        self.steps = [self.get_portal, self.lookup_code, self.additional_code, self.download_info, self.submit]
        self.config = None
        self._val = None
        self._storage_pth = None

    def reset(self):
        self.config = None
        self._val = None
        self._storage_pth = None

    def set_step(self, flow_type, status, step_val, in_step, msg):
        self.config['data'][self._val]['status'] = status
        self.config['data'][self._val]['steps'][flow_type] = step_val
        self.config['data'][self._val]['in_step'] = in_step
        self.config['data'][self._val]['message'] = msg

    def get_portal(self):
        next_step = True
        try:
            url = find_links_in_pdf(
                f'{self.config["root_pth"]}/{self._val}')
            self.config['data'][self._val]['portal'] = get_portal_router(url)
            self.set_step(flow_type=self.GET_PORTAL,
                          status=FlowName.GET_PORTAL.value,
                          step_val=url,
                          in_step=FlowName.GET_PORTAL.value,
                          msg=self.SUCCESS)
            if not get_portal_router(input_domain=url):
                next_step = False

        except Exception as e:
            self.set_step(flow_type=self.GET_PORTAL,
                          status=CollectorStatus.NF_PORTAL.value,
                          step_val=None,
                          in_step=FlowName.GET_PORTAL.value,
                          msg=e.__str__())
            next_step = False

        return next_step

    def lookup_code(self):
        next_step = True
        try:
            code = find_lookup_code_in_pdf(
                f'{self.config["root_pth"]}/{self._val}')
            if not code:
                raise ValueError('Lookup code is not found')
            self.set_step(flow_type=self.LOOKUP_INFO,
                          status=FlowName.LOOKUP_INFO.value,
                          step_val=code,
                          in_step=FlowName.LOOKUP_INFO.value,
                          msg=self.SUCCESS)

        except Exception as e:
            self.set_step(flow_type=self.LOOKUP_INFO,
                          status=CollectorStatus.NF_LOOKUP_INFO.value,
                          step_val=None,
                          in_step=FlowName.LOOKUP_INFO.value,
                          msg=e.__str__())
            next_step = False

        return next_step

    def additional_code(self):
        next_step = True
        try:
            instance = get_portal_module(self.config['data'][self._val]['portal'])
            if not hasattr(instance, cfg.USE_COMPANY_CODE_ATTR.lower()):
                self.set_step(flow_type=self.ADDITIONAL_CODE,
                              status=FlowName.ADDITIONAL_CODE.value,
                              step_val=None,
                              in_step=FlowName.ADDITIONAL_CODE.value,
                              msg=self.SUCCESS)
                return next_step
            code = find_company_code_in_pdf(
                f'{self.config["root_pth"]}/{self._val}')
            self.set_step(flow_type=self.ADDITIONAL_CODE,
                          status=FlowName.ADDITIONAL_CODE.value,
                          step_val=code,
                          in_step=FlowName.ADDITIONAL_CODE.value,
                          msg=self.SUCCESS)
            if not code:
                raise ValueError(CollectorStatus.NF_ADDITIONAL_CODE.value)
        except Exception as e:
            self.set_step(flow_type=self.ADDITIONAL_CODE,
                          status=CollectorStatus.NF_ADDITIONAL_CODE.value,
                          step_val=None,
                          in_step=FlowName.ADDITIONAL_CODE.value,
                          msg=e.__str__())
            next_step = False
        return next_step

    def download_info(self):
        next_step = True

        try:
            instance = get_portal_module(self.config['data'][self._val]['portal'])
            storage_path = instance.extract_data(self.config['data'][self._val]['steps'][self.GET_PORTAL],
                                                 self.config['data'][self._val]['steps'][self.LOOKUP_INFO],
                                                 self.config['storage_pth'],
                                                 self._val.split('.')[0],
                                                 self.config['data'][self._val]['steps'][self.ADDITIONAL_CODE])
            instance.reset()
            if not is_valid_download_info(storage_path):
                raise ValueError("Downloaded files are incomplete")
            self.set_step(flow_type=self.DOWNLOAD_INFO,
                          status=FlowName.DOWNLOAD_INFO.value,
                          step_val=storage_path,
                          in_step=FlowName.DOWNLOAD_INFO.value,
                          msg=self.SUCCESS)

        except Exception as e:
            self.set_step(flow_type=self.DOWNLOAD_INFO,
                          status=CollectorStatus.INVALID_DOWNLOAD_INFO.value,
                          step_val=None,
                          in_step=FlowName.DOWNLOAD_INFO.value,
                          msg=e.__str__())
            next_step = False
        return next_step

    def submit(self):
        self.set_step(flow_type=self.SUBMITTED,
                      status=FlowName.SUBMITTED.value,
                      step_val=self.SUCCESS,
                      in_step=FlowName.SUBMITTED.value,
                      msg=self.SUCCESS)
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
            t = time.time()
            index = eval(f"self.{data[d]['in_step']}")
            if index > 0:
                start_idx = index
            else:
                start_idx = 0
            for step in self.steps[start_idx:]:
                self._val = d
                if not step():
                    break
            time.sleep(1)
            self.config['data'][self._val]['time_process'] = f'{round(time.time() - t, 2)}s'

        return self.config


collector_ins = CollectorFlow()
