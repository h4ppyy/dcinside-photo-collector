#-*- coding:utf-8 -*-
import requests
import urllib
import pymysql
from bs4 import BeautifulSoup

conn = pymysql.connect(
    host='192.168.33.22', 
    user='admin', 
    password='0000',
    db='adult', 
    charset='utf8'
)

fix_link = "http://gall.dcinside.com"
upload_dir = '/Users/ahn/python/img/'

url = 'http://gall.dcinside.com/board/lists/?id=baseball_new6&page=1'
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'ko-KR,ko;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'gall.dcinside.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}

r = requests.get(url, headers=headers)

html = r.text

#rows = curs.fetchall()

soup = BeautifulSoup(html, "lxml")
link = soup.find_all("td", { "class" : "t_subject" })
for m in link:
    if(m.find("a", {"class":"icon_pic_n"})):
        post_number = m.parent.find("td", {"class" : "t_notice"}).string
        post_title = m.a.string
        print "글번호 = ", post_number
        print "글제목 = ", post_title

        inner_link = fix_link + m.a.get('href') + "\n"
        print inner_link
        r = requests.get(inner_link, headers=headers)
        inner_html = r.text
	soup = BeautifulSoup(inner_html, "lxml")
	link2 = soup.find_all("li", { "class" : "icon_pic" })
        cnt = 0
        for n in link2:
      	    pure_file_name = n.a.string
            file_link = n.a.get('href')
            print "파일명 = " + pure_file_name.encode('utf-8')
            tmp_a = "http://image.dcinside.com/download.php"
	    tmp_b = "http://dcimg2.dcinside.co.kr/viewimage.php"
	    file_link = file_link.replace(tmp_a, tmp_b);
            print "다운로드링크 = " + file_link
            print "------------------------------------------------------------->"
            r = requests.get(file_link, headers=headers)
            fff = r.text
            img_file = urllib.urlopen(file_link)
            full_dir = upload_dir + post_number + '#' + str(cnt) + ".png"
            full_path = post_number + '#' + str(cnt) + ".png"
            f = open(full_dir, 'wb')
            #f.write(fff.read())
            f.write(img_file.read())
	    f.close()
            curs = conn.cursor()
            sql = '''
                insert into picture(file_name)
                values('{filename}')
            '''.format(filename=full_path)
            curs.execute(sql)
            cnt += 1
conn.close()
