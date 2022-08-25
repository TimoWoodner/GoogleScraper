#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convenience wrapper for running GoogleScrapper directly from source tree."""

from GoogleScraper import scrape_with_config

def main():
    config = {
            'keyword': 'Kenichi Sato Caddi',
            'search_engines': ['Google'],
            'num_pages_for_keyword': 1,
            'output_filename': "csv_test.csv",
            'scrape_method': 'selenium',
            'sel_browser': 'chrome',
            'do_caching': False,
            'num_workers': 5
        }

    search = scrape_with_config(config)
    for serp in search.serps:
        print(serp)

if __name__ == '__main__':
    main()
