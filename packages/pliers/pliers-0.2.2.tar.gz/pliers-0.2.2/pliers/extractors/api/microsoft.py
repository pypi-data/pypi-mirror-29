'''
Extractors that interact with Microsoft Azure Cognitive Services API.
'''

from pliers.extractors.base import ExtractorResult
from pliers.extractors.image import ImageExtractor
from pliers.transformers import (MicrosoftAPITransformer,
                                 MicrosoftVisionAPITransformer)

import pandas as pd


class MicrosoftAPIFaceExtractor(MicrosoftAPITransformer, ImageExtractor):
    ''' Extracts face features (location, emotion, accessories, etc.). From an
    image using the Microsoft Azure Cognitive Services API.

    Args:
        face_id (bool): return faceIds of the detected faces or not. The
            default value is False.
        landmarks (str): return face landmarks of the detected faces or
            not. The default value is False.
        attributes (list): one or more specified face attributes as strings.
            Supported face attributes include accessories, age, blur, emotion,
            exposure, facialHair, gender, glasses, hair, headPose, makeup,
            noise, occlusion, and smile. Note that each attribute has
            additional computational and time cost.
    '''

    api_name = 'face'
    api_method = 'detect'
    _env_keys = 'MICROSOFT_FACE_SUBSCRIPTION_KEY'
    _log_attributes = ('api_version', 'face_id', 'rectangle', 'landmarks',
                       'attributes')

    def __init__(self, face_id=False, rectangle=True, landmarks=False,
                 attributes=None, **kwargs):
        self.face_id = face_id
        self.rectangle = rectangle
        self.landmarks = landmarks
        self.attributes = attributes
        super(MicrosoftAPIFaceExtractor, self).__init__(**kwargs)

    def _extract(self, stim):
        if self.attributes:
            attributes = ','.join(self.attributes)
        else:
            attributes = ''

        params = {
            'returnFaceId': self.face_id,
            'returnFaceLandmarks': self.landmarks,
            'returnFaceAttributes': attributes
        }
        raw = self._query_api(stim, params)
        return ExtractorResult(raw, stim, self)

    def _parse_response_json(self, json):
        data_dict = {}
        for k, v in json.items():
            if k == 'faceRectangle' and not self.rectangle:
                continue
            if k == 'faceAttributes':
                k = 'face'
            if isinstance(v, dict):
                subdata = self._parse_response_json(v)
                for sk, sv in subdata.items():
                    data_dict['%s_%s' % (k, sk)] = sv
            elif isinstance(v, list):
                # Hard coded to this extractor
                for attr in v:
                    if k == 'hairColor':
                        key = attr['color']
                    elif k == 'accessories':
                        key = '%s_%s' % (k, attr['type'])
                    else:
                        continue
                    data_dict[key] = attr['confidence']
            else:
                data_dict[k] = v
        return data_dict

    def _to_df(self, result):
        face_results = []
        for i, face in enumerate(result._data):
            face_data = self._parse_response_json(face)
            face_results.append(face_data)

        return pd.DataFrame(face_results)


class MicrosoftAPIFaceEmotionExtractor(MicrosoftAPIFaceExtractor):

    ''' Extracts facial emotions from images using the Microsoft API '''

    def __init__(self, face_id=False, rectangle=False, landmarks=False,
                 **kwargs):
        super(MicrosoftAPIFaceEmotionExtractor, self).__init__(face_id,
                                                               rectangle,
                                                               landmarks,
                                                               ['emotion'],
                                                               **kwargs)


class MicrosoftVisionAPIExtractor(MicrosoftVisionAPITransformer,
                                  ImageExtractor):
    ''' Base MicrosoftVisionAPIExtractor class.

    Args:
        features (list): one or more specified vision features as strings.
            Supported vision features include Tags, Categories, ImageType,
            Color, and Adult. Note that each attribute has additional
            computational and time cost. By default extracts all visual
            features from an image.
    '''

    api_method = 'analyze'
    _log_attributes = ('api_version', 'features')

    def __init__(self, features=None, subscription_key=None, location=None,
                 api_version='v1.0'):
        self.features = features if features else ['Tags', 'Categories',
                                                   'ImageType', 'Color',
                                                   'Adult']
        super(MicrosoftVisionAPIExtractor, self).__init__(subscription_key=None,
                                                          location=None,
                                                          api_version='v1.0')

    def _extract(self, stim):
        params = {
            'visualFeatures': ','.join(self.features),
        }
        raw = self._query_api(stim, params)
        return ExtractorResult(raw, stim, self)

    def _to_df(self, result):
        data_dict = {}
        for feat in self.features:
            feat = feat[0].lower() + feat[1:]
            if feat == 'tags':
                for tag in result._data[feat]:
                    data_dict[tag['name']] = tag['confidence']
            elif feat == 'categories':
                for cat in result._data[feat]:
                    data_dict[cat['name']] = cat['score']
            else:
                data_dict.update(result._data[feat])
        return pd.DataFrame([data_dict.values()], columns=data_dict.keys())


class MicrosoftVisionAPITagExtractor(MicrosoftVisionAPIExtractor):

    ''' Extracts image tags using the Microsoft API '''

    def __init__(self, subscription_key=None, location=None, api_version='v1.0'):
        super(MicrosoftVisionAPITagExtractor, self).__init__(features=['Tags'],
                                                             subscription_key=None,
                                                             location=None,
                                                             api_version='v1.0')


class MicrosoftVisionAPICategoryExtractor(MicrosoftVisionAPIExtractor):

    ''' Extracts image categories using the Microsoft API '''

    def __init__(self, subscription_key=None, location=None, api_version='v1.0'):
        super(MicrosoftVisionAPICategoryExtractor, self).__init__(features=['Categories'],
                                                                  subscription_key=None,
                                                                  location=None,
                                                                  api_version='v1.0')


class MicrosoftVisionAPIImageTypeExtractor(MicrosoftVisionAPIExtractor):

    ''' Extracts image types (clipart, etc.) using the Microsoft API '''

    def __init__(self, subscription_key=None, location=None, api_version='v1.0'):
        super(MicrosoftVisionAPIImageTypeExtractor, self).__init__(features=['ImageType'],
                                                                   subscription_key=None,
                                                                   location=None,
                                                                   api_version='v1.0')


class MicrosoftVisionAPIColorExtractor(MicrosoftVisionAPIExtractor):

    ''' Extracts image color attributes using the Microsoft API '''

    def __init__(self, subscription_key=None, location=None, api_version='v1.0'):
        super(MicrosoftVisionAPIColorExtractor, self).__init__(features=['Color'],
                                                               subscription_key=None,
                                                               location=None,
                                                               api_version='v1.0')


class MicrosoftVisionAPIAdultExtractor(MicrosoftVisionAPIExtractor):

    ''' Extracts the presence of adult content using the Microsoft API '''

    def __init__(self, subscription_key=None, location=None, api_version='v1.0'):
        super(MicrosoftVisionAPIAdultExtractor, self).__init__(features=['Adult'],
                                                               subscription_key=None,
                                                               location=None,
                                                               api_version='v1.0')
