socialplus
==========

Social Plus - Google+ for Enterprise

Deploy
------

1. you need to compile the GUI files, all .jade .coffee and .scss files in the /public directory. Simply output the compiled version in the same directory as the source file. Compiled versions are already gitignored. An example script to do this could be (depends on you OS and configuration):

    #!/bin/sh
    jade DJANGO_GAE/public/html/
    jade DJANGO_GAE/pages/
    coffee -c DJANGO_GAE/public/js/coffee/
    sass --update DJANGO_GAE/public/css/

2. run the appengine server, from the DJANGO_GAE directory:
    
    dev_appserver.py --port=8080 ./

3. open the GUI at the address:

    http://localhost:8080/public/html/main.html

4. in the sync tab, click "reset domain" and then run the first four tasks one after the other, in the order they're displayed.

To create and view reports, specify a query in the activities->advanced tab, then create a report with a new name. To update the report, go to the sync tab and use the relevant task. Only after having updated it you can view it from the reports tab.