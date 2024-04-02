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

# Creates a GUI component for a tutorial specified by the key 
def create_tutorials_component(key, is_quicktutorials=False):
    def fun():
        return opts.data[key] if key in opts.data else opts.data_labels[key].default

    info = opts.data_labels[key]
    t = type(info.default)

    args = info.component_args() if callable(info.component_args) else info.component_args

    if info.component is not None:
        comp = info.component
    elif t == str:
        comp = gr.Textbox
    elif t == int:
        comp = gr.Number
    elif t == bool:
        comp = gr.Checkbox
    else:
        raise Exception(f'bad options item type: {t} for key {key}')

    elem_id = f"tutorials_{key}"

    if info.refresh is not None:
        if is_quicktutorials:
            res = comp(label=info.label, value=fun(), elem_id=elem_id, **(args or {}))
            ui_common.create_refresh_button(res, info.refresh, info.component_args, f"refresh_{key}")
        else:
            with FormRow():
                res = comp(label=info.label, value=fun(), elem_id=elem_id, **(args or {}))
                ui_common.create_refresh_button(res, info.refresh, info.component_args, f"refresh_{key}")
    else:
        res = comp(label=info.label, value=fun(), elem_id=elem_id, **(args or {}))

    return res

