class Page:
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
