import uuid
import os
import tempfile

from werkzeug import secure_filename
from flask import Blueprint, request, send_file, jsonify
from Utils.ZipUtils import UnzipFile
from FileNodes.FileTree import GetFileTree
from Parser.SyntaxTree import GetProjectSyntaxTree

apiBp = Blueprint('api', __name__, url_prefix="/api")

@apiBp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        streamData = file.read()
        temp_filename = os.path.join(
            tempfile.gettempdir(), 'tmp_' + file.filename)

        with open(temp_filename, 'wb') as f:
            f.write(streamData)
        
        fileKey, path = UnzipFile(temp_filename)
        fileKey = str(fileKey)
        fileTree = GetFileTree(path, fileKey)
        syntaxTree = GetProjectSyntaxTree(path, False)

    return jsonify({
        'fileKey': fileKey,
        'fileTree': fileTree,
        'syntaxTree': syntaxTree
    })

@apiBp.route('/getFile/<fileKey>/<path:filePath>')
def getFile(fileKey, filePath):
    path = os.path.normpath(os.path.join(os.getcwd(), './upload/' + fileKey + '/' + filePath))
    with open(path, 'r', encoding='utf8') as f:
        content = f.read()
    
    return jsonify({
        'content': content
    })


