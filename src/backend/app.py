from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask import send_file
from flask_cors import CORS
import json as json
import os as os
import zipfile as zipfile

from audio_processor import *
from image_processor import *

app = Flask(__name__)

CORS(app)

datasetDirectory = "dataset"
inputDirectory = "input"

queryResult = []

imageProcessor = None

def ListFind(list, func):
    for item in list:
        if (func(item)):
            return item

@app.route("/api/getmusic/<int:offset>", methods=["GET"])
def GetMusic(offset):
    with open(os.path.join(datasetDirectory, "mapper.json")) as mapperfile:
        data = json.load(mapperfile)
        return {
            "name" : data[offset]['album_name'],
            "audiosrc" : data[offset]['audio_file'],
            "coversrc" : data[offset]['pic_name']
        }

@app.route("/api/getmusiclist/<string:query>/<int:offset>/<int:count>", methods=["GET"])
def GetMusicList(query, offset, count):
    query = query.removeprefix("_")
    
    if (not os.path.exists(os.path.join(datasetDirectory, "mapper.json"))):
        return Response(json.dumps([]), mimetype='application/json')

    with open(os.path.join(datasetDirectory, "mapper.json")) as mapperfile:
        data = json.load(mapperfile)
        data = [item for item in filter(lambda music: music['album_name'].startswith(query), data)]
        
        result = [{
            "name" : data[i]['album_name'],
            "audiosrc" : data[i]['audio_file'],
            "coversrc" : data[i]['pic_name']
        } for i in range(offset, min(offset + count, len(data)))]

        return Response(json.dumps(result), mimetype='application/json')

@app.route("/api/getmusiccount/<string:query>", methods=["GET"])
def GetMusicCount(query):
    query = query.removeprefix("_")

    if (not os.path.exists(os.path.join(datasetDirectory, "mapper.json"))):
        return { "count" : 0 }
    
    with open(os.path.join(datasetDirectory, "mapper.json")) as mapperfile:
        data = json.load(mapperfile)
        data = [item for item in filter(lambda music: music['album_name'].startswith(query), data)]
        return { "count" : len(data) }

@app.route("/api/getqueryresult/<int:offset>/<int:count>", methods=["GET"])
def GetQueryResult(offset, count):
    return Response(json.dumps(queryResult), mimetype='application/json')

@app.route("/api/updatedataset", methods=["POST"])
def UpdateDataset():
    global imageProcessor

    datasetFile = request.files["dataset"]
    
    datasetFile.save(datasetFile.filename)
    
    if not os.path.exists(datasetDirectory):
        os.mkdir(datasetDirectory)

    for relFileName in os.listdir(datasetDirectory):
        fullFileName = os.path.join(datasetDirectory, relFileName)
        os.remove(fullFileName)

    zipFile = zipfile.ZipFile(datasetFile.filename)
    zipFile.extractall(datasetDirectory)
    zipFile.close()

    os.remove(datasetFile.filename)

    imageProcessor = ImageProcessor((32, 32), datasetDirectory, 16)
    imageProcessor.load(datasetDirectory)

    return jsonify(success=True)

@app.route("/api/queryimage", methods=["POST"])
def QueryImage():
    global queryResult

    imageFile = request.files["query"]

    if not os.path.exists(os.path.join(datasetDirectory, inputDirectory)):
        os.mkdir(os.path.join(datasetDirectory, inputDirectory))

    for relFileName in os.listdir(os.path.join(datasetDirectory, inputDirectory)):
        fullFileName = os.path.join(os.path.join(datasetDirectory, inputDirectory), relFileName)
        os.remove(fullFileName)
    
    imageFile.save(os.path.join(os.path.join(datasetDirectory, inputDirectory), imageFile.filename))
    
    temp = imageProcessor.search(os.path.join(inputDirectory, imageFile.filename))

    with open(os.path.join(datasetDirectory, "mapper.json")) as mapperfile:
        data = json.load(mapperfile)

        queryResult = [
            {
                "name" : ListFind(data, lambda t: t['pic_name'] == temp[i][0])['album_name'],
                "audiosrc" : ListFind(data, lambda t: t['pic_name'] == temp[i][0])['audio_file'],
                "coversrc" : temp[i][0],
                "similarity" : temp[i][1]
            }

            for i in range(len(temp))
        ]
    
    return jsonify(success=True)

@app.route("/api/queryaudio", methods=["POST"])
def QueryAudio():
    global queryResult
    
    audioFile = request.files["query"]

    if not os.path.exists(inputDirectory):
        os.mkdir(inputDirectory)

    for relFileName in os.listdir(inputDirectory):
        fullFileName = os.path.join(inputDirectory, relFileName)
        os.remove(fullFileName)
    
    audioFile.save(os.path.join(inputDirectory, audioFile.filename))
    
    temp = AudioProcessor().main_process(os.path.join(inputDirectory, audioFile.filename), datasetDirectory, datasetDirectory)

    with open(os.path.join(datasetDirectory, "mapper.json")) as mapperfile:
        data = json.load(mapperfile)

        queryResult = [
            {
                "name" : ListFind(data, lambda t: t['audio_file'] == temp[i][0])['album_name'],
                "audiosrc" : temp[i][0],
                "coversrc" : ListFind(data, lambda t: t['audio_file'] == temp[i][0])['pic_name'],
                "similarity" : temp[i][1]
            }

            for i in range(len(temp))
        ]
    
    return jsonify(success=True)

@app.route("/api/resource/<string:name>", methods=["GET"])
def GetResource(name):
    return send_file(os.path.join(datasetDirectory, name))