import os
import flask
import time
from werkzeug import secure_filename


ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT_PATH, "static")
FILE_SAVE_PATH = os.path.join(ROOT_PATH, "file")


app = flask.Flask(__name__)
app.static_folder = STATIC_PATH


def json_response(code=0, msg='okay', data=None):
    return flask.jsonify(code=code, msg=msg, data=data)


def okay_response(data=None):
    return json_response(data=data)


@app.route("/")
def index():
    return flask.redirect("/static/index.html")


def timestamp_to_time(timestamp):
    time_struct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)


def size_humanize(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB',
             'EB', 'ZB', 'YB', 'BB', 'NB', 'DB', 'CB']

    try:
        size = int(size)
    except:
        return False

    if size < 0:
        return False

    for unit in units:
        if size >= 1024:
            size //= 1024
        else:
            size_h = '{} {}'.format(size, unit)
            return size_h

    size_h = '{} {}'.format(size, units[-1])
    return size_h


@app.route("/file/list")
def file_list():
    files = []
    for file_name in os.listdir(FILE_SAVE_PATH):
        file_path = os.path.join(FILE_SAVE_PATH, file_name)
        if os.path.isfile(file_path):
            file = {
                'name': file_name
            }
            file['time'] = timestamp_to_time(os.path.getmtime(file_path))
            file['size'] = size_humanize(os.path.getsize(file_path))
            files.append(file)
    data = {
        'files': files
    }
    return okay_response(data)


def generate_file(file_path):
    with open(file_path, "rb") as fd:
        while True:
            chunk = fd.read(10 * 1024 * 1024)
            if not chunk:
                break
            yield chunk


@app.route("/file/download")
def file_download():
    file_name = flask.request.args.get("file_name", None)
    if file_name is None:
        return json_response(code=1000, msg='缺少参数：file_name')
    file_path = os.path.join(FILE_SAVE_PATH, file_name)
    if not os.path.exists(file_path):
        return json_response(code=1001, msg='文件不存在')

    response = flask.Response(generate_file(
        file_path=file_path), mimetype='application/gzip')
    response.headers['Content-Disposition'] = "attachment; filename=%s" % (
        file_name)
    response.headers['content-length'] = os.stat(str(file_path)).st_size
    return response


@app.route("/file/delete", methods=["POST"])
def file_delete():
    file_name = flask.request.form.get("file_name", None)
    if file_name is None:
        return json_response(code=1000, msg='缺少参数：file_name')
    file_name = secure_filename(file_name)
    file_path = os.path.join(FILE_SAVE_PATH, file_name)
    if not os.path.exists(file_path):
        return json_response(code=1001, msg='文件不存在')
    os.unlink(file_path)
    return okay_response()


@app.route("/file/upload", methods=["POST"])
def file_upload():
    file = flask.request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(FILE_SAVE_PATH, filename)
        if os.path.exists(file_path):
            return json_response(code=1002, msg='上传失败，文件已存在')
        file.save(file_path)
        return okay_response()
    else:
        return json_response(code=1003, msg='上传失败，没有文件')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
