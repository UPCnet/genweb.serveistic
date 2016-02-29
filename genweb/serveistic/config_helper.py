import os
import ConfigParser
import csv

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def get_absolute_path(relative_path):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        relative_path)


def build_facets_vocabulary():
    facets_file_path = get_absolute_path(config.get('facets', 'file_path'))
    with open(facets_file_path, 'r') as facets_file:
        facets = set([
            row[0]
            for row in csv.reader(
                facets_file, delimiter=',', quotechar='"')])
    return SimpleVocabulary([
        SimpleTerm(
            title=facet.decode('utf-8'),
            value=facet.decode('utf-8'),
            token=index)
        for index, facet in enumerate(facets)])

config = ConfigParser.ConfigParser()
config.read(get_absolute_path('serveistic.cfg'))

facets_vocabulary = build_facets_vocabulary()
