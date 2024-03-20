from crowd_rpa.cores.collector_flow import collector_ins
from crowd_rpa.cores.extractot_flow import extractor_ins


class CollectorOutput:
    pass


class ExtractorOutput:
    pass


def make_collector(metadata: dict) -> dict:
    '''
    Create a collector instance based on the provided metadata.

    Parameters:
        metadata (dict): A dictionary containing metadata information necessary to create the collector.

    Returns:
        Collector: A Dict of Collector flow.

    Example:
        fake_data = {
            "769367.pdf": {
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
            'root_pth': "crowd_electronic",
            'data': fake_data,
            'storage_pth': 'tests'
        }

        collector_instance = make_collector(metadata)
    '''

    # Check if required keys are present in metadata
    if 'root_pth' not in metadata or 'storage_pth' not in metadata:
        print("Invalid metadata: Missing required keys")
        return {}

    # Check if 'data' key contains valid data
    if not isinstance(metadata['data'], dict):
        print("Invalid metadata: 'data' must be a non-empty dictionary")
        return {}

    # Other conditions to check can be added here...

    # If all conditions are met, proceed to create the collector instance
    output = collector_ins.infer_flow(metadata)
    collector_ins.reset()
    return output


def make_extractor(metadata: dict, format_result_fn=None) -> dict:
    output = extractor_ins.infer_flow(metadata)
    if format_result_fn:
        output = format_result_fn(output)
    return output
