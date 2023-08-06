import re

def valip(data):
    match = re.search('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9])$',data)
    return match


def alph(data):
    if str(str(data).replace(' ','').replace('-','').replace('_','').replace('.','').replace(':','')).isalnum():
        return True
    else:
        return False


def aplhnum(data):
    if str(str(data).replace(' ','')).isalnum():
	return True
    else:
	return False


def api(data):
    if type(data) == str:
	if data.count('-') ==4:
	    if aplhnum(data.split('-')[0]) and aplhnum(data.split('-')[1]) and aplhnum(data.split('-')[2]) and aplhnum(data.split('-')[3]):
		return True
	    else:
		return False
        else:
	    return False
    else:
	return False


def version(data):
    if type(data) == float or type(str(data.replace('.',''))) ==int :
	return True
    else:
	return False


def jsontodict(data):
    dat=[]
    if type(data) == list:
	d={}
        for val in data:
            for k,v in val.iteritems():
                d[k]=v
        dat.append(d)

    elif type(data) ==dict:
        d={}
        for k,v in data.iteritems():
            d[str(k)]=v
        dat.append(d)

    dat=eval(str(data))
    return dat




def dix(data):
    d={}
    for k,v in data.iteritems():
        if k == 'project' and alph(v) or k == 'classification' and alph(v)  or k == 'test' and alph(v) or k == 'source' and alph(v):
	    d[k]=v

        elif k == 'version' and version(v):
            d[k]=v

	else:
            d[k]=v

    return d



