from abc import ABCMeta, abstractmethod


class IRpa:
    __metaclass__ = ABCMeta

    def __init__(self, meta_data):
        self.url = meta_data['URL']
        self.name = meta_data['RPA_NAME']
        self.driver_name = meta_data['DRIVER_NAME']

    def reset(self):
        self.url = None
        self.name = None
        self.driver_name = None

    @abstractmethod
    def get_code_lookup(self):
        raise NotImplementedError

    @abstractmethod
    def extract_data(self, portal, lookup_code, storage_pth, filename):
        raise NotImplementedError

    @abstractmethod
    def get_driver(self, download_directory=None):
        raise NotImplementedError

    @abstractmethod
    def versions(self) -> dict:
        """
        return: JSON version group by version. ex: {'v1': {'url': 'link', 'Supplier': 'misa'}
        """
        raise NotImplementedError

    @abstractmethod
    def get_latest_version(self) -> dict:
        """
        return: latest version
        """
        raise NotImplementedError

    def get_name(self):
        return self.name

    def get_driver_name(self):
        return self.driver_name
