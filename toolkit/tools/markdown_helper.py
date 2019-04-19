import os

from markdown import markdown

from ..service.monitors import Service


class MarkDownRender(object):
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

    def __init__(self, css, file_path):
        self.css = css
        self.file_path = file_path

    def __enter__(self):
        return self

    @staticmethod
    def _walk(path):
        for root, dir, filenames in os.walk(path):
            for fn in filenames:
                if fn.endswith(".md"):
                    fp = os.path.join(root, fn)
                    # 返回文件名和文件目录深度，深度用来设置css相对路径
                    yield fp, fp.replace(path, "").strip("/").count("/")

    def render(self):
        """
        用来渲染file_path下的md，将其输出为html格式
        :return:
        """
        if os.path.isfile(self.file_path):
            files = [(self.file_path, 0)]
        else:
            files = self._walk(self.file_path)

        first_page = None
        for input, deep in files:
            buffer = markdown(open(input).read(),
                              extensions=['markdown.extensions.extra'])
            output = input + ".html"
            first_page = first_page or output

            with open(output, "w") as f:
                f.write(self.tpl % ("../" * deep + self.css, buffer))
        return first_page

    def render_css(self):
        if os.path.isfile(self.file_path):
            self.file_path = os.path.dirname(self.file_path)

        with open(os.path.join(self.file_path, self.css), "w") as f:
            f.write(open(os.path.join(os.path.dirname(__file__), self.css)).read())

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.render_css()


class MarkDownHelper(Service):
    """
    将markdown文件转换成html文件并打开
    """
    def run(self):
        mk_render = MarkDownRender(self.args.css, self.args.input)

        with mk_render:
            output = mk_render.render()

            if output:
                self.logger.debug(f"打开{output}.")
                os.system(f"open {output}")
            else:
                self.logger.info("未发现可转换的文件！")

    def enrich_parser_arguments(self):
        super(MarkDownHelper, self).enrich_parser_arguments()
        self.parser.add_argument("input", help="markdown file or path.")
        self.parser.add_argument(
            "-c", "--css", help="css file name.", default="github-markdown.css")


def main():
    MarkDownHelper().run()
