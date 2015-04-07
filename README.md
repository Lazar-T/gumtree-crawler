gumtree-crawler
==================

###About

Crawler built with [Scrapy](http://scrapy.org/). Uses [Tor](https://www.torproject.org/) and [polipo](http://www.pps.univ-paris-diderot.fr/~jch/software/polipo/). Crawls [gumtree.com.au](http://www.gumtree.com.au/s-jobs/c9302?ad=wanted) and gets fields such as: name, location, sender, description, job type.
There are 30k+ job postings available.

### Installation and Running
```
git clone https://github.com/Lazar-T/gumtree-crawler
cd gumtree-crawler
scrapy crawl gumtreeSpider
