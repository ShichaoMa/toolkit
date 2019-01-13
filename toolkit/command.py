import os

from markdown import markdown

from .monitors import Service

tpl = """
<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="%s">
<style>
    .markdown-body {
        box-sizing: border-box;
        min-width: 200px;
        max-width: 980px;
        margin: 0 auto;
        padding: 45px;
    }
 
    @media (max-width: 767px) {
        .markdown-body {
            padding: 15px;
        }
    }
</style> 
<article class="markdown-body">
    %s
</article>
</html>
"""


class MarkDownHelper(Service):

    def run(self):
        buffer = markdown(open(self.args.input).read(),
                          extensions=['markdown.extensions.extra'])
        output = self.args.input + ".html"
        css = self.args.css

        with open(output, "w") as f:
            f.write(tpl % (css, buffer))

        with open(os.path.join(os.path.dirname(output), css), "w") as f:
            f.write(open(os.path.join(os.path.dirname(__file__), css)).read())

        self.logger.info(f"打开{output}.")
        os.system(f"open {output}")

    def enrich_parser_arguments(self):
        super(MarkDownHelper, self).enrich_parser_arguments()
        self.parser.add_argument("input", help="markdown file.")
        self.parser.add_argument(
            "-c", "--css", help="css file name.", default="github-markdown.css")


def main():
    MarkDownHelper().run()
