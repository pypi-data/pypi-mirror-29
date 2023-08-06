#!/usr/bin/env python

import os
from pyspark.sql import *
from pandas.io.json import json_normalize


class Spark(object):
    def __init__(self, file_path):
        self._path = os.sep.join(file_path.split(os.sep)[:-1])
        self._filename_source = (file_path.split(os.sep)[-1]).split('.')[-1]
        self._filename_normalized = (file_path.split(os.sep)[-1]).split('.')[-1]
        self._format = file_path.split('.')[-1].lower()
        try:
            self._session = SparkSession.builder \
                        .master("local") \
                        .appName("Word Count") \
                        .getOrCreate()
            self._dataframe = None
        except Exception as ex:
            print(repr(ex))

    def read(self):
        try:
            fullpath = os.path.join(self._path, self._filename_normalized)
            self._dataframe = self._session.read.load(fullpath, format=self._format)
            return self._dataframe
        except Exception as ex:
            print(repr(ex))

    def get_dataframe(self):
        return self._dataframe

    def show_dataframe(self):
        self._dataframe.show()

    def to_parquet(self, name=None):
        try:
            if not name:
                name = self._filename_normalized
            path = os.path.join(self._path, name, '.parquet')

            if self._format == 'parquet':
                raise Exception('File loaded is already in parquet format')

            self._dataframe.write.parquet(path)
            return path
        except Exception as ex:
            print(repr(ex))
            raise

