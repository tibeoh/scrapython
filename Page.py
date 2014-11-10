import lxml.html
from urlparse import urlparse

class Page:
  def __init__(self, content, url):
    self.content = content
    self.url = url


  def getUrl(self):
    return self.url

  def getFilename(self, defaultFilename='index.html'):
    splittedPath = urlparse(self.url).path.split('/')
    if(splittedPath[len(splittedPath)-1] != ''):
      return splittedPath[len(splittedPath)-1]
    else:
      return defaultFilename

  def getDomain(self):
    return urlparse(self.url)[1]

  def getLinkDomain(self, link):
    domain = self.getDomain()
    parsedLink = urlparse(link)
    if parsedLink[1] == '' or parsedLink[1] == domain:
      return domain
    else:
      return parsedLink[1]

  def getBaseUrl(self):
    return urlparse(self.url)[0] + '://' + urlparse(self.url)[1] + '/'


  def getAllLinks(self, max=200):
    dom =  lxml.html.fromstring(self.content)
    links = []
    for link in dom.xpath('//a/@href'): # select the url in href for all a   tags(links)
      links.append(link)
    return links

  def getDomainLinks(self):
    links = self.getAllLinks()
    domainLinks = []
    domain = self.getDomain()
    for link in links: # select the url in href for all a tags(links)
      parsedLink = urlparse(link)
      if(parsedLink[1] == '' or parsedLink[1] == domain): # No or same domain
        domainLinks.append(link)
    return domainLinks


  def getFiles(self, max=50):

    dom =  lxml.html.fromstring(self.content)
    links = []
    for link in dom.xpath('//link/@href'): # select the url in href for all link tags
        if self.getLinkDomain(link) == self.getDomain():
            links.append(link)
    for link in dom.xpath('//script/@src'): # select the url in href for all script tags
        if self.getLinkDomain(link) == self.getDomain():
            links.append(link)
    for link in dom.xpath('//img/@src'): # select the url in href for all img tags
        if self.getLinkDomain(link) == self.getDomain():
            links.append(link)
    return links

class Test:
  def __init__(self, content, name, path):
    self.content = content
    self.name = name
    self.path = path


  def getUrl(self):
    return self.path + self.name

  def getDomainLinks(self, max=200):
    return

  def getFiles(self, max=50):
    return
