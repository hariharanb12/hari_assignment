from elasticsearch import Elasticsearch, exceptions

class ESHelper():

    @staticmethod
    def get_status():
        '''
        helper method to get values from Elasticsearch
        '''
        services = ["httpd", "rabbitmq-server", "postgresql-11"]
        es = Elasticsearch('eshost')
        app_status = {}
        for service_name in services:
            try:
                service_status = es.get(index=service_name, id=1)
            except exceptions.NotFoundError:
                app_status[service_name] = "UNAVAILABLE"
                continue
            except exceptions.ConnectionError:
                app_status[service_name] = "UNKNOWN"
                continue
            app_status[service_name] = service_status["_source"]["service_status"].rstrip("\n")
        return app_status

    @staticmethod
    def update_status(index, request_data):
        '''
        helper method to store values from Elasticsearch
        '''
        es = Elasticsearch('eshost')
        try:
            update_response = es.index(index=index, id=1, body=request_data)
        except exceptions.ConnectionError:
            return
        return update_response
