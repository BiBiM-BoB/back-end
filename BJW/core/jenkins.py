from jenkinsapi.jenkins import Jenkins


def get_server_instance(url, username, password):
    server = Jenkins(url, username=username, password=password)
    return server
