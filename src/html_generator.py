import os.path


def get_html_page(path, files):
    # create table of files
    files_html = ''
    for file in files:
        files_html += f"<li> <a href=\"{os.path.join(path, file)}\">{file}</a> </li>\n"

    with open("html_template.html", "r") as f:
        html_template = f.read()

    # add files to the html template
    return html_template.format(path=path, table=files_html)
