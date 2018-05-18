import pandas as pd
from tqdm import tqdm
import time,bs4,requests,re
heading,link,dat,lead,text,video = ([],[],[],[],[],[])
for q in tqdm(range(1,28)):
    time.sleep(0.5)
    response = requests.get('http://www.president.gov.ua/news/speeches?date-from=07-06-2014&date-to=09-05-2018&page=' + str(q)).text
    parsed_html = bs4.BeautifulSoup(response, 'lxml')
    for w in range(len(parsed_html.select('.cat_list h3'))):
        heading.append(parsed_html.select('.cat_list h3')[w].getText().strip())
        link.append(parsed_html.select('.cat_list .item_stat_headline a')[w].get('href'))
        dat.append(parsed_html.select('.cat_list .item_stat_headline p')[w].getText().strip())
        lead.append(parsed_html.select('.cat_list .item_short')[w].getText().strip())
        time.sleep(0.5)
        response_text = requests.get(link[-1]).text
        parsed_text = bs4.BeautifulSoup(response_text, 'lxml')
        text.append(parsed_text.select('.article_content')[0].getText().strip())
        if not parsed_text.select('iframe'):
            if not parsed_text.select('object'):
                video.append(False)
            else:
                video.append(parsed_text.select('object')[0].get('data').replace('//www.youtube.com/v','https://www.youtube.com/watch?v='))
        else:
            video.append(parsed_text.select('iframe')[0].get('src').replace('embed/','watch?v='))
news = pd.DataFrame({'heading':heading,'link':link,'dat':dat,'lead':lead,'text':text,'video':video})
news.to_csv('speeches_president.csv')