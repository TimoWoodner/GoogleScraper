#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convenience wrapper for running GoogleScrapper directly from source tree."""

from GoogleScraper import scrape_with_config
from email_finder import EmailFinder

def main():
    config = {
            'keyword': 'Daisuke Takei Caddi contacts',
            'search_engines': ['Google'],
            'num_pages_for_keyword': 1,
            'output_filename': "csv_test.csv",
            'scrape_method': 'selenium',
            'sel_browser': 'chrome',
            'do_caching': False,
            'num_workers': 5
        }

    search_results = scrape_with_config(config)

    # search_links = ["https://blog.zenprospect.com/people/Kenichi/Sato/60ebde9de3a12e00010da588",
    #                 "https://craft.co/caddi",
    #                 "https://nz.linkedin.com/company/%E3%82%AD%E3%83%A3%E3%83%87%E3%82%A3%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE",
    #                 "https://caddi.vn/recruit",
    #                 "https://caddi.connpass.com/event/245696/",
    #                 "https://www.zoominfo.com/c/caddi/542782065",
    #                 "https://theorg.com/org/caddi",
    #                 "https://twitter.com/ksato9700",
    #                 "https://www.wantedly.com/companies/caddi/members"]

    search_links = []
    for row in search_results:
        print(row['link'])
        search_links.append(row['link'])

    email_finder = EmailFinder(links=search_links)
    email_finder.run()
    print(email_finder.results)
    

if __name__ == '__main__':
    main()
