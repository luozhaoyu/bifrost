# -*- coding: utf-8 -*-
"""
    app.py
    ~~~~~~~~~~~~~~

    A brief description goes here.
"""
import os
from bottle import run, route
from bottle import template
from bottle import request

import markdown


@route('/index')
@route('/')
@route('/article')
def index():
    filenames = os.listdir('markdowns')
    articles = [i[:i.index('.')] for i in filenames]
    return "<br/>".join(articles)


@route('/article/:article', method='GET')
def article(article):
    article_htmlpath = os.path.join('htmls', '%s.html' % article)
    if os.path.isfile(article_htmlpath):
        content = None
        with open(article_htmlpath, 'r') as f:
            content = f.read()
        return content
    else:
        article_path = os.path.join('markdowns', '%s.md' % article)
        article_meta_path = os.path.join('metas', '%s.meta' % article)
        if os.path.isfile(article_path):
            md_content = None
            with open(article_path, 'r') as f:
                md_content = f.read()
            md = markdown.Markdown()
            content = md.convert(md_content)
            return content
        else:
            return "file <b>%s</b> not existed" % article


@route('/new', method='GET')
def new_article():
    return template(os.path.join('templates', 'new'))


@route('/article', method='POST')
def create_article():
    """搞清楚HTML5 RESTful问题"""
    f = request.forms.decode('utf-8')
    title = f.get('title', '')
    content = f.get('content', '')
    new_article_path = os.path.join('markdowns', '%s.md' % title)
    if os.path.exists(new_article_path):
        return "%s exists! PLEASE SAVE YOUR ARTICLE %s" % (title, content)
    else:
        with open(new_article_path, 'w') as f:
            f.write(content)
        return 'SUCCESS!'


@route('/edit/:article', method='GET')
def start_edit_article(article):
    article_path = os.path.join('markdowns', '%s.md' % article)
    if os.path.isfile(article_path):
        content = ''
        with open(article_path, 'r') as f:
            content = f.read()

        edit_template_string = ''
        with open('templates/edit.html', 'r') as f:
            edit_template_string = f.read()
        edit_template_string = edit_template_string.replace('TITLE', article)
        edit_template_string = edit_template_string.replace('CONTENT', content)
        return edit_template_string
    else:
        return "WRONG EDIT! ARTICLE %s NOT EXISTS!" % article


@route('/article/:article', method='PUT')
def update_article(article):
    """注意title修改后的问题"""
    print("UPDATE!")


def _main(argv):
    port = int(argv[1]) if len(argv) > 1 else 8080
    run(host='127.0.0.1', port=port, debug=True)


if __name__ == '__main__':
    import sys
    _main(sys.argv)
