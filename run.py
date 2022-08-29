#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convenience wrapper for running GoogleScrapper directly from source tree."""
import os
import time
from GoogleScraper import scrape_with_config
from GoogleScraper.email_finder import EmailFinder

name = "Phụng Đặng Thị Hải"
company = "CADDi VIETNAM"
position = ""
location = ""

query_key = ["", "contacts", "blog", "twitter", "linkedin", "instagram", "email", "page", "medium"]

def main():
    keywords = [f"{name} {company} {keyword}" for keyword in query_key]

    start = time.time()
    output_path = "\\".join([os.path.dirname(os.path.abspath(__file__)), "Outputs\\csv_test.csv"])
    print(output_path)
    
    config = {
            'keywords': keywords,
            'search_engines': ['google'],
            'num_pages_for_keyword': 1,
            'output_filename': output_path,
            'scrape_method': 'selenium',
            'sel_browser': 'chrome',
            'do_caching': False,
            'num_workers': 10
        }

    search_results = scrape_with_config(config)
    print(search_results.length)
    

    # search_links = ["https://blog.zenprospect.com/people/Kenichi/Sato/60ebde9de3a12e00010da588",
    #                 "https://craft.co/caddi",
    #                 "https://nz.linkedin.com/company/%E3%82%AD%E3%83%A3%E3%83%87%E3%82%A3%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE",
    #                 "https://caddi.vn/recruit",
    #                 "https://caddi.connpass.com/event/245696/",
    #                 "https://www.zoominfo.com/c/caddi/542782065",
    #                 "https://theorg.com/org/caddi",
    #                 "https://twitter.com/ksato9700",
    #                 "https://www.wantedly.com/companies/caddi/members"]

    # search_links = set()
    # for row in search_results:
    #     print(row['link'])
    #     search_links.add(row['link'])

    # email_finder = EmailFinder(links=search_links)
    # email_finder.run()
    # print(email_finder.results)
    
    end = time.time() - start
    print("Finished after ", end)

if __name__ == '__main__':
    main()
