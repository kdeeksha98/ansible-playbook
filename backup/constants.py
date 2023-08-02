Vizio_Upload_path = 'vizio/video_upload'
mp4_extension = '.mp4'
vizio_prefix = 'vizio_creatives'


class EventAttributes:
    LOADED = 'loaded'
    START = 'start'
    FIRST_QUARTILE = 'firstQuartile'
    MIDPOINT = 'midpoint'
    THIRD_QUARTILE = 'thirdQuartile'
    COMPLETE = 'complete'
    PROGRESS = 'progress'
    CLOSE_LINEAR = 'closeLinear'


class ElasticURL:
    url = "http://54.202.179.131:9200/fluentd-k8s/_search"

