import os

def init(app):

    @app.route('/api')
    def api():
        return 'api working!'

    @app.route('/distro_name')
    def os_release():
        if os.path.isfile('/etc/os-release'):
            with open('/etc/issue') as f:
                return f.read().lower().split()[0]
        return 'Not found :- ('