import lxml.html
from urlparse import urlparse

class Page:
  def __init__(self, content, url):
    self.content = content
    self.url = url


  def getUrl(self):
    return self.url

  def getAllLinks(self, max=200):
    dom =  lxml.html.fromstring(self.content)
    links = []
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
      links.append(link)
    return links

  def getDomainLinks(self):
    links = self.getAllLinks()
    domainLinks = []
    domain = urlparse(self.url)[1]
    for link in links: # select the url in href for all a tags(links)
      parsedLink = urlparse(link)
      if(parsedLink[1] == '' or parsedLink[1] == domain): # No or same domain
        domainLinks.append(link)
    return domainLinks


  def getFiles(self, max=50):
    return

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
