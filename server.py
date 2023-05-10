from generation_tab_tortoise import css_tortoise, generation_tab_tortoise
import setup_or_recover
import dotenv_init
import matplotlib
import matplotlib.pyplot as plt
from generation_tab_bark import generation_tab_bark
import gradio as gr
import json
from history_tab import favorites_tab, history_tab
from model_manager import model_manager
from settings_tab import settings_tab
from config import config

setup_or_recover.dummy()
dotenv_init.init()
matplotlib.use('agg')

def save_config(text_use_gpu,
                text_use_small,
                coarse_use_gpu,
                coarse_use_small,
                fine_use_gpu,
                fine_use_small,
                codec_use_gpu,
                load_models_on_startup=False
                ):
    global config
    config["model"]["text_use_gpu"] = text_use_gpu
    config["model"]["text_use_small"] = text_use_small
    config["model"]["coarse_use_gpu"] = coarse_use_gpu
    config["model"]["coarse_use_small"] = coarse_use_small
    config["model"]["fine_use_gpu"] = fine_use_gpu
    config["model"]["fine_use_small"] = fine_use_small
    config["model"]["codec_use_gpu"] = codec_use_gpu
    config["load_models_on_startup"] = load_models_on_startup
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile, indent=2)

    return f"Saved: {str(config)}"


def load_models(
    text_use_gpu,
    text_use_small,
    coarse_use_gpu,
    coarse_use_small,
    fine_use_gpu,
    fine_use_small,
    codec_use_gpu
):

    save_config(text_use_gpu,
                text_use_small,
                coarse_use_gpu,
                coarse_use_small,
                fine_use_gpu,
                fine_use_small,
                codec_use_gpu)
    # download and load all models
    model_manager.reload_models(config)
    return gr.Button.update(value="Reload models", interactive=True)

material_symbols_css = """
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 24px !important;
    line-height: 1 !important;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
}
"""

full_css = ""
full_css += material_symbols_css
full_css += css_tortoise

with gr.Blocks(css=full_css) as demo:
    gr.Markdown("# TTS Generation WebUI (Bark & Tortoise)")
    generation_tab_bark()
    generation_tab_tortoise()

    history_tab()
    favorites_tab()

    settings_tab(config, save_config, load_models)

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0')