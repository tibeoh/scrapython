import lxml.html, urllib2
from urlparse import urlparse
import logging

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

  def getLocalFilename():
   return urlparse(self.url).path.replace('/', '-')

  def getDestinationPath(self):
      return urlparse(self.url)[2][1:].replace('/', '-')

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
    try:
      for link in links:
        parsedLink = urlparse(link)
        # if link relatif
        if(parsedLink[1] == domain): # No or same domain
          if urllib2.urlopen(link).info()['Content-Type'].startswith('text/html'):
            domainLinks.append(link)
            logging.warning(link)

        if(parsedLink[1] == ''):
          if urllib2.urlopen(self.getBaseUrl() + link).info()['Content-Type'].startswith('text/html'):
            domainLinks.append(self.getBaseUrl() + link)
            logging.warning(self.getBaseUrl() + link)

        # if absolute
    except urllib2.URLError:
        # The URL is valid but the page is not accessible (network or server error etc.)
        logging.warning('The link ' + link + ' is not accessible.')
    return domainLinks


  def getFilesLinks(self, deelLevel, detinationPath='', max=50):

    dom =  lxml.html.fromstring(self.content)
    links = []
    if(deelLevel > 0):
      for link in dom.xpath('//a/@href'): # select the url in href for all link tags
        if link not in links:
            try:
                if not urlparse(link).scheme:
                    url = self.getBaseUrl() + link
                else:
                    url = link

                if not urllib2.urlopen(url).info()['Content-Type'].startswith('text/html'):
                    links.append(link)
            except urllib2.URLError:
                # The URL is valid but the page is not accessible (network or server error etc.)
                logging.warning("The file link " + url + " is not accessible.")
    for link in dom.xpath('//link/@href'): # select the url in href for all link tags
      if link not in links:
        links.append(link)
    for link in dom.xpath('//script/@src'): # select the url in href for all script tags
        if link not in links:
            links.append(link)
    for link in dom.xpath('//img/@src'): # select the url in href for all img tags
        if link not in links:
          links.append(link)

    return links
