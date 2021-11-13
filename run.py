'''
main point of execution
'''
from flaskserver import app
from flaskserver.database import db_session

# execution
if __name__ == '__main__':
    app.run(debug=True)

# teardown


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
