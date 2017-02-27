# -*- coding: utf-8 -*-
import requests
import re
import bs4
import datetime


class FetchNews(object):
    def __init__(self):
        self.s = requests.Session()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2963.0 Safari/537.36',
        }
        self.s.headers.update(self.headers)
        self.url_prefix = {'jw': 'http://jw.nju.edu.cn/',
                           'stuex': 'http://stuex.nju.edu.cn/',
                           }
        self._websites = {}   # each key is a name of website,
                            # each value is a list of news (news dicts) from the website.
        self.output = {}    # each key is a name of website,
                            # each value is str ready to be sent
    def jw(self):
        """Fetch latest news from jw.nju.edu.cn,
        return a list of reformatted string ready to be sent.

        """
        url = self.url_prefix['jw'] + 'allContentList.aspx?MType=PX-WZSY-ZXTZ'
        res = self.s.get(url)
        content = res.content

        match = re.search(r'<ul class="listContent">([\s,\S]+?)</ul>', content)
        news_raw = match.groups()[0]  # raw html string of news section

        soup = bs4.BeautifulSoup(news_raw, 'html.parser')
        news_list = soup.findAll('li')  # news entries

        news_dict_list = [] # encompass entries (reformatted to dict) of news
        for news in news_list:
            news_title = news.find('a').get_text()
            news_time = news.find('span', class_='time_l').get_text()
            news_url = self.url_prefix['jw'] + re.search(r'href="(.+?)"', str(news)).groups()[0]
            # when parse raw html to beautifulsoup, it will replace '&' with '&amp;', destroying the URLs.
            news_url = re.sub(r'&amp;', r'&', news_url)
            news_dict = {'title': news_title,
                     'time': datetime.datetime.strptime(news_time, '[%Y-%m-%d]'),
                     'time_str': news_time,
                     'url': news_url
                     }
            news_dict = clean_new_line(news_dict)
            news_dict_list.append(news_dict)
        
        self._websites['jw'] = news_dict_list

    def stuex(self):
        """Fetch latest news from stuex.nju.edu.cn, 
        return a list of entries of news, with each entry being a dict.

        Parameters
        -----------

        Returns
        --------
        news_dict_list : list. Entries of news

        """
        url = self.url_prefix['stuex'] + ''
        res = self.s.get(url)
        content = res.content
        soup = bs4.BeautifulSoup(content, 'html.parser')
        tag_content = soup.findAll('div', class_='tagContent')
        news_list = tag_content[0].findAll('li')  # news entries

        #TODO the following bloack of codes are duplicate with those in self.jw()
        news_dict_list = [] # encompass entries (reformatted to dict) of news
        for news in news_list:
            news_title = news.find('a').get_text()
            news_time = news.find('span', class_='mccLtime').get_text()
            news_url = self.url_prefix['stuex'] + re.search(r'href="(.+?)"', str(news)).groups()[0]
            # when parse raw html to beautifulsoup, it will replace '&' with '&amp;', destroying the URLs.
            news_url = re.sub(r'&amp;', r'&', news_url)
            news_dict = {'title': news_title,
                         'localtime': datetime.datetime.strptime(news_time, '%Y-%m-%d'),
                         'time_str': news_time,
                         'url': news_url
                        }
            news_dict_list.append(news_dict)
        
        self._websites['stuex'] = news_dict_list
    
    def filtrate(self, interval=3):
        """Drop news which are outdated.
        
        Parameters
        -----------
        interval : int. Criteria used to judge "latest".
        
        """
        now = datetime.datetime.now()
        func = lambda x: (now - x['localtime']) <= datetime.timedelta(interval)
        for k, v in self._websites.iteritems():
            self._websites[k] = filter(func, v)
    
    def combine(self):
        """Generate a ready-to-be-sent string from news dicts.

        Parameters
        -----------
        dicts : list. Entries of news.
        name : str. The website to which the news belong.

        Returns
        --------
        res : list. Entries of qualified news.

        """
        for k, v in self._websites.iteritems():
            news_str_list = []
            for news_dict in v:
                news_dict.pop('localtime')
                
                news_dict = clean_new_line(news_dict)
                
                news_str = '\n'.join(news_dict.values())
                news_str_list.append(news_str)
          
            s = ('='*5 + name + 'START'+ '='*5 + '\n'
                   + '\n\n'.join(news_str_list) + '\n\n'
                   + '='*5 + name + 'END'+ '='*5 + '\n')
            self.output[k] = s
    
    def go(self, targets):
        if not targets:
            print "ERROR! parameter [targets] is null!"
        else:
            if isinstance(targets, str):
                targets = [targets]
            
            if isinstance(targets, (list, tuple)):
                for target in targets:
                    if target == 'jw':
                        self.jw()
                        interval = 3
                    elif target == 'stuex':
                        self.stuex()
                        interval = 9
                    else:
                        print 'ERROR! [target] is not recognized!'
                self.filtrate(interval)
                self.combine()
            else:
                print 'ERROR! [targets] is not recognized!'    

def clean_new_line(obj):
    STR_TYPES = (str, unicode)
    def clean(s):
        s = s
        s = re.sub(r'\n', '', s)
        s = re.sub(r'\r', '', s)
        return s

    if isinstance(obj, STR_TYPES):
        res = clean(obj)
    elif isinstance(obj, dict):
        for k, v in obj.iteritems():
            if isinstance(v, STR_TYPES):
                obj[k] = clean(v)
        res = obj
    else: 
        print 'ERROR! type of obj is not recognized!'
    return res

if __name__ == '__main__':
    fetcher = FetchNews()
    msgs = []
    
    fetcher.go(['jw', 'stuex'])

    t = time.localtime()
    t_s = str(t.tm_year)+'-'+str(t.tm_mon)+'-'+str(t.tm_mday)+' '+str(t.tm_hour+8)+':'+str(t.tm_min)+':'+str(t.tm_sec)
    print t_s

    for k, v in fetcher.output.iteritems():
        print k
        print v