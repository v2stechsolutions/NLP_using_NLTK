#!/usr/bin/env python

from app import app

#app.run()
app.run(host='0.0.0.0',port=5024,debug=True,threaded=True)
#app.run(threaded=True)
