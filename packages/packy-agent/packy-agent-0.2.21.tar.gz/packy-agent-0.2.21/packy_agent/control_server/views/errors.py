from flask import render_template


def handle_http500(e):
    return render_template('errors/500.html')


def handle_http401(e):
    return render_template('errors/401.html')
