import Page, urllib2
from urlparse import urlparse
import unittest

def suite():

    testPagesResults = []

    testPagesResults.append({
    'url':"http://bouye.fr",
    'filename':"index.html",
    'domain':"bouye.fr",
    'domainLink':{'link':"http://bouye.fr/css/style.css", 'result':"bouye.fr"},
    'baseUrl':"http://bouye.fr/"
    })

    testPagesResults.append({
    'url':"http://tibeoh.fr",
    'filename':"index.html",
    'domain':"tibeoh.fr",
    'domainLink':{'link':"http://tibeoh.fr/css/style.css", 'result':"tibeoh.fr"},
    'baseUrl':"http://tibeoh.fr/"
    })

    testPagesResults.append({
    'url':"http://tibeoh.fr/",
    'filename':"index.html",
    'domain':"tibeoh.fr",
    'domainLink':{'link':"http://tibeoh.fr/css/style.css", 'result':"tibeoh.fr"},
    'baseUrl':"http://tibeoh.fr/"
    })

    testPagesResults.append({
    'url':"tibeoh.fr",
    'filename':"index.html",
    'domain':"tibeoh.fr",
    'domainLink':{'link':"http://tibeoh.fr/css/style.css", 'result':"tibeoh.fr"},
    'baseUrl':"http://tibeoh.fr/"
    })


    suite = unittest.TestSuite()
    suite.addTests(PageTestSequence(testPagesResult, 'test_getUrl') for testPagesResult in testPagesResults)
    suite.addTests(PageTestSequence(testPagesResult, 'test_getFilename') for testPagesResult in testPagesResults)
    suite.addTests(PageTestSequence(testPagesResult, 'test_getDomain') for testPagesResult in testPagesResults)
    suite.addTests(PageTestSequence(testPagesResult, 'test_getLinkDomain') for testPagesResult in testPagesResults)
    suite.addTests(PageTestSequence(testPagesResult, 'test_getBaseUrl') for testPagesResult in testPagesResults)
    return suite

class PageTestSequence(unittest.TestCase):

    def __init__(self, pageTestResult, methodName):
        super(PageTestSequence, self).__init__(methodName)
        self.pageTestResult = pageTestResult


    def setUp(self):
        url = self.pageTestResult['url']
        if not urlparse(url).scheme:
          url = "http://"+url
        f = urllib2.urlopen(url)
        content = f.read()
        self.testPage = Page.Page(content, url)

    def test_getUrl(self):
        self.assertEqual(self.testPage.getUrl(), self.pageTestResult['url'])

    def test_getFilename(self):
        self.assertEqual(self.testPage.getFilename(), self.pageTestResult['filename'])

    def test_getDomain(self):
        self.assertEqual(self.testPage.getDomain(), self.pageTestResult['domain'])

    def test_getLinkDomain(self):
        self.assertEqual(self.testPage.getLinkDomain(self.pageTestResult['domainLink']['link']), self.pageTestResult['domainLink']['result'])

    def test_getBaseUrl(self):
        self.assertEqual(self.testPage.getBaseUrl(), self.pageTestResult['baseUrl'])


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
