import sys, string, urllib2
import Page

if __name__ == '__main__':
  if(len(sys.argv)) > 1:
    url = sys.argv[1]

    f = urllib2.urlopen(url)
    content = f.read()
    myPage = Page.Page(content, url)

    print myPage.getDomainLinks()
  else:
    print "No argument found"
