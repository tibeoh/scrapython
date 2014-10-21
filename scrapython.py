import os, sys, string, urllib2
import Page

def savePage(page, localPath='./download/'):
  file = open(localPath + page.getFilename(), 'w+')
  file.write(localPath + page.content)

def savePageAndFiles(page, localPath='./download/'):
  if not os.path.exists(localPath):
      os.makedirs(localPath)
  file = open(localPath + page.getFilename(), 'w+')
  file.write(page.content)
  fileLinks = page.getFiles()
  for link in fileLinks:
    url = page.getBaseUrl() + link
    f = urllib2.urlopen(url)
    content = f.read()
    currentPage = Page.Page(content, url)

    # Create folders to save files
    if not os.path.exists(os.path.dirname(localPath + link)):
      os.makedirs(os.path.dirname(localPath + link))

    file = open(localPath + link, 'w+')
    file.write(currentPage.content)

if __name__ == '__main__':
  if(len(sys.argv)) > 1:
    url = sys.argv[1]

    f = urllib2.urlopen(url)
    content = f.read()
    myPage = Page.Page(content, url)

    savePageAndFiles(myPage)

  else:
    print "No argument found"
