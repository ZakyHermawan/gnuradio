from ..io.yaml import GRCDumper
import yaml

def dump(data, stream=None, **kwargs):
    config = dict(stream=stream, default_flow_style=False,
                  indent=4, Dumper=GRCDumper)
    config.update(kwargs)
    return yaml.dump_all([data], **config)
