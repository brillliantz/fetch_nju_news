import unittest
import sys
sys.path.append(r'E:\SYS Files\Documents\Python files\fetch_nju_news') #for debugging
import fetch_nju_news


class TestStringMethods(unittest.TestCase):
    
    def test_fetching(self):
        fetcher = fetch_nju_news.FetchNews()
        fetcher.jw()
        fetcher.stuex()
        tmp = fetcher._websites
        for k, v in fetcher._websites.iteritems():
            # v is a list of news, so it cannot be empty
            self.assertGreater(len(v), 3)
    
    def test_filtrate(self, threshold_int=5):
        import datetime as dt
        current = dt.datetime.now()
        threshold = dt.timedelta(threshold_int)
        long_interval = threshold + dt.timedelta(1)
        short_interval = threshold - dt.timedelta(1)
        
        filtrated_list = fetch_nju_news
        fetcher = fetch_nju_news.FetchNews()
        fetcher._websites = {'test_website':
                             [{'data': '1', 'localtime': current - long_interval},
                              {'data': '2', 'localtime': current - short_interval},
                             ]
                            }   # test case
        fetcher.filtrate(intervals={'test_website': threshold_int})
        self.assertEqual(len(fetcher._websites['test_website']), 1)
        
if __name__ == '__main__':
    unittest.main()