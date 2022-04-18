import os

import yaml

from PrometeusPBX.defaults import DEFAULT_CONFIG


def load_config():
    with open(
        os.environ.get(
            "PROMETEUSPBX_CONFIG_PATH", "/etc/prometeuspbx/prometeuspbx.yaml"
        ),
        "r",
    ) as stream:
        try:
            file_content = yaml.safe_load(stream)
            config = file_content["prometeuspbx"]

            config = {**DEFAULT_CONFIG, **config}
        except yaml.YAMLError:
            config = DEFAULT_CONFIG

    return config
