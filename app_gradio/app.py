"""Provide an image from your webcam and a question and get back out a string!"""
import argparse
import json
import logging
import os
from pathlib import Path
from typing import Callable
import random

import gradio as gr
from PIL.Image import Image

from gen.gen import Gen

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # do not use GPU

logging.basicConfig(level=logging.INFO)

APP_DIR = Path(__file__).resolve().parent  # what is the directory for this application?
FAVICON = APP_DIR / "logo.png"  # path to a small image for display in browser tab and social media
README = APP_DIR / "README.md"  # path to an app readme file in HTML/markdown

DEFAULT_PORT = 11700

max_tokens_min = 20
max_tokens_max = 200


def main(args):
    frontend = make_frontend(
        Gen.predict,
        flagging=args.flagging
    )
    frontend.launch(
        server_name="0.0.0.0",  # make server accessible, binding all interfaces  # noqa: S104
        server_port=DEFAULT_PORT,  # set a port to bind to, failing if unavailable
        share=True,  # should we create a (temporary) public link on https://gradio.app?
        favicon_path=FAVICON,  # what icon should we display in the address bar?
    )


def make_frontend(
    fn: Callable[[Image], str],
    flagging: bool = False
):
    """Creates a gradio.Interface frontend for an image + text to text function."""
    img_examples_dir = Path("training-strips") / "images"
    img_example_fnames = [elem for elem in os.listdir(img_examples_dir) if elem.endswith(".png")]
    img_example_paths = [img_examples_dir / fname for fname in img_example_fnames]

    random_numbers = list(range(20, 201))
    examples = [[str(img_path), random.choice(random_numbers)] for img_path in img_example_paths]

    allow_flagging = "never"
    if flagging: # logging user feedback to a local CSV file
        allow_flagging = "manual"  
        flagging_callback = gr.CSVLogger()
        flagging_dir = "flagged"
    else:
        flagging_callback, flagging_dir = None, None

    readme = _load_readme(with_logging=allow_flagging == "manual")

    # build a basic browser interface to a Python function
    frontend = gr.Interface(
        fn=fn,  # which Python function are we interacting with?
        outputs=[gr.components.Textbox(label="OCR"), gr.components.Textbox(label="Am I a writer?...")],  # what output widgets does it need? the default text widget
        # what input widgets does it need? we configure an image widget
        inputs=[gr.components.Image(type="pil", label="Comic Strip"), gr.Slider(max_tokens_min, max_tokens_max)],
        title="Scribble",  # what should we display at the top of the page?
        thumbnail=FAVICON,  # what should we display when the link is shared, e.g. on social media?
        description=__doc__,  # what should we display just above the interface?
        article=readme,  # what long-form content should we display below the interface?
        examples=examples,  # which potential inputs should we provide?
        cache_examples=False,  # should we cache those inputs for faster inference? slows down start
        allow_flagging=allow_flagging,  # should we show users the option to "flag" outputs?
        flagging_options=["incorrect", "offensive", "other"],  # what options do users have for feedback?
        flagging_callback=flagging_callback,
        flagging_dir=flagging_dir
    )

    return frontend


def _load_readme(with_logging=False):
    with open(README) as f:
        lines = f.readlines()
        if not with_logging:
            lines = lines[: lines.index("<!-- logging content below -->\n")]

        readme = "".join(lines)
    return readme


def _make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--flagging",
        action="store_true",
        help="Pass this flag to allow users to 'flag' model behavior and provide feedback.",
    )

    return parser


if __name__ == "__main__":
    parser = _make_parser()
    args = parser.parse_args()
    main(args)
