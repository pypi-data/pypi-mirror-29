# encoding: utf-8
from __future__ import absolute_import
from __future__ import print_function
import os


__version__ = "1.2.0"
app_dir = os.path.dirname(__file__)
app_dir_components = app_dir.split(os.sep)
base_dir = os.sep.join(app_dir_components[:-1])

from adobe_analytics.client import Client
from adobe_analytics.reports.report_definition import ReportDefinition
from adobe_analytics.classifications.classification_uploader import ClassificationUploader
