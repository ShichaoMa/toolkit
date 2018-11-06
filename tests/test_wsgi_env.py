from bottle import run, post, get, request


@get("/")
def index():

    return """
    <html>
        <body>
            <form method="post" action="/p" enctype="multipart/form-data" >
                <input name="aaa" value="bbbb" />
                <input name="bbb" type="file" />
                <input type="submit"/>
            </form>
        </body>
    </html>
    
    
    """



@post("/p")
def p():
    print(request.POST["bbb"].read())
    return "1"



run()