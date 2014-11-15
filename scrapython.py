import os, urllib2
import Page
import argparse
from urlparse import urlparse

def savePage(page, localPath='downloaded-site/'):
  file = open(localPath + page.getFilename(), 'w+')
  file.write(page.content)
  print "saving " + page.getFilename()

def saveFile(content, path):
  file = open(path, 'w+')
  file.write(content)
  print "file saved -> " + path


def replaceLinks(filesDir, path, pageLinksReplacements):

    infile = open(path)
    outfile = open(path+"temp", 'w')


    replacements = {}

    # add the local path of files in replacement
    for link in pageLinksReplacements.keys():
        replacements[link] = filesDir+pageLinksReplacements[link]

    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        outfile.write(line)
    infile.close()
    outfile.close()

    os.remove(path)
    os.rename(path+"temp", path)

def saveAllFiles(filesPath, downloadedFiles, fileLinks, pageBaseUrl, pageName):

  if not os.path.exists(filesPath):
      os.makedirs(filesPath)

  pageLinksReplacements = {}
  for link in fileLinks:
      if not urlparse(link).scheme:
        print "add base " + link
        url = pageBaseUrl + link
      else:
        print "add pas " + link
        url = link
      #url = pageBaseUrl + link
      try:
          splittedPath = urlparse(link).path.split('/')
          filename = splittedPath[len(splittedPath)-1]

          if link in downloadedFiles.keys():
            # le fichier a deja ete telecharge on l\'ajoute au remplacement de la page actuelle
            pageLinksReplacements[link] = filename

          else:
            # le fichier n\'a jamais ete telecharge
            # on va le telecharger de toute facon donc on l\'ouvre
            f = urllib2.urlopen(url)
            fileContent = f.read()

            if filename in downloadedFiles.values():
              # un fichier avec le mm nom a ete telecharge
              # On le renome avec un increment
              # count the number of files with the same filename
              count = 0
              for val in downloadedFiles.values():
                if val == filename:
                  count = count+1

              filenameWithoutExtension, extension = os.path.splitext(filename)
              filenameWithoutExtensionPlusCount = filenameWithoutExtension + "-" + str(count) + pageName

              pageLinksReplacements[link] = filenameWithoutExtensionPlusCount + extension
              newPath = filesPath + filenameWithoutExtensionPlusCount + extension

              saveFile(fileContent, newPath)

            else:
              # jamais ete dl et possede un nom different, on le telecharge
              saveFile(fileContent, filesPath + filename)
              pageLinksReplacements[link] = filename

          downloadedFiles[link] = filename

      except urllib2.URLError:
        print ("file at " + url + " is not accessible. Please check the URL.")
      except Exception as inst:
        print (inst)
        print ("file at " + url + " has not a valid URL.")

  return pageLinksReplacements

def savePageAndFiles(page, downloadedPages, downloadedFiles, deepLevel=0, localPath='downloaded-site/', filesDir='files/'):
    localPath = localPath + page.getDomain() + "/"
    filesPath = localPath + "files/"

    if not os.path.exists(localPath):
        os.makedirs(localPath)

    savePage(page, localPath)
    downloadedPages.append(page.getBaseUrl() + page.getFilename())

    ## Saving files associated to current page.
    pageLinksReplacements = saveAllFiles(filesPath, downloadedFiles, page.getFilesLinks(), page.getBaseUrl(), page.getFilename())

    replaceLinks(filesDir, localPath + page.getFilename(), pageLinksReplacements)

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
                    savePageAndFiles(myPage, downloadedPages, downloadedFiles, deepLevel-1)
                except urllib2.URLError:
                      print ("Link error: " + pageLink + " is not accessible.")
                except Exception as inst:
                      print inst
                      print ("Link error: " + pageLink + " is not a valid URL.")

if __name__ == '__main__':

  # Instenciate the argument parser
  parser = argparse.ArgumentParser(description='Download a website from a given URL.')
  # Add different arguments
  parser.add_argument('url', help='URL of the website to download')
  parser.add_argument('--rec', type=int, help='Deepness of link recursion')

  # args contrains the passed arg values
  args = parser.parse_args()

  # arg url is required so it can't be null
  url = args.url

  # arg rec (level of recursivity) is optional. If it's not set, the default rec level is 0
  if(args.rec != None):
      deepLevel = args.rec
  else:
      deepLevel = 0

  # urllib2 test tha validity and accesibilty of an URL and a website.
  # it can throw exceptions in case of errors so we have to catch them to prevent any crash
  try:
      if not urlparse(url).scheme:
        url = "http://"+url
      f = urllib2.urlopen(url)

      # Valid URL
      content = f.read()
      # instanciate a page object
      myPage = Page.Page(content, url)
      # in order to keep track of the saved pages (to not download again the same pages)
      downloadedPages = [] # values: URL
      downloadedFiles = {} # key: URL value: filename
      # call of the recursive function that download a page according the
      savePageAndFiles(myPage, downloadedPages, downloadedFiles, deepLevel)


  except urllib2.URLError:
   # The URL is valid but the page is not accessible (network or server error etc.)
   print ("The webpage " + url + " is not accessible. Please check the URL.")
  except Exception as inst:
    print inst
    print (url + " is not a valid URL.")
    parser.print_help()
