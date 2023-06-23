#!/usr/bin/bash


xvfb-run scrapy crawl sreality 
python3 simple_server/simple_http_server.py
