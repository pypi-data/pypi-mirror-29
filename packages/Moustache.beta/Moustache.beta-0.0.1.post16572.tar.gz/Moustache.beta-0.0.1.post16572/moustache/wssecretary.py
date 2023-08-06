# -*- coding: utf-8 -*-

import json
import tempfile

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, session
from jinja2 import TemplateSyntaxError
from secretary import Renderer

from moustache.FusionHelper import FusionHelper
from moustache.InvalidUsage import InvalidUsage

app = Flask(__name__)
app.secret_key = 'super secret key'

OUTPUT_FORMAT_JSON_KEY = "__output_format"
OUTPUT_QUALITY_JSON_KEY = "__output_quality"


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def index():
    validation = {}
    if 'validation' in session :
        validation = session.pop('validation')
        app.logger.debug("toto")
    return render_template("test_form.html",validation=validation)


@app.route('/validate',methods=['POST'])
def validate():
    session['validation'] = {
        'is_valid': False,
        'message': ""
    }
    app.logger.debug("Starting validate API call")
    if 'template' not in request.files:
        session['validation']['message'] = "Le fichier template n'est pas présent"
        return redirect(url_for('index'))

    f = request.files['template']
    temp_template_file = tempfile.NamedTemporaryFile(suffix='.odt').name
    f.save(temp_template_file)

    app.logger.info("Saving template file %s to %s" % (f.filename, temp_template_file))

    render = Renderer()
    the_json = json.load(StringIO("{}"))
    try:
        render.render(
            temp_template_file,
            **the_json
        )
        session['validation']['is_valid'] = True
        session['validation']['message'] = "Le template est valide"
    except TemplateSyntaxError as e:
        session['validation']['message'] = "Syntax error on line %d : %s" % (e.lineno, e.message)

    return redirect(url_for('index'))


@app.route('/parse', methods=['POST'])
def parse():
    app.logger.debug("Starting parse API call")

    if 'template' not in request.files:
        raise InvalidUsage("Le fichier template n'est pas présent")

    f = request.files['template']
    temp_template_file = tempfile.NamedTemporaryFile(suffix='.odt').name
    f.save(temp_template_file)

    app.logger.info("Saving template file %s to %s" % (f.filename, temp_template_file))

    if 'json' not in request.files:
        raise InvalidUsage("Le fichier json n'est pas présent")

    j = request.files['json']
    json_content = j.stream.read()
    the_json = json.load(StringIO(json_content.decode('utf-8')))

    app.logger.debug("Retrieving json data %s" % the_json)

    gabarit_filelist = request.files.getlist("gabarit")
    gabarit_file_mapping = {}
    app.logger.info("Gabarit file list %s" % gabarit_filelist)

    for gabarit_file in gabarit_filelist:
        temp_gabarit_file = tempfile.NamedTemporaryFile(suffix='.odt').name
        gabarit_file.save(temp_gabarit_file)
        gabarit_file_mapping[gabarit_file.filename] = temp_gabarit_file
        app.logger.info("Saving gabarit %s to %s" % (gabarit_file, temp_gabarit_file))

    annexe_filelist = request.files.getlist("annexe")
    annexe_file_mapping = {}
    app.logger.info("Annexe file list %s" % annexe_filelist)

    tmp_dir = tempfile.mkdtemp()

    for annexe_file in annexe_filelist:
        temp_annexe_file = "%s/%s" % (tmp_dir, annexe_file.filename)
        annexe_file.save(temp_annexe_file)
        annexe_file_mapping[annexe_file.filename] = temp_annexe_file
        app.logger.info("Saving annexe %s to %s" % (annexe_file, temp_annexe_file))

    render = Renderer()

    try:
        result = render.render(
            temp_template_file,
            **the_json
        )
    except TemplateSyntaxError as e:
        raise InvalidUsage("Syntax error on line %d : %s" % (e.lineno, e.message))

    temp_result = tempfile.NamedTemporaryFile(suffix='.odt').name
    with open(temp_result, 'wb') as f_out:
        f_out.write(result)

    out_result = tempfile.NamedTemporaryFile(suffix='.odt').name

    helper = FusionHelper(2002, temp_result)

    if the_json.get('gabarit_mapping'):
        for gabarit_key, gabarit_value in the_json['gabarit_mapping'].items():
            if helper.search_and_select(gabarit_key):
                helper.insert_odt(gabarit_file_mapping[gabarit_value])

    if the_json.get('annexe_mapping'):
        quality = int(the_json.get(OUTPUT_FORMAT_JSON_KEY)) if the_json.get(OUTPUT_FORMAT_JSON_KEY) else 150
        for annexe_key, annexe_value in the_json['annexe_mapping'].items():
            if helper.search_and_select(annexe_key):
                helper.insert_pdf(annexe_file_mapping[annexe_value], quality=quality)

    helper.execute("UpdateAllIndexes")

    if the_json.get(OUTPUT_FORMAT_JSON_KEY) == 'pdf':
        render_in_pdf = True
        attachment_filename = "result.pdf"
        app.logger.debug("Response file format : PDF")
    else:
        render_in_pdf = False
        attachment_filename = "result.odt"
        app.logger.debug("Response file format : ODT")

    helper.save_and_close(out_result, pdf=render_in_pdf)
    app.logger.info("Send response : filename=%s" % attachment_filename)
    return send_file(out_result,
                     attachment_filename=attachment_filename,
                     as_attachment=True)


def default_app():
    return app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
