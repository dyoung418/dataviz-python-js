# Scrapy key commands

## Create a project
this will create a new directory with several subdirectories

`scrapy startproject <project_name>`

## Shell for real-time exploration
1. Go to root directory of the project
2. type `scrapy shell <target_URL>`
3. This will open up a terminal-based ipython session.
4. Use the %magic to see documentation on magic commands
5. Use `%save <filename.py> 1-15` to save lines 1-15 to filename.py

## Run a spider
1. Create the spider by adding <spider_name>_spider.py file in project_name/project_name/spider directory.
2. Go to root directory
3. run `scrapy list` to see the list of all the spiders.  Your new one should be included
4. run `scrapy crawl <spider_name> -o <output_filename.json>
