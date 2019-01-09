import os

from markdown import markdown

from .monitors import Service


class MarkDownHelper(Service):

    def run(self):
        buffer = markdown(open(self.args.input).read(),
                          extensions=['markdown.extensions.extra'])
        with open(self.args.output, "w") as f:
            f.write(f"<html><body>{buffer}</body></html>")

        self.logger.info(f"打开{self.args.output}.")
        os.system(f"open {self.args.output}")

    def enrich_parser_arguments(self):
        super(MarkDownHelper, self).enrich_parser_arguments()
        self.parser.add_argument(
            "-i", "--input", required=True, help="markdown file. ")
        self.parser.add_argument(
            "-o", "--output", help="html file", default="output.html")


def main():
    MarkDownHelper().run()
