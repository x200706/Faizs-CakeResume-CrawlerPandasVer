import requests
import time
import datetime
import random
from bs4 import BeautifulSoup
import pandas as pd

list_serach_job = ["後端工程師", "軟體工程師", "Java", "Django"]

# 创建一个空的DataFrame用于存储数据
df = pd.DataFrame(columns=['職缺名稱', '職缺連結', '公司名稱', '地區', '月薪', '給薪方式'])

for serach_job in list_serach_job:
  page = 0

  while page < 150:
    page += 1
    response = requests.get(
      "https://www.cakeresume.com/jobs/" + serach_job +
      "?location_list[0]=Taipei City, Taiwan&location_list[1]=New Taipei City, Taiwan&location_list[2]=台北市, 台灣&location_list[3]=新北市, 台灣&seniority_level[0]=entry_level&seniority_level[1]=internship_level&seniority_level[2]=associate&page="
      + str(page))  # 台北 新北 初階 實習 助理
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
      if soup.find_all('div', class_='EmptyResults_emptyTitle__XQ18I'
                       )[0].text == 'No results found':
        break
    except IndexError:
      pass

    for job in soup.find_all(
        'div', class_='JobSearchPage_searchResults__yLBAf')[0].find_all(
          'div', class_='JobSearchItem_wrapper__0zoCh'):
      job1 = job.find_all('a', 'JobSearchItem_jobTitle__Fjzv2')[0].text
      job2 = 'https://www.cakeresume.com' + job.find_all(
        'div', class_='JobSearchItem_headerTitle__k_1FH')[0].a['href']
      job3 = job.find_all('div', 'JobSearchItem_headerSubtitle__XoiMM')[0].text
      job5 = job.find_all(
        'div',
        class_=
        'InlineMessage_inlineMessage__I9C_W InlineMessage_inlineMessageLarge__yeH0A InlineMessage_inlineMessageDark__rNo_a'
      )[2].text
      print(job1, job2, job3, job5)
      job51 = job5[0:job5.find('/')]
      job52 = job5[job5.find('/') + 1:len(job5)].replace(" ", "")
      price = ''
      for word in job5:
        if word == '0' or word == '1' or word == '2' or word == '3' or word == '4' or word == '5' or word == '6' or word == '7' or word == '8' or word == '9' or word == '.' or word == '~' or word == '萬':
          price += word
      low_price = ''
      high_price = ''
      if '~' in price:
        low_price = price[0:price.find('~')]
        high_price = price[price.find('~') + 1:len(price)]
      else:
        low_price = price
        high_price = price

      print(low_price, high_price)
      df = df._append(
        {
          '職缺名稱': job1,
          '職缺連結': job2,
          '公司名稱': job3,
          '地區': job5,
          '月薪': job52
        },
        ignore_index=True)
    print("頁數", page)
    print("***************")
    time.sleep(random.randint(5, 15))

# 将DataFrame保存为CSV文件
output_file = 'cake職缺爬蟲' + str(datetime.date.today()) + '.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
