Possible alternative class structure

"""
A possible alternative to subclassing the scraper could be to create a fisher (e.g. scraper) 
that performs the page retrieval, parses HTML and stores results. The parsed page object 
would then be passed to a series of analyzers (page, image, css, etc). If the analyzers returned 
results in a dictionary, then storing them would be identical to each analyzer and can be done 
by the fisher. Alternatively, each analyzer could be responsible for storing its own results, 
but that flexibility is more complicated.

The basic shell is:
"""

class fisher:
  
  _analyzers = []
  
  def __init__():
    pass
  
  def addAnalyzer(analyzer):
    _analyzers.add(analyzer)
  
  def goFishing():
    # loop through list of URLs, calling goFish(url) on each
    pass
  
  def goFish(url): # aka scrape
    # Fetch the url
    # Store/cache the page contents
    # parse the url
    # for each analyzer, 
    #   pass url, page contents and parser to analyzer
    #     note, page is retrieved only once for all analyzers, and I think the parsed page can be reused for all analyzers too
    #   self.store(analyzer.name, results)
    pass
  
  def store(name, results):
    # store the results, by analyer name
    pass
  
  
class analyzer:
    def name():
      # return analyzer's name
      pass
    
    def analyze(url, contents, parser):
      results = dict()
      # custom analysis here
      return results
    
    
class pageAnalyzer(analyzer):
      def name():
        return "page"
      
    def analyze(url, contents, parser):
      results = dict()
      # analyze HTML
      return results
      
      
class imageAnalyzer(analyzer):
      def name():
        return "image"
      
    def analyze(url, contents, parser):
      results = dict()
      # analyze images in this page
      # hmm... how do we store/cache the images?
      return results
     
      
  def main():
    fisher = fisher((pageAnalyzer(), imageAnalyzer())); # shortcut, allow fisher to accept a list of analyzers on initialization
    fisher.goFishing()
      
    
