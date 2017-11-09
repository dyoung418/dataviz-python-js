# dataviz-python-js
My working files from reading "Data Visualization with Python &amp; JavaScript" by Kyran Dale.

Note that this does not include the git repository that the author makes available (I don't
want to repeat it.)  However, it can be manually placed in this directory by running


git clone https://github.com/Kyrand/dataviz-with-python-and-js.git


Note that I've already included the directory that is created by this command in .gitignore


Also, the 'nobel_winners' directory was created by the scrapy library for python.  The
command to make it was


scrapy startproject nobel_winners


Most of the files in that directory were generated automatically, but the important files to look at are in the top level directory where I captured a session of 'scrapy shell' (which runs a terminal-based ipython) in day-exploration.py.  Also, the spider I created at nobel_winners/nobel_winners/spiders/nwinners_list_spider.py and the spider for getting bios and photos: nobel_winners/nobel_winners/spiders/minibio_nwinners_spider.py. Also the pipeline.py in nobel_winners and the comm directory that I created there.

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
