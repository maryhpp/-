import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def topmovies(max_num=50):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    url = 'https://movie.douban.com/typerank?type_name=%E6%82%AC%E7%96%91&type=10&interval_id=100:90&action='
    driver.get(url)

    #获取电影图片
    movie_num = len(driver.find_elements_by_xpath('//div[@class="movie-info"]//span[@class="movie-name-text"]'))
    while movie_num < 50:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # 向下滚动页面
        time.sleep(1)
        new_num = len(driver.find_elements_by_xpath('//div[@class="movie-info"]//span[@class="movie-name-text"]'))
        if movie_num == new_num:
            break

        movie_num = new_num

    movie_top=[]
    for i in range(min(movie_num,max_num)):
        movie = driver.find_elements_by_xpath('//div[@class="movie-info"]//span[@class="movie-name-text"]')[i].text
        movie_top.append(movie)


    print(movie_top)

    driver.quit()

if __name__=='__main__':
    topmovies(50)


