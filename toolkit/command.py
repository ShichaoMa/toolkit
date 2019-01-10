import os

from markdown import markdown

from .monitors import Service


class MarkDownHelper(Service):

    def run(self):
        buffer = markdown(open(self.args.input).read(),
                          extensions=['markdown.extensions.extra'])
        output = self.args.input + ".html"
        with open(output, "w") as f:
            f.write(f"<html><body>{buffer}</body></html>")

        self.logger.info(f"打开{output}.")
        os.system(f"open {output}")

    def enrich_parser_arguments(self):
        super(MarkDownHelper, self).enrich_parser_arguments()
        self.parser.add_argument("input", help="markdown file.")


def main():
    MarkDownHelper().run()
