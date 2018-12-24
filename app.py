import os
import flask


ROOT_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.abspath(os.path.join(ROOT_PATH,"static"))
FILE_SAVE_PATH = os.path.abspath(os.path.join(ROOT_PATH,"file"))


app = flask.Flask(__name__)
app.static_folder = STATIC_PATH

def json_response(code=0, msg='okay', data=None):
    return flask.jsonify(code=code,msg=msg,data=data)

def okay_response(data=None):
    return json_response(data=data)


@app.route("/")
def index():
    return flask.redirect("/static/index.html")


@app.route("/file/list")
def file_list():
    '''for post_dir_item in os.listdir(const.POST_DIR_PATH):
        post_dir = os.path.join(const.POST_DIR_PATH, post_dir_item)
        if (os.path.isdir(post_dir)):
            print()
            '''
    return okay_response()


@app.route("/file/delete", methods=["POST"])
def file_delete():
    return okay_response()


@app.route("/file/upload", methods=["POST"])
def file_upload():
    return okay_response()

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
    