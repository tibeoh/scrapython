import os, sys, string, urllib2
import Page
import argparse

def savePage(page, localPath='downloaded-site/'):
  file = open(localPath + page.getFilename(), 'w+')
  file.write(localPath + page.content)

def savePageAndFiles(page, localPath='downloaded-site/'):
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

    print link + " -> " + localPath + link

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Download a website from a given URL.')
  parser.add_argument('url', help='URL of the website to download')

  args = parser.parse_args()

  url = args.url

  try:
      f = urllib2.urlopen(url)

      ## Valid URL

      content = f.read()
      myPage = Page.Page(content, url)

      savePageAndFiles(myPage)


  except urllib2.URLError:
    print "The webpage " + args.url + " is not accessible. Please check the URL."
  except:
    print args.url + " is not a valid URL."
    parser.print_help()
