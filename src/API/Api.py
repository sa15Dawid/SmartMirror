from bottle import run, get, post, request, delete

windows = [{'type' : 'Site', 'name' : 'Main'}]

@get('/window')
def getAll():
	return {'windows' : windows}

@get('/window/<type>')
def getOne(type):
	the_window = [window for window in windows if window['type'] == type]
	return {'window' : the_window[0]}

@post('/window')
def addOne():
	new_window = {'type' : request.json.get('type'), 'name' : request.json.get('name')}
	windows.append(new_window)
	return {'windows' : windows}

@delete('/window/<type>')
def removeOne(type):
	the_window = [window for window in windows if window['type'] == type]
	windows.remove(the_window[0])
	return {'windows' : windows}

run(host='localhost', port=5000)
