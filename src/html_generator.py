HTML_TEMPLATE = \
    """\
    <html>
    <head> 
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Directory listing for {path}</title>
     </head>
    
    <body>
        <h1>Directory listing for {path}</h1>
            <hr>
                <ul>
                {table}
                </ul>
            <hr>
    </body>
    </html>\
    """


def get_html_page(path, files):
    files_html = ''
    for file in files:
        files_html += f"<li> <a href=\"{file}\">{file}</a> </li>\n"

    return HTML_TEMPLATE.format(path=path, table=files_html)
