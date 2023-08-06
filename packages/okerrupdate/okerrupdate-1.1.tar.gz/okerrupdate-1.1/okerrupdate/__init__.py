import time
import requests
import logging
import re

from future.standard_library import install_aliases
install_aliases()
from urllib.parse import urlparse, urljoin


class OkerrExc(Exception):
    pass

class OkerrIndicator:
    def __init__(self, name, project, secret=None, method=None, policy=None, tags=None, error=None, origkeypath=None, keypath=None):
    
        if not isinstance(project, OkerrProject):
            project = OkerrProject(project)
            
        self.name = name
        self.project = project
        self.secret = secret
        self.method = method
        self.policy = policy
        self.tags = tags
        self.error = error
        self.origkeypath = origkeypath
        self.keypath = keypath

    def update(self, status, details=None):
        return self.project.update(self.name, status = status, details = details, secret = self.secret, method = self.method, 
            policy = self.policy, tags = self.tags, error = self.error, origkeypath = self.origkeypath, keypath = self.keypath)
        
    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


class OkerrProject:
    
    url = None # base url, for director
    project_url = None
    
    def __init__(self, textid=None, url=None, dry_run=False, secret=None):
        logging.basicConfig()
        self.textid = textid
        self.url = url
        self.dry_run = dry_run
        self.log  = logging.getLogger()
        self.secret = secret
        self.x = dict()
        if url:
            self.url = url
        else:
            self.url = 'https://cp.okerr.com/' 


    def setloglevel(self,lvl):
        print "okerrproject setloglevel", lvl
        self.log.setLevel(lvl)
        self.log.debug('set loglevel {}'.format(lvl))
        
    def verbose(self):
        self.setloglevel(logging.DEBUG)

    def setlog(self, log):
        self.log = log

    def indicator(self, name, secret=None, method=None, policy=None, tags=None, error=None, origkeypath=None, keypath=None):
        
        if secret is None:
            secret = self.secret
        
        i = OkerrIndicator(name, self, secret = secret, method = method, policy = policy, 
            tags = tags, error = error, origkeypath = origkeypath, keypath = keypath)
        return i

    def update(self,name, status, details=None, secret=None,
        method=None, policy='Default', tags=None, error=None, origkeypath=None, keypath=None):
        if self.dry_run:
            self.log.debug('Do NOT update: dry run. {} = {}'.format(name, repr(status)))            
            return
        
        textid = self.textid
        tags = tags or list()
        secret = secret or self.secret
        
        if not textid:
            self.log.error('Do not update: no textid')
            return
        
        # fix name
        if name.startswith(':') and self.prefix is not None:
            name = self.prefix+name

        r = None                
        
        url = self.geturl()

        if not url:
            self.log.error("cannot update, url not given!")
            raise OkerrExc('cannot update, url not given')
            return

        if not url.endswith('/'):
            url+='/'
            
        url = url+'update'
        
        self.log.debug(u"update: {}:{} = {} ({}) url: {}".format(self.textid,name,status,details, url))

        
        if keypath is None:
            keypath=''
            
        if origkeypath is None:
            origkeypath=''


        payload={
            'textid': textid, 
            'name':name, 
            'status': str(status), 
            'details': details, 
            'secret': secret, 
            'method': method,
            'policy': policy, 
            'tags': ','.join(tags),
            'error': error,
            'keypath': keypath, 
            'origkeypath': origkeypath}

        # process x
        for k, v in self.x.items():
            xname = "x_" + k
            payload[xname] = v

        if self.secret:
            secretlog="[secret]"
        else:
            secretlog="[nosecret]"
        start = time.time()
        
        
        preview = str(status)
        
        preview = re.sub('[\r\n]'," ", preview)
        
        if len(str(preview))>40:
            preview = str(preview)[:38]+".."
        else:
            preview = str(preview)
            
        
        stop = False
        success = False
        
        try:
            r = requests.post(url, data=payload, timeout=5)
            if r.status_code == 200:
                stop = True
                success = True
                self.log.info(u'okerr updated {} = {}'.\
                    format(name,preview))
            else:

                self.log.error(u'okerr update error ({}) textid:{}, {}={} {}'.\
                    format(r.status_code,self.textid,name,preview,secretlog))            
        
            self.log.debug(u'Request to URL {}:'.format(r.request.url))
            self.log.debug(r.request.body)
            
        except requests.exceptions.RequestException as e:
            raise OkerrExc(u'okerr exception {} textid:{}, {}={} {}'.\
                format(e,self.textid,name,status,secretlog))
                    
            
     
        if r:
            self.log.debug(r.content)
        else:
            self.log.debug("no reply, check log")
        self.log.debug("took {} sec.".format(time.time() - start))
    
        return success


    def __repr__(self):
        if self.secret:
            out = '{} [secret]'.format(self.textid)
        else:
            out = '{}'.format(self.textid)
        return out
        
    def __unicode__(self):
        return self.textid        
    
    def geturl(self):
        if self.project_url is None or (time.time() - self.url_received) > 300:
            durl = urljoin(self.url,'/api/director/{}'.format(self.textid))
            try:
                r = requests.get(durl, timeout=5)
            except requests.exceptions.RequestException as e:
                self.log.error("ERROR! geturl connection error: {}".format(e))
                self.project_url = None
                self.url_received = 0
                return None                        
            if r.status_code != 200:
                self.log.error("ERROR! status code: {} for dURL {}".format(r.status_code, durl))
                return None

            self.log.debug("got url {} from director {}".format(r.text.rstrip(), durl))
            self.project_url = r.text.rstrip()
            self.url_received = time.time()
        self.log.debug("geturl: return {}".format(self.project_url))
        return self.project_url
    
