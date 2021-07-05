import luigi
from utils import nlp_utils

class ScrapeStaticWebsite(luigi.Task):
	param = luigi.Parameter(default=42)
	def requires(self):
		return None

    def run(self):
		# Init list of url are hard coded into nlp_utils.scrap_static_website()
		# but the function accepts kwargs to scrap custom lists of urls
		(self.links, 
		self.links_suffixes, 
		self.direct_links, 
		self.session, 
		self.soup) = nlp_utils.scrap_static_website()
  
	def output(self):
   		return luigi.LocalTarget('/wms/intermediate/scrap_static_website' % self.param)

if __name__ == "__main__":
    luigi.run()