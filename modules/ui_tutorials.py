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
def get_value_for_tutorial(key):
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

class UiSettings:
    submit = None
    result = None
    interface = None
    components = None
    component_dict = None
    dummy_component = None
    quicktutorials_list = None
    quicktutorials_names = None
    text_tutorials = None
    show_all_pages = None
    show_one_page = None
    search_input = None

    def run_tutorials(self, *args):
        changed = []

        for key, value, comp in zip(opts.data_labels.keys(), args, self.components):
            assert comp == self.dummy_component or opts.same_type(value, opts.data_labels[key].default), f"Bad value for tutorials {key}: {value}; expecting {type(opts.data_labels[key].default).__name__}"

        for key, value, comp in zip(opts.data_labels.keys(), args, self.components):
            if comp == self.dummy_component:
                continue

            if opts.set(key, value):
                changed.append(key)

        try:
            opts.save(shared.config_filename)
        except RuntimeError:
            return opts.dumpjson(), f'{len(changed)} tutorials changed without save: {", ".join(changed)}.'
        return opts.dumpjson(), f'{len(changed)} tutorials changed{": " if changed else ""}{", ".join(changed)}.'

    ## determine if necessary
    # def run_tutorials_single(self, value, key):
    #     if not opts.same_type(value, opts.data_labels[key].default):
    #         return gr.update(visible=True), opts.dumpjson()

    #     if value is None or not opts.set(key, value):
    #         return gr.update(value=getattr(opts, key)), opts.dumpjson()

    #     opts.save(shared.config_filename)

    #     return get_value_for_tutorial(key), opts.dumpjson()

    def create_ui(self, loadsave, dummy_component):
        self.components = []
        self.component_dict = {}
        self.dummy_component = dummy_component

        shared.tutorials_components = self.component_dict

        script_callbacks.ui_tutorials_callback()
        opts.reorder()
    
        ## these are where the tabs for settings are created
        with gr.Blocks(analytics_enabled=False) as tutorials_interface:

            self.search_input = gr.Textbox(value="", elem_id="tutorials_search", max_lines=1, placeholder="Type key words for a tutorial", show_label=False)
            self.text_settings = gr.Textbox(elem_id="tutorials_json", value=lambda: opts.dumpjson(), visible=False)

            self.result = gr.HTML(elem_id="tutorials_result")

            # self.quicktutorials_names = opts.quicktutorials_list
            # self.quicktutorials_names = {x: i for i, x in enumerate(self.quicktutorials_names) if x != 'quicktutorials'}

            # self.quicktutorials_list = []

            previous_section = None
            current_tab = None
            current_row = None
            with gr.Tabs(elem_id="tutorials"):
                # for i, (k, item) in enumerate(opts.data_labels.items()):
                #     section_must_be_skipped = item.section[0] is None

                #     if previous_section != item.section and not section_must_be_skipped:
                #         elem_id, text = item.section

                #         if current_tab is not None:
                #             current_row.__exit__()
                #             current_tab.__exit__()

                #         gr.Group()
                #         #tabs are created here
                #         current_tab = gr.TabItem(elem_id=f"tutorials_{elem_id}", label=text)
                #         current_tab.__enter__()
                #         current_row = gr.Column(elem_id=f"column_tutorials_{elem_id}", variant='compact')
                #         current_row.__enter__()

                #         previous_section = item.section

                #     if k in self.quicktutorials_names and not shared.cmd_opts.freeze_settings:
                #         self.quicktutorials_list.append((i, k, item))
                #         self.components.append(dummy_component)
                #     elif section_must_be_skipped:
                #         self.components.append(dummy_component)
                #     else:
                #         component = create_tutorials_component(k)
                #         self.component_dict[k] = component
                #         self.components.append(component)
                
                if current_tab is not None:
                    current_row.__exit__()
                    current_tab.__exit__()

                with gr.TabItem("General", id="general", elem_id="tutorials_tab_general"):
                    gr.Markdown("# Welcome!")
                    gr.Markdown("Easy Artistry is a tool intended to aid small artists and indie studios in developing larger projects using AI image generation. Easy Artistry is **not** intended to replace human artists, but instead to expand the scope of what an already skilled artist can acomplish with a smaller amount of time and budget. Our hope is to allow individuals to create animations, comics, and concept art, and small studios to create films.")
                    gr.Markdown("\n[Example inputs and outputs]")
                    gr.Markdown("\nPlease refer to the tabs on the right hand side of the \"General\" tab for more information on each operation of Easy Artistry.")

                with gr.TabItem("Generate Images", id="generateImg", elem_id="tutorials_tab_generateImg"):
                    with gr.TabItem("Text prompt", id="textPrompt", elem_id="tutorials_tab_textPrompt"):
                        gr.Markdown("# Using a text prompt:")
                        gr.Markdown("Under the \"txt2img\" tab, there will be two types of text prompts: \"Prompt\" and \"Negative prompt\":\nPrompt: In this section, type key words for any elements you would like to **include** in your image. Examples include: \nNegative prompt: In this section, type key words for any elements you would like to **exclude** in your image. Examples include: ")
                        gr.Markdown("To adjust the image size, go to the \"Generation\" tab under the \"txt2img\". There you will see the option to adjust the width and height of your image")
                        gr.Markdown("To generate the image, under the \"txt2img\" tab click on the orange button labeled \"Generate\" on the top right hand side. The image will be generated on the bottom right hand side of the \"text2img\" tab.")
                        gr.Markdown("Additional opertions under the \"txt2img\" tab:\nYou can load the generated image into the \"img2img\" tab by clicking on this button under the generated image:\nYou can load the generated image into the \"inpaint\" tab by clicking on this button under the generated image:\nFor more information on the \"img2img\" and \"inpaint\" tab, please refer the \"Image Prompt\" and \"Completing an image\" tab")
                    with gr.TabItem("Image prompt", id="imagePrompt", elem_id="tutorials_tab_imagePrompt"):
                        gr.Markdown("# Using an image:")
                    with gr.TabItem("Completing an image", id="completeImg", elem_id="tutorials_tab_completeImg"):
                        gr.Markdown("# Filling in blank image parts:")

                with gr.TabItem("Save Images", id="saveImg", elem_id="tutorials_tab_saveImg"):
                    gr.Markdown("# Saving an image:")
                    gr.Markdown("To save your image to a specific directory:")

                with gr.TabItem("Training Model", id="trainModel", elem_id="tutorials_tab_trainModel"):
                    gr.Markdown("# Training model with your artworks:")

                with gr.TabItem("Sysinfo", id="sysinfo", elem_id="tutorials_tab_sysinfo"):
                    gr.HTML('<a href="./internal/sysinfo-download" class="sysinfo_big_link" download>Download system info</a><br /><a href="./internal/sysinfo" target="_blank">(or open as text in a new page)</a>', elem_id="sysinfo_download")

                with gr.TabItem("Licenses", id="licenses", elem_id="tutorials_tab_licenses"):
                    gr.HTML(shared.html("licenses.html"), elem_id="licenses")

            def call_func_and_return_text(func, text):
                def handler():
                    t = timer.Timer()
                    func()
                    t.record(text)

                    return f'{text} in {t.total:.1f}s'

                return handler

            
            def reload_scripts():
                scripts.reload_script_body_only()
                reload_javascript()  # need to refresh the html page

        self.interface = tutorials_interface

    # def add_quicktutorials(self):
    #     with gr.Row(elem_id="quicktutorials", variant="compact"):
    #         for _i, k, _item in sorted(self.quicktutorials_list, key=lambda x: self.quicktutorials_names.get(x[1], x[0])):
    #             component = create_tutorials_component(k, is_quicktutorials=True)
    #             self.component_dict[k] = component

    def add_functionality(self, demo):
        self.submit.click(
            fn=wrap_gradio_call(lambda *args: self.run_tutorials(*args), extra_outputs=[gr.update()]),
            inputs=self.components,
            outputs=[self.text_settings, self.result],
        )

        # for _i, k, _item in self.quicktutorials_list:
        #     component = self.component_dict[k]
        #     info = opts.data_labels[k]

        #     if isinstance(component, gr.Textbox):
        #         methods = [component.submit, component.blur]
        #     elif hasattr(component, 'release'):
        #         methods = [component.release]
        #     else:
        #         methods = [component.change]

        #     for method in methods:
        #         method(
        #             fn=lambda value, k=k: self.run_tutorials_single(value, key=k),
        #             inputs=[component],
        #             outputs=[component, self.text_settings],
        #             show_progress=info.refresh is not None,
        #         )

        # button_set_checkpoint = gr.Button('Change checkpoint', elem_id='change_checkpoint', visible=False)
        # button_set_checkpoint.click(
        #     fn=lambda value, _: self.run_settings_single(value, key='sd_model_checkpoint'),
        #     _js="function(v){ var res = desiredCheckpointName; desiredCheckpointName = ''; return [res || v, null]; }",
        #     inputs=[self.component_dict['sd_model_checkpoint'], self.dummy_component],
        #     outputs=[self.component_dict['sd_model_checkpoint'], self.text_settings],
        # )

        component_keys = [k for k in opts.data_labels.keys() if k in self.component_dict]

        def get_tutorials_values():
            return [get_value_for_tutorial(key) for key in component_keys]

        demo.load(
            fn=get_tutorials_values,
            inputs=[],
            outputs=[self.component_dict[k] for k in component_keys],
            queue=False,
        )

    def search(self, text):
        print(text)

        return [gr.update(visible=text in (comp.label or "")) for comp in self.components]
