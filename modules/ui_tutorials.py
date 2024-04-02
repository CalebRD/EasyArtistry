##components of the tutorials tab will be implemented here
import gradio as gr

from modules import ui_common, shared, script_callbacks, scripts, sd_models, sysinfo, timer
from modules.call_queue import wrap_gradio_call
from modules.shared import opts
from modules.ui_components import FormRow
from modules.ui_gradio_extensions import reload_javascript
from concurrent.futures import ThreadPoolExecutor, as_completed

## retrieves the value associated with a given key and grabs the component
## arguments and updates the gradio with the found arguements and value
def get_value_for_setting(key):
    value = getattr(opts, key)

    info = opts.data_labels[key]
    args = info.component_args() if callable(info.component_args) else info.component_args or {}
    args = {k: v for k, v in args.items() if k not in {'precision'}}

    return gr.update(value=value, **args)

