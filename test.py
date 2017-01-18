# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import urllib
import time 
import sys

# http://gall.dcinside.com/board/lists/?id=game_classic1&page=
# http://gall.dcinside.com/board/lists/?id=stock_new2&page=
# http://gall.dcinside.com/board/lists/?id=ib&page=
# http://gall.dcinside.com/board/lists/?id=drama_new1&page=

global last_check
last_check = 0

def dcinside():		
	if len(sys.argv) == 2:
		#initial variable
		gall_link = str(sys.argv[1])
		fix_link = "http://gall.dcinside.com"
		post_title = ""
		post_number = ""
		inner_link = ""
		file_link = ""
		file_name = ""
		file_extension = ""
		save_point = "./"
		now = time.localtime()
		pre_time = str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec)
		save_time = str(now.tm_year) +"년"+ str(now.tm_mon) +"월"+ str(now.tm_mday) +"일"+ str(now.tm_hour) +"시"+ str(now.tm_min) +"분"+ str(now.tm_sec) +"초"
		global last_check
		global open_door

		#1page parsing
		html = urllib.urlopen(gall_link)
		soup = BeautifulSoup(html, "lxml")
		link = soup.find_all("td", { "class" : "t_subject" })

		#picture_post parsing
		for m in link:
			if(m.find("a", {"class":"icon_pic_n"})):

				post_number = m.parent.find("td", {"class" : "t_notice"}).string
				post_title = m.a.string

				if(last_check<int(post_number)):	

					print "\n" + "number = " + post_number
					print "title = " + post_title			

					inner_link = fix_link + m.a.get('href') + "\n"
					html = urllib.urlopen(inner_link)
					soup = BeautifulSoup(html, "lxml")
					link2 = soup.find_all("li", { "class" : "icon_pic" })
					
					#picture parsing
					for n in link2:
						pure_file_name = n.a.string
						file_name = n.a.string + " "
						#file_extension = file_name[-4:-1]

						print "file_name = " + file_name
						print "save_time = " + save_time
						#test code
						#print "file_extension = " + file_extension

						file_link = n.a.get('href')
						a = "http://image.dcinside.com/download.php"
						b = "http://dcimg2.dcinside.com/viewimage.php"
						file_link = file_link.replace(a, b);
						img_file = urllib.urlopen(file_link)

						print ("/// test /// = " + str(last_check) + " < " + str(post_number) )

			
						f = open(save_point + pre_time + "_" + pure_file_name, 'wb')
						f.write(img_file.read())
						f.close()

						last_check = int(post_number)
						
	else:
		print "\n사용 방법이 틀렸습니다. 메뉴얼을 참고하거나 아래 hint를 참고하세요!\n"
		print "hint..."
		print "windows 사용법, python.exe <프로그램명> <갤러리주소>"
		print "linux, mac 사용법, python <프로그램명> <갤러리주소>\n"
		print "ex) python.exe test.py http://gall.dcinside.com/board/lists/?id=stock_new2&page=\n"

if __name__ == "__main__":
	while True:
		dcinside()
		time.sleep(3)



