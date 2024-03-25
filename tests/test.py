import crowd_rpa


def update_in_step():
    fake_data = {"769367.pdf": {
        "status": "INVALID_DOWNLOAD_INFO",
        "time_process": {},
        "steps": [
            "https://www.meinvoice.vn/tra-cuu/?sc=X9IDF6VBLDZ",
            "X9IDF6VBLDZ",
            "NULL",
            "null",
            4
        ],
        "in_step": "DOWNLOAD_INFO",
        "portal": "misa"
    }
    }
    metadata = {
        'root_pth': r"C:\Users\phduo\Downloads\crowd_electronic",
        'data': fake_data,
        'storage_pth': r'C:\Users\phduo\PycharmProjects\master_tools\velociti-be\crowd_rpa\tests\output'
    }
    print(crowd_rpa.make_collector(metadata))


def create_flow():

    metadata = {
        'root_pth': r"C:\Users\phduo\Downloads\crowd_electronic",
        'data': {},
        'storage_pth': r'C:\Users\phduo\PycharmProjects\master_tools\velociti-be\crowd_rpa\tests\output'
    }
    print(crowd_rpa.make_collector(metadata))


if __name__ == '__main__':
    create_flow()
    # update_in_step()
