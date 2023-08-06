# coding=utf-8
# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.

from __future__ import absolute_import


jvm_third_party_map = {
  'airlift': 'slice',
  'akka': 'akka',
  'backtype': {
    'storm': 'storm-core',
  },
  'breeze': 'breeze',
  'caffe': 'caffe-protobuf',
  'ch': {
    'qos': {
      'logback': 'logback',
    },
  },
  'cascading': 'cascading',
  'cc': {
    'factorie': 'factorie',
  },
  'com': {
    'amazon': {
      'speech': 'alexa-skills-kit',
      'emr': 'amazon-emr-kinesis'
    },
    'amazonaws': 'amazonaws',
    'apporiented': {
      'algorithm': {
        'clustering': 'hierarchical-clustering'
      }
    },
    'beeswax': 'beeswax-api',
    'clearspring': {
      'analytics': {
        'stream': 'stream-lib',
       }
    },
    'bettercloud': {
      'vault': 'vault-java-driver',
    },
    'codahale': {
      'jerkson': 'jerkson',
    },
    'carrotsearch': 'langid-java',
    'cybozu': {
      'labs': 'language-detect',
    },
    'drew': 'metadata-extractor',
    'esotericsoftware': {
      'kryo': 'kryo',
    },
    'esri': {
      'core': 'esri-geometry-api',
      'hadoop': 'spatial-sdk-hive'
    },
    'facebook': {
      'presto': {
        'DEFAULT': 'presto-main',
        'jdbc': {
          'DEFAULT': 'presto-jdbc',
          'internal': 'presto-main',
        }
      }
    },
    'fasterxml': {
      'jackson': 'jackson-scala',
    },
    'foursquare': {
      'caffe': 'caffe-jni',
      'common': {
        'async': 'twitter-util-async',
      },
      'datafiles': {
        'DEFAULT': 'geotouches'
      },
      'es231': 'elasticsearch-231',
      'esh230': 'elasticsearch-hadoop-mr-230',
      'geo': {
        'quadtree': 'country-revgeo',
        'shapefile': {
          'cbsa': {
            'CbsaByNameShapefile': 'cbsa-name-shapefiles',
            'CbsaByIdShapefile': 'cbsa-id-shapefiles',
          },
          'continent': 'continent-shapefiles',
          'country': 'cc-shapefiles',
          'dma': {
            'DmaByNameShapefile': 'dma-name-shapefiles',
            'DmaByIDShapefile': 'dma-id-shapefiles',
          },
          'metro': 'metro-shapefiles',
          'state': 'state-shapefiles',
          'timezone': 'tz-shapefiles',
          'zcta': 'zcta-shapefiles',
          'caprovince': 'ca-provinces-shapefiles',
        },
      },
      'jedis281': {
          'redis': {
              'clients': 'jedis281',
          },
      },
      'kafka1': 'kafka1-clients',
      'kafka9': 'kafka9-clients',
      'kafka10': 'kafka10-clients',
      'lucene550': 'lucene-550'
    },
    'github': {
      'fakemongo': 'fongo',
      'mustachejava': 'mustache-java'
    },
    'google': {
      'api': {
        'client': {
          'googleapis': {
            'auth': {
              'oauth2': 'libmirror'
            },
            'batch': {
              'json': 'libmirror'
            },
            'javanet': 'gdata',
            'json': 'libmirror'
          },
          'auth': {
            'oauth2': 'gdata'  # note(stefano): this probably shouldn't be in gdata
          },
          'http': 'libmirror',
          'json': 'libmirror',
          'util': 'gdata'
        },
        'services': {
          'drive': 'gdata',
          'mirror': 'libmirror'
        }
      },
      'caliper': 'caliper',
      'closure': {
        'compiler': 'closure-compiler',
        'templates': 'closure-templates',
      },
      'common': {
        'annotations': 'guava',
        'base': 'guava',
        'cache': 'guava',
        'collect': 'guava',
        'geometry': 's2',
        'hash': 'guava',
        'io': 'guava',
        'primitives': 'guava',
        'util': 'guava',
      },
      'gdata': 'gdata',
      'gson': 'gson',
      'i18n': {
        'phonenumbers': {
          'geocoding': 'phonenumbers-geocoder',
          'DEFAULT': 'phonenumbers'
        }
      },
      'inject': 'guice',
      'javascript': 'closure',
      'protobuf': 'protobuf-java',
      'template': 'closure-templates',
      'zxing': 'zxing',
    },
    'googlecode': {
        'concurrentlinkedhashmap': 'concurrentlinkedhashmap'
    },
    'ibm': {
      'icu': 'icu4j',
    },
    'infochimps': {
      'elasticsearch': 'wonderdog'
    },
    'jcraft': 'jsch',
    'jayway': {
      'restassured': 'restassured'
    },
    'mapzen': {
      'jpostal': 'jpostal',
    },
    'maxmind': 'geoip',
    'mongodb': {
      'DEFAULT': 'mongodb-drivers',
    },
    'mchange': {
      'v2': {
        'c3p0': 'c3p0'
      }
    },
    'mysql': 'mysql',
    'opencsv': 'opencsv',
    'relayrides': {
      'pushy': 'pushy',
    },
    'rockymadden': 'rockymadden',
    'thoughtworks': 'SKIP',
    'sun': {
      'jna': 'jna',
      'net': {
        'httpserver': 'SKIP',
      },
    },
    'thimbleware': {
      'jmemcached': 'jmemcached-daemon',
    },
    'twitter': {
      'algebird': 'algebird',
      'bijection': 'bijection',
      'chill': 'chill',
      'common': 'zookeeper-lock',
      'concurrent': 'twitter-util',
      'conversions': 'twitter-util',
      'elephantbird': 'elephant-bird',
      'finagle': {
        'httpx': {
          'HttpToHttpxAdaptor': None,
          'DEFAULT': 'finagle',
        },
        'memcached': {
          'NoReplicationClient': None,
          'DEFAULT': 'finagle',
        },
        'DEFAULT': 'finagle',
      },
      'hashing': 'twitter-util',
      'io': 'twitter-util',
      'json': 'twitter-json',
      'logging': 'twitter-util',
      'ostrich': 'ostrich',
      'parrot': 'iago',
      'penguin': 'korean-text',
      'scalding': {
        'platform': 'scalding-hadoop-test',
        'DEFAULT': 'scalding',
      },
      'thrift': {
        'ServiceInstance': 'zookeeper-lock',
      },
      'util': 'twitter-util',
      'zookeeper': 'zookeeper-client',
    },
    'typesafe': {
      'config': 'typesafe-config',
    },
    'vividsolutions': {
      'jts': 'jts',
    },
    'wcohen': {
      'ss': 'secondstring',
    },
  },
  'datafu': 'datafu',
  'de': {
    'bwaldvogel': {
      'liblinear': 'liblinear',
    },
    'javakaffee': {
      'kryoserializers': 'kryo-serializers',
    },
    'lmu': {
      'ifi': {
        'dbs': {
          'elki': 'elki',
        },
      },
    },
    'micromata': {
      'opengis': 'JavaAPIforKml'
    },
    'undercouch': {
      'bson4jackson': 'bson4jackson'
    },
  },
  'difflib': 'java-diff-utils',
  'edu': {
    'upc': 'freeling',
  },
  'epic': 'epic',
  'gnu': {
    'trove': 'trove4j',
  },
  'gobblin': 'gobblin',
  'io': {
    'fabric8': {
      'kubernetes': {
        'client': 'kubernetes-client-java',
      },
    },
    'fsq': {
      'spindle': {
        '__shaded_for_spindle_bootstrap__': {
          'descriptors': {
            'java_thrift_descriptors': 'SKIP',
          },
        },
      },
    },
    'netty': 'netty4',
  },
  'java': 'SKIP',
  'javax': {
    'mail': 'mail',
    'DEFAULT': 'SKIP',  # NOTE(ryan): I can't find where this lives
  },
  'jskills': 'jskills',
  'kafka': {
    'api': 'kafka',
    'common': 'kafka',
    'consumer': 'kafka',
    'etl': 'kafka-hadoop-consumer',
    'message': 'kafka',
    'producer': 'kafka',
    'serializer': 'kafka',
    'utils': 'kafka',
  },
  'kr': {
    'ac': {
      'kaist': {
        'swrc': 'jhannanum_cprw',
      }
    }
  },
  'ml': {
    'dmlc': {
      'xgboost4j': 'xgboost4j',
    },
  },
  'net': {
    'jpountz': {
      'lz4': 'lz4',
    },
    'liftweb': {
      'actor': 'lift-actor',
      'builtin': 'lift-webkit',
      'common': 'lift-common',
      'db': 'lift-db',
      'http': 'lift-webkit',
      'json': 'lift-json',
      'mapper': 'lift-mapper',
      'mocks': 'liftweb-testkit',
      'mongodb': 'lift-mongo',
      'proto': 'lift-proto',
      'record': 'lift-record',
      'sitemap': 'lift-webkit',
      'util': 'lift-util',
    },
    'fortuna': {
      'ical4j': 'ical4j',
    },
    'sf': {
      'uadetector': 'uadetector'
    }
  },
  'nl': {
    'captcha': 'simplecaptcha',
  },
  'opennlp': 'opennlp',
  'org': {
    'apache': {
      'avro': 'avro',
      'axis2': 'axis2',
      'commons': {
        'cli': 'commons-cli',
        'codec': 'twitter-util',
        'compress': 'commons-compress',
        'fileupload': 'commons-fileupload',
        'httpclient': 'commons-httpclient',
        'io': 'commons-io',
        'lang': 'commons-lang',
        'lang3': 'commons-lang3',
        'math': 'commons-math',
        'math3': 'commons-math3',
        'net': 'commons-net',
        'validator': 'commons-validator',
      },
      'curator': {
        'DEFAULT': 'curator',
        'test': 'curator-test',
      },
      'hadoop': {
        # NOTE(ryan): org.apache.hadoop is a complicated soup of dependencies
        'conf': 'hadoop-common',
        'filecache': 'hadoop-mapreduce-client',
        'fs': 'hadoop-common',
        'hbase': {
          'io': {
            'hfile': {
              'DEFAULT': 'hbase',
              'hacks': None,
            },
          },
          'util': 'hbase',
        },
        'hdfs': 'hadoop-hdfs',
        'hive': {
          'DEFAULT': 'hive-exec',  # TODO(joe): this isn't the whole story
          'common': 'hive-common'
        },
        'http': 'hadoop-common',
        'io': 'hadoop-common',
        'mapred': 'hadoop-mapreduce-client',
        'mapreduce': {
          'DEFAULT': 'hadoop-mapreduce-client',
          'lib': {
            'DEFAULT': 'hadoop-mapreduce-client',
            'output': {
              'DEFAULT': 'hadoop-mapreduce-client',
              'NiceMultipleOutputs': None,
            },
          },
          'util': {
            'DEFAULT': 'hadoop-mapreduce-client',
            'HostUtil': None,
          },
        },
        'mrunit': 'mrunit',
        'security': 'hadoop-common',
        'util': 'hadoop-common',
      },
      'hive': {
        'jdbc': 'hive-jdbc',
        'service': 'hive-cli'
      },
      'hcatalog': 'hcatalog',
      'http': {
        'DEFAULT': 'apache-httpclient',
        'message': 'commons-httpclient',
        'client': 'commons-httpclient',
        'entity': 'commons-httpclient',
        'impl': {
          'DEFAULT': 'apache-httpclient',
        },
      },
      'lucene': {
        'DEFAULT': 'lucene-analyzers-common',
        'analysis': {
          'DEFAULT': 'lucene-analyzers-common',
          'cn': 'lucene-analyzers-smartcn',
          'ja': 'lucene-analyzers-kuromoji',
          'icu': 'lucene-analyzers-icu',
        },
      },
      'parquet': 'parquet',
      'sanselan': 'sanselan',
      'spark': 'spark',
      'thrift': 'thrift',
      'zookeeper': 'zookeeper',
    },
    'atilika': {
      'kuromoji': 'kuromoji',
    },
    'bson': 'bson',
    'bytedeco': 'tesseract-javacpp',
    'clapper': {
      'argot': 'argot',
      'classutil': 'classutil',
    },
    'codehaus': {
      'jackson': 'jackson',
    },
    'eclipse': {
      'jetty': {
        'server': 'jetty-server',
        'servlet': 'jetty-servlet',
      }
    },
    'elasticsearch': {
      'DEFAULT': 'elasticsearch',
      'hadoop': 'elasticsearch-hadoop-mr',
    },
    'fusesource': {
      'scalate': 'scalate',
    },
    'geonames': {
      'Admin1Cities': 'admin1cities',
      'NameTranslation': 'NameTranslation',
      'Cities15000': 'cities15000',
      'CountryInfo': 'countryinfo'
    },
    'geotools': {
      'geometry': 'gt-main',
      'geojson': 'gt-geojson',
      'DEFAULT': 'gt-shapefile'
    },
    'hamcrest': 'hamcrest-core',
    'I0Itec': {
      'zkclient': 'I0Itec-zkclient',
    },
    'jboss': {
      'netty': 'netty',
    },
    'jets3t': 'jets3t',
    'jh': 'sizer',
    'joda': {
      'time': 'joda-time',
    },
    'json4s': 'json4s',
    'jsoup': 'jsoup',
    'junit': 'junit',
    'mockito': 'mockito',
    'mortbay': {
      'jetty': 'jetty',
      'resource': 'jetty',
      'thread': 'jetty',
      'util': 'jetty-util',
    },
    'mozilla': {
      'javascript': 'rhino',
    },
    'objectweb': {
      'asm': 'asm'
    },
    'openjdk': {
      'jmh': 'jmh'
    },
    'openid4java': 'openid-client',

    'opencv': {
      'HaarCascadeFrontalFaceAlt': 'haarcascade_frontalface_alt',
      'DEFAULT': 'opencv'
    },
    'opengis': 'gt-shapefile',
    'openimaj': 'openimaj',
    'openstreetmap': {
      'osmosis': 'osmosis',
    },
    'pantsbuild': {
      'junit': 'junit-runner',
    },
    'parboiled': 'parboiled-scala',
    'postgresql': {
      'core': 'postgresql',
    },
    'reflections': 'reflections',
    'rocksdb': 'rocksdb',
    'scala_tools': {
      'time': 'scalaj-time',
    },
    'scalacheck': 'scalacheck',
    'scalatra': 'scalatra',
    'slf4j': 'slf4j-all',
    'slf4s': 'slf4s',
    'specs': 'specs',
    'specs2': 'specs2',
    'tartarus': {
      'snowball': 'lucene-analyzers-common',
    },
    'xerial': {
      'snappy': 'snappy-java',
    },
    'xml': 'SKIP',
  },
  'redis': {
    'clients': {
      'jedis': 'jedis',
    },
  },
  'scala': {
    'util': {
      'parsing': 'scala-parser-combinators',
      'DEFAULT': 'SKIP',
    },
    'reflect': 'scala-reflect',
    'xml': 'scala-xml',
    'DEFAULT': 'SKIP',
  },
  'scalaj': {
    'http': 'scalaj-http',
  },
  'scalax': 'scala-io',
  'scopt': 'scopt',
  'storm': {
    'kafka': 'storm-kafka',
  },
  'sun': {
    'reflect': 'SKIP',
    'misc': {
      'BASE64Decoder': 'SKIP',  # NOTE(ryan): I can't find where this lives
      'BASE64Encoder': 'SKIP',  # NOTE(ryan): I can't find where this lives
    },
  },
  'tools': {
    'nsc': 'scala-io',
  },
  'zemberek': 'zemberek',
}
