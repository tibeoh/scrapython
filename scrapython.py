import os, sys, string, urllib2
import Page
import argparse
from urlparse import urlparse

def savePage(page, localPath='downloaded-site/'):
  file = open(localPath + page.getFilename(), 'w+')
  file.write(page.content)

def replaceLinks(filespath, path, links):
    filespath = "files/"
    infile = open(path)
    outfile = open(path+"2", 'w')

    replacements = {}
    for link in links:
        splittedPath = urlparse(link).path.split('/')
        filename = splittedPath[len(splittedPath)-1]
        replacements.update({link:(filespath+filename)})

    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        outfile.write(line)
    infile.close()
    outfile.close()

    os.remove(path)
    os.rename(path+"2", path)


def savePageAndFiles(page, downloadedPages, deepLevel=0, localPath='downloaded-site/'):
    localPath = localPath + page.getDomain() + "/"
    filesPath = localPath + "files/"
    if not os.path.exists(localPath):
        os.makedirs(localPath)
    if not os.path.exists(filesPath):
        os.makedirs(filesPath)

    savePage(page, localPath)

    downloadedPages.append(page.getBaseUrl() + page.getFilename())

    ## Saving files associated to current page.
    fileLinks = page.getFiles()
    for link in fileLinks:
        url = page.getBaseUrl() + link
        try:
            f = urllib2.urlopen(url)
            content = f.read()
            currentPage = Page.Page(content, url)

            # Create folders to save files
            # if not os.path.exists(os.path.dirname(localPath + link)):
            #     os.makedirs(os.path.dirname(localPath + link))
            #
            # file = open(localPath + link, 'w+')
            # file.write(currentPage.content)

            splittedPath = urlparse(link).path.split('/')
            filename = splittedPath[len(splittedPath)-1]
            file = open(filesPath + filename, 'w+')
            file.write(currentPage.content)

            print link + " -> " + localPath + link
        except urllib2.URLError:
          print "file " + url + " is not accessible. Please check the URL."
        except Exception as inst:
          print inst
          print "file" + url + " is not a valid URL."

    replaceLinks(filesPath, localPath + page.getFilename(), fileLinks)


    ## recursion in links
    if(deepLevel > 0):
        pageLinks = page.getDomainLinks()
        for pageLink in pageLinks:
            pageLink = page.getBaseUrl() + pageLink
            if(pageLink not in downloadedPages):
                try:
                    f = urllib2.urlopen(pageLink)
                    ## Valid URL
                    content = f.read()
                    myPage = Page.Page(content, pageLink)
                    # self calling
                    savePageAndFiles(myPage, downloadedPages, deepLevel-1)
                except urllib2.URLError:
                      print "Link error: " + pageLink + " is not accessible."
                except:
                      print "Link error: " + pageLink + " is not a valid URL."

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Download a website from a given URL.')
  parser.add_argument('url', help='URL of the website to download')
  parser.add_argument('--rec', type=int, help='Deepness of link recursion')

  args = parser.parse_args()

  url = args.url

  if(args.rec != None):
      deepLevel = args.rec
  else:
      deepLevel = 0

  try:
      f = urllib2.urlopen(url)

      ## Valid URL
      content = f.read()
      myPage = Page.Page(content, url)

      downloadedPages = []
      savePageAndFiles(myPage, downloadedPages, deepLevel)


  except urllib2.URLError:
    print "The webpage " + url + " is not accessible. Please check the URL."
  except Exception as inst:
    print inst
    print url + " is not a valid URL."
    parser.print_help()
