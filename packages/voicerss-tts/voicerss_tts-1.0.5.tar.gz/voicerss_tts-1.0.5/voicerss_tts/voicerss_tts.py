import os
import datetime
import requests
import logging_helper
from fdutil.safe import file_safe
from cachingutil import (BinaryFileCache,
                         CacheError)

logging = logging_helper.setup_logging()

CATALAN               = u'ca-es'
CHINESE_CHINA         = u'zh-cn'
CHINESE_HONG_KONG     = u'zh-hk'
CHINESE_TAIWAN        = u'zh-tw'
DANISH                = u'da-dk'
DUTCH                 = u'nl-nl'
ENGLISH_AUSTRALIA     = u'en-au'
ENGLISH_CANADA        = u'en-ca'
ENGLISH_GREAT_BRITAIN = u'en-gb'
ENGLISH_INDIA         = u'en-in'
ENGLISH_UNITED_STATES = u'en-us'
FINNISH               = u'fi-fi'
FRENCH_CANADA         = u'fr-ca'
FRENCH_FRANCE         = u'fr-fr'
GERMAN                = u'de-de'
ITALIAN               = u'it-it'
JAPANESE              = u'ja-jp'
KOREAM                = u'ko-kr'
NORWEGIAN             = u'nb-no'
POLISH                = u'pl-pl'
PORTUGESE_BRAZIL      = u'pt-br'
PORTUGESE_PORTUGAL    = u'pt-pt'
RUSSIAN               = u'ru-ru'
SPANISH_MEXICO        = u'es-mx'
SPANISH_SPAIN         = u'es-es'
SWEDISH               = u'sv-se'

MP3 = u'MP3'
WAV = u'WAV'
AAC = u'AAC'
OGG = u'OGG'
CAF = u'CAF'

MONO_8KHZ_8BIT       = u'8khz_8bit_mono'
STEREO_8KHZ_8BIT     = u'8khz_8bit_stereo'
MONO_8KHZ_16BIT      = u'8khz_16bit_mono'
STEREO_8KHZ_16BIT    = u'8khz_16bit_stereo'
MONO_11KHZ_8BIT      = u'11khz_8bit_mono'
STEREO_11KHZ_8BIT    = u'11khz_8bit_stereo'
MONO_11KHZ_16BIT     = u'11khz_16bit_mono'
STEREO_11KHZ_16BIT   = u'11khz_16bit_stereo'
MONO_12KHZ_8BIT      = u'12khz_8bit_mono'
STEREO_12KHZ_8BIT    = u'12khz_8bit_stereo'
MONO_12KHZ_16BIT     = u'12khz_16bit_mono'
STEREO_12KHZ_16BIT   = u'12khz_16bit_stereo'
MONO_16KHZ_8BIT      = u'16khz_8bit_mono'
STEREO_16KHZ_8BIT    = u'16khz_8bit_stereo'
MONO_16KHZ_16BIT     = u'16khz_16bit_mono'
STEREO_16KHZ_16BIT   = u'16khz_16bit_stereo'
MONO_22KHZ_8BIT      = u'22khz_8bit_mono'
STEREO_22KHZ_8BIT    = u'22khz_8bit_stereo'
MONO_22KHZ_16BIT     = u'22khz_16bit_mono'
STEREO_22KHZ_16BIT   = u'22khz_16bit_stereo'
MONO_24KHZ_8BIT      = u'24khz_8bit_mono'
STEREO_24KHZ_8BIT    = u'24khz_8bit_stereo'
MONO_24KHZ_16BIT     = u'24khz_16bit_mono'
STEREO_24KHZ_16BIT   = u'24khz_16bit_stereo'
MONO_32KHZ_8BIT      = u'32khz_8bit_mono'
STEREO_32KHZ_8BIT    = u'32khz_8bit_stereo'
MONO_32KHZ_16BIT     = u'32khz_16bit_mono'
STEREO_32KHZ_16BIT   = u'32khz_16bit_stereo'
MONO_44KHZ_8BIT      = u'44khz_8bit_mono'
STEREO_44KHZ_8BIT    = u'44khz_8bit_stereo'
MONO_44KHZ_16BIT     = u'44khz_16bit_mono'
STEREO_44KHZ_16BIT   = u'44khz_16bit_stereo'
MONO_48KHZ_8BIT      = u'48khz_8bit_mono'
STEREO_48KHZ_8BIT    = u'48khz_8bit_stereo'
MONO_48KHZ_16BIT     = u'48khz_16bit_mono'
STEREO_48KHZ_16BIT   = u'48khz_16bit_stereo'
ALAW_8KHZ_MONO       = u'alaw_8khz_mono'
ALAW_8KHZ_STEREO     = u'alaw_8khz_stereo'
ALAW_11KHZ_MONO      = u'alaw_11khz_mono'
ALAW_11KHZ_STEREO    = u'alaw_11khz_stereo'
ALAW_22KHZ_MONO      = u'alaw_22khz_mono'
ALAW_22KHZ_STEREO    = u'alaw_22khz_stereo'
ALAW_44KHZ_MONO      = u'alaw_44khz_mono'
ALAW_44KHZ_STEREO    = u'alaw_44khz_stereo'
ULAW_MONO_8KHZ_MONO  = u'law_mono_8khz_mono'
ULAW_8KHZ_STEREO     = u'law_8khz_stereo'
ULAW_MONO_11KHZ_MONO = u'law_mono_11khz_mono'
ULAW_11KHZ_STEREO    = u'law_11khz_stereo'
ULAW_MONO_22KHZ_MONO = u'law_mono_22khz_mono'
ULAW_22KHZ_STEREO    = u'law_22khz_stereo'
ULAW_MONO_44KHZ_MONO = u'law_mono_44khz_mono'
ULAW_44KHZ_STEREO    = u'law_44khz_stereo'

REQUEST_LIMIT_EXCEEDED             = (u'The subscription is expired or '
                                      u'requests count limitation is exceeded!')
REQUEST_CONTENT_TOO_LONG           = u'The request content length is too large!'
UNSUPPORTED_LANGUAGE               = u'The language does not support!'
LANGUAGE_NOT_SPECIFIED             = u'The language is not specified!'
TEXT_NOT_SPECIFIED                 = u'The text is not specified!'
API_KEY_NOT_AVAILABLE              = u'The API key is not available!'
API_KEY_NOT_SPECIFIED              = u'The API key is not specified!'
SUBSCRIPTION_DOES_NOT_SUPPORT_SSML = u'The subscription does not support SSML!'


class VoiceError(Exception):
    pass


def start_of_day():
    sod = datetime.datetime.combine(datetime.date.today(),
                                    datetime.datetime.min.time())
    return (sod - datetime.datetime(1970, 1, 1)).total_seconds()


class TextToSpeech(object):
    HEADERS = {
        u'Content-Type': u'application/x-www-form-urlencoded; charset=UTF-8'}
    URL = u'api.voicerss.org'

    def __init__(self,
                 api_key,
                 text,
                 language,
                 rate=None,
                 codec=None,
                 audio_format=None,
                 ssml=None,
                 base64=None,
                 ssl=None):

        self.api_key = api_key
        self.text = text
        self.language = language
        self.rate = rate
        self.codec = codec
        self.audio_format = audio_format
        self.ssml = ssml
        self.base64 = base64
        self.ssl = ssl

        protocol = u'https' if self.ssl else u'http'
        self.url = u'{protocol}://{url}'.format(protocol=protocol,
                                                url=self.URL)

        self.params = {u'key': self.api_key,
                       u'hl': self.language,
                       u'src': self.text
                       }

        self.__check_mandatory_parameters()

        # Add optional parameters.
        self.params.update({key: unicode(value).lower()
                            for key, value in {u'r': self.rate,
                                               u'c': self.codec,
                                               u'f': self.audio_format,
                                               u'ssml': self.ssml,
                                               u'b64': self.base64}.iteritems()
                            if value is not None})

        self.__request()

    def __check_mandatory_parameters(self):
        for key, value in self.params.iteritems():
            if not value:
                raise RuntimeError(u'The parameter "{key}" is undefined'
                                   .format(key = key))

    def __request(self):
        self.response = requests.get(url=self.url,
                                     params=self.params,
                                     headers=self.HEADERS)

    def check_error(self):
        if self.response.status_code == 200:
            try:
                if self.response.content.startswith(u'ERROR:'):
                    raise VoiceError(self.response.content)
            except UnicodeDecodeError:
                pass
        else:
            raise VoiceError(u'Status code:{status_code} for "{url}"'
                             .format(status_code=self.response.status_code,
                                     url=self.url))

    @property
    def subscription_limit_reached(self):
        try:
            self.check_error()
        except VoiceError as ve:
            if REQUEST_LIMIT_EXCEEDED in ve.message:
                return True
        return False

    @property
    def speech(self):
        self.check_error()
        return self.response.content

    def save(self,
             filepath):
        logging.debug(u'Writing "{text}" to ')
        with open(filepath, mode=u'wb') as f:
            f.write(self.speech)

    def play(self):
        print([ord(c) for c in self.speech])
        # TODO: figure out how to play the sound in a multiplatform manner


class TextToSpeechCache(BinaryFileCache):

    def __init__(self,
                 folder,
                 api_key,
                 language,
                 rate=None,
                 codec=None,
                 audio_format=None,
                 ssml=None,
                 base64=None,
                 ssl=None,
                 api_request_limit=300):

        self.folder = folder
        self.api_key = api_key
        self.api_request_limit = api_request_limit
        self.language = language
        self.rate = rate
        self.codec = codec
        self.audio_format = audio_format
        self.ssml = ssml
        self.base64 = base64
        self.ssl = ssl

        super(TextToSpeechCache, self).__init__(folder=folder)

    def key(self,
            text,
            **params):
        return text

    def filename(self,
                 key):
        filename = file_safe(key.strip().lower())
        filename = u'{filename}.{ext}'.format(filename=filename,
                                              ext=self.codec.lower())
        return os.path.join(self.folder, self.language, filename)

    @property
    def requests_remaining(self):

        sod = start_of_day()

        files = [os.path.join(self.folder, f)
                 for f in os.listdir(self.folder)]

        todays_request_count = len([f
                                    for f in files
                                    if os.path.getctime(f) > sod])

        remaining = self.api_request_limit - todays_request_count

        logging.debug(u'VOICETSS requests remaining today: {remaining}'
                      .format(remaining=remaining))

        return remaining

    def _create_dummy_files(self,
                            requests_remaining = None):
        u"""
        Creates enough dummy files so that
        further requests aren't made when
        the daily limit has been exceeded.

        :param requests_remaining: I
        """
        requests_remaining = (self.requests_remaining
                              if requests_remaining is None
                              else requests_remaining)

        filenames = [self.filename(text=(u'exceeded_api_limit_dummy_file_{i}'
                                         .format(i=i)))
                     for i in xrange(requests_remaining)]

        for filename in filenames:
            with open(filename, u'w') as f:
                f.write(filename)

    def fetch_from_source(self,
                          text,
                          **params):
        tts = None
        requests_remaining = self.requests_remaining
        if requests_remaining:
            try:

                tts = TextToSpeech(api_key=self.api_key,
                                   text=text,
                                   language=self.language,
                                   codec=self.codec,
                                   audio_format=self.audio_format,
                                   ssl=self.ssl)
                return tts.speech

            except VoiceError as ve:
                if tts.subscription_limit_reached:
                    self._create_dummy_files(requests_remaining)
                raise CacheError(u'Could not fetch from source ({error})'
                                 .format(error = ve.message))
        else:
            raise CacheError(u'Could not fetch from source (ERROR: {error})'
                             .format(error = REQUEST_LIMIT_EXCEEDED))
