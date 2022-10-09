import argparse
from app_gradio import app
from gen.gen import Gen

gen = Gen()

def main(args):
    frontend = app.make_frontend(
        gen.predict,
        flagging=args.flagging
    )
    frontend.launch(share=True)


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
