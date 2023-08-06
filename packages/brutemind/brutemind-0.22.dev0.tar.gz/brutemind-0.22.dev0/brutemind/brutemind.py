#
#   MIT License
#
#    brutemind framework for python
#    Copyright (C) 2018 Michael Lin, Valeriy Garnaga
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import io
import pathlib
from urllib.request import urlretrieve
import json
import base64
import zipfile
import threading
import time
import shutil

import requests
import tensorflow as tf
import pandas as pd
import numpy as np
from brutemind import models

os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"
tf.logging.set_verbosity(tf.logging.ERROR)

class GeneticAlgoSearch(object):

    DEBUG_MODE = False
    SERVER = "http://oliver.dnsdojo.org:5001"
    MODELS_FOLDER = "models"
    DATA_FOLDER = "data"
    TEST_ZIP_INPUTS_FILENAME = 'data/test-inputs.zip'
    TEST_ZIP_OUTPUTS_FILENAME = 'data/test-outputs.zip'
    TEST_CSV_INPUTS_FILENAME = 'data/test-inputs.csv'
    TEST_CSV_OUTPUTS_FILENAME = 'data/test-outputs.csv'
    RELATIVE_ERROR_ZERO_BIAS = 0.001
    REQUEST_TIMEOUT = (60, 180)

    def __init__(self, parameters=None, server=None):
        self.parameters = parameters
        self.server = server if not server is None else GeneticAlgoSearch.SERVER
        self.model = None
        self.stopPredictFlag = True
        self.data = None
        self.inputData = None
        self.outputData = None

    def get_params(self):
        return {
            "status": self.getStatus(),
            "params": self.parameters
        }

    def get_result(self):
        return self.getBestModel(GeneticAlgoSearch.MODELS_FOLDER)

    def predictResult(self):
        accuracy = None
        folder = None
        self.get_test_data()
        if  not self.inputData is None and not self.outputData is None:
            identity, _, model, folder, _ = self.getBestModel(GeneticAlgoSearch.MODELS_FOLDER)
            if not identity is None:
                # clusterization
                if not np.any((self.outputData > 0.0) & (self.outputData < 1.0)):
                    correctAnswersCount = 0
                    for i in range(len(self.inputData)):
                        y = model.run([self.inputData[i]])
                        if not y is None:
                            n = len(self.outputData[i])
                            if n == 1:
                                if (self.outputData[i][0] == 1.0 and y[0][0] > 0.5) or (self.outputData[i][0] == 0.0 and y[0][0] <= 0.5):
                                    correctAnswersCount += 1
                            else:
                                okIndex = 0
                                resultIndex = 0
                                resultValue = y[0][0]
                                for j in range(n):
                                    if self.outputData[i][j] == 1.0:
                                        okIndex = j
                                    if resultValue < y[0][j]:
                                        resultIndex = j
                                        resultValue = y[0][j]
                                if okIndex == resultIndex:
                                    correctAnswersCount += 1
                    accuracy = 100.0 * correctAnswersCount / len(self.outputData)
                else:
                    accuracy = 0.0
                    for i in range(len(self.inputData)):
                        y = model.run([self.inputData[i]])
                        if y is None:
                            accuracy += 1.0
                        else:
                            a = 0.0
                            for j in range(len(self.outputData[i])):
                                t = abs(y[0][j] - self.outputData[i][j]) / (self.outputData[i][j] + GeneticAlgoSearch.RELATIVE_ERROR_ZERO_BIAS)
                                if t is None or t > 1.0:
                                    t = 1.0
                                a += t
                            accuracy += a / len(self.outputData[i])
                    accuracy = 100.0 * (1.0 - (accuracy / len(self.inputData)))
        return accuracy, folder

    def predictThread(self, callback=None, accuracy=None, stop=True):
        maxAccuracy = 0
        while not self.stopPredictFlag:
            a, f = self.predictResult()
            if not a is None and a > maxAccuracy:
                maxAccuracy = a
                if (not accuracy is None and a >= accuracy) or accuracy is None:
                    callback(self, a, f)
                    if stop:
                        self.stopPredictFlag = True
                else:
                    if not f is None:
                        shutil.rmtree(f, ignore_errors=True)
            else:
                if not f is None:
                    shutil.rmtree(f, ignore_errors=True)
            time.sleep(3)

    def predict(self, data=None):
        output = []
        identity, _, model, _, _ = self.getBestModel(GeneticAlgoSearch.MODELS_FOLDER)
        if not identity is None and not data is None:
            for i in data:
                output.append(model.run([i]))
        return output

    def fit(self, data, callback=None, accuracy=None, stop=True):
        self.clear()
        self.data = data
        if not os.path.exists(GeneticAlgoSearch.DATA_FOLDER):
            pathlib.Path(GeneticAlgoSearch.DATA_FOLDER).mkdir(parents=True, exist_ok=True)
        self.start()
        if not callback is None:
            self.stopPredictFlag = False
            callbackThread = threading.Thread(target=self.predictThread, args=(callback, accuracy, stop))
            callbackThread.start()

    def post_server(self, url, data):
        repeats = 3
        while repeats > 0:
            try:
                response = requests.post(url, data=data, timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
                return response.json()
            except (requests.exceptions.ChunkedEncodingError) as e:
                repeats -= 1
                if repeats <= 0:
                    raise e

    def get_test_data(self):
        if self.inputData is None or self.outputData is None:
            # FIXME: server API should be changed
            data = self.post_server('{}/get_test_csv_zip'.format(self.server), json.dumps({}))
            if not data is None and not data.get("inputTestCsvZip", None) is None:
                zpf = zipfile.ZipFile(io.BytesIO(base64.b64decode(data['inputTestCsvZip'])), "r")
                fl = zpf.namelist()[0]
                zpf.extract(fl, GeneticAlgoSearch.DATA_FOLDER, data["zipPassword"])
                zpf.close()
                zpf = zipfile.ZipFile(io.BytesIO(base64.b64decode(data['outputTestCsvZip'])), "r")
                fl = zpf.namelist()[0]
                zpf.extract(fl, GeneticAlgoSearch.DATA_FOLDER, data["zipPassword"])
                zpf.close()
                self.inputData = pd.read_csv(GeneticAlgoSearch.TEST_CSV_INPUTS_FILENAME, sep=',', encoding='utf-8').astype(np.float64).values
                self.inputData = np.array([x[1:] for x in self.inputData])
                self.outputData = pd.read_csv(GeneticAlgoSearch.TEST_CSV_OUTPUTS_FILENAME, sep=',', encoding='utf-8').astype(np.float64).values
                self.outputData = np.array([x[1:] for x in self.outputData])
            else:
                self.inputData = None
                self.outputData = None
        if self.inputData is None or self.outputData is None:
            return None, None 
        else:
            return self.inputData, self.outputData

    def sendModelsList(self):
        response = requests.post("{}/api/v1/register_models_list".format(self.server), data=json.dumps({
            "autentificationToken": None,
            "modelsList": self.parameters
        }), timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
        return response.json()

    def sendData(self):
        if not self.data is None:
            responseTrain = requests.post("{}/api/v1/add_train_csv_zip_url".format(self.server), data=json.dumps({
                "autentificationToken": None,
                "inputTrainCsvZipUrl": self.data.inputTrainCsvZipUrl,
                "outputTrainCsvZipUrl": self.data.outputTrainCsvZipUrl,
                "refreshData": self.data.refreshData
            }), timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
            responseTest = requests.post("{}/api/v1/add_test_csv_zip_url".format(self.server), data=json.dumps({
                "autentificationToken": None,
                "inputTestCsvZipUrl": self.data.inputTestCsvZipUrl,
                "outputTestCsvZipUrl": self.data.outputTestCsvZipUrl,
                "refreshData": self.data.refreshData
            }), timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
            return {
                "responseTrain": responseTrain.json(),
                "responseTest": responseTest.json(),
            }
        return None

    def start(self):
        self.sendModelsList()
        if self.sendData() is None:
            raise RuntimeError("Nothing to start. No data.")
        else:
            response = requests.post("{}/api/v1/start".format(self.server), data=json.dumps({
                "autentificationToken": None
            }))
            return response.json()

    def getStatus(self):
        response = requests.post("{}/api/v1/get_status".format(self.server), data=json.dumps({
            "autentificationToken": None
        }), timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
        return response.json()

    def getBestModel(self, path):
        try:
            response = requests.post("{}/api/v1/get_best_model".format(self.server), data=json.dumps({
                "autentificationToken": None
            }), timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
            args = response.json()
            identity = args.get('id', None)
            if identity is None:
                return None, None, None, None, "Processing currently ..."
            loss = args['loss']
            folder = os.path.join(path, "{} {}".format(time.strftime("%Y %b %d %H-%M-%S"), identity))
            chromosome = args['chromosome']
            layersCount = args['layersCount']
            model = io.BytesIO(base64.b64decode(args['modelZip']))
            zpf = zipfile.ZipFile(model, "r")
            if not os.path.exists(folder):
                pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
            zpf.extractall(folder)
            zpf.close()
            self.model = models.NeuralNetwork(chromosome, layersCount, {'CPU' : 8, 'GPU' : 0})
            self.model.load(os.path.join(folder))
            return identity, loss, self.model, folder, "Working ..."
        except Exception as e:
            if GeneticAlgoSearch.DEBUG_MODE:
                print(e)
            self.stopPredictFlag = True
            return None, None, None, None, "Stopped ..."

    def stop(self):
        self.stopPredictFlag = True
        response = requests.post("{}/api/v1/stop".format(self.server), data=json.dumps({
            "autentificationToken": None
        }), timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
        return response.json()

    def clear(self):
        self.stop()
        self.inputData = None
        self.outputData = None
        tryCount = 10
        while tryCount > 0:
            tryCount -= 1
            try:
                if os.path.exists(GeneticAlgoSearch.DATA_FOLDER):
                    shutil.rmtree(GeneticAlgoSearch.DATA_FOLDER)
                    pathlib.Path(GeneticAlgoSearch.DATA_FOLDER).mkdir(parents=True, exist_ok=True)

                if os.path.exists(GeneticAlgoSearch.MODELS_FOLDER):
                    shutil.rmtree(GeneticAlgoSearch.MODELS_FOLDER)
                    pathlib.Path(GeneticAlgoSearch.MODELS_FOLDER).mkdir(parents=True, exist_ok=True)
            except:
                time.sleep(5)
        response = requests.post("{}/api/v1/clear".format(self.server), data=json.dumps({
            "autentificationToken": None
        }), timeout=GeneticAlgoSearch.REQUEST_TIMEOUT)
        return response.json()
