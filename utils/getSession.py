import web

def getSession(app):
	# Hack to make session play nice with the reloader (in debug mode)
	if web.config.get('_session') is None:
	    session = web.session.Session(app, web.session.DiskStore('sessions'))
	    web.config._session = session
	else:
	    session = web.config._session

	return session