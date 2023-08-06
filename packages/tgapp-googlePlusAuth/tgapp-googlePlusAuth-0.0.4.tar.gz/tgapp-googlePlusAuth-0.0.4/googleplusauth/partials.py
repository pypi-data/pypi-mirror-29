from tg import expose

@expose('googleplusauth.templates.little_partial')
def something(name):
    return dict(name=name)