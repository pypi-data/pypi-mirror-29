from werkzeug import security
import os.path


def load_secret(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.readline()
    else:
        print "Generating salt"
        salt = security.gen_salt(60)
        with open(path, 'w') as f:
            f.write(salt)
        return salt