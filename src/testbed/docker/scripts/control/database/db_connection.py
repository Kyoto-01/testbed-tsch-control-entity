from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client import WriteApi, DeleteApi, BucketsApi
from influxdb_client.rest import ApiException
from influxdb_client.client.write_api import SYNCHRONOUS


INFLUXDB_MAIN_PORT = 8086


class InfluxDBConnection:

    def __init__(
        self,
        configFile: 'str' = None
    ):
        self._configFile = configFile
        self._client: 'InfluxDBClient' = None
        self._writeApi: 'WriteApi' = None
        self._deleteApi: 'DeleteApi' = None
        self._bucketsApi: 'BucketsApi' = None

        self._setup()

    def _get_client(self):
        self._client = InfluxDBClient.from_config_file(self._configFile)
            
    def _test_client(self):
        self._test_client_config()
        self._test_client_connection()

    def _test_client_config(self):
        if self._client.org is None:
            raise KeyError("org")
        
    def _test_client_connection(self):
        try:
            self.insert('test', 'test')
            self._bucketsApi.delete_bucket(
                self._bucketsApi.find_bucket_by_name('test')
            )
        except ApiException as ae:
            if ae.status == 401:
                raise Exception("Unauthorized token")
        
    def _setup(self):
        self._get_client()
        self._setup_api()
        self._test_client()

    def _setup_api(self):
        self._writeApi = self._client.write_api(
            write_options=SYNCHRONOUS
        )

        self._deleteApi = self._client.delete_api()

        self._bucketsApi = self._client.buckets_api()

    def create_bucket(self, bucket_name: 'str'):
        ret = False

        if self._bucketsApi:
            try:
                self._bucketsApi.create_bucket(bucket_name=bucket_name)
                ret = True
            except ApiException as ae:
                if ae.status != 422:
                    raise

        return ret

    def insert(
        self,
        bucket: 'str',
        measurement: 'str',
        tags={},
        fields={}
    ):
        if self._writeApi:
            data = {
                'measurement': measurement,
                'tags': tags,
                'fields': fields,
                'time': datetime.utcnow()
            }

            self.create_bucket(bucket)

            self._writeApi.write(
                bucket=bucket,
                record=data
            )

    def remove(
        self,
        bucket: 'str',
        measurement='',
        predicate='',
        start='',
        end=''
    ):
        if self._bucketsApi.find_bucket_by_name(bucket):
            if not start:
                start = '1970-01-01T00:00:00Z'
            if not end:
                end = datetime.utcnow()

            if measurement:
                if predicate:
                    predicate = f'_measurement={measurement} and {predicate}'
                else:
                    predicate = f'_measurement={measurement}'

            self._deleteApi.delete(
                start=start,
                stop=end,
                predicate=predicate,
                bucket=bucket,
            )

    def close(self):
        self._writeApi.close()
        self._writeApi = None

        self._client.close()
        self._client = None
