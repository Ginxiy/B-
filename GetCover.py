#Filename:GetCover.py
import requests
import os
from bs4 import BeautifulSoup

UA = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/35.0.1916.114 Safari/537.36',
    'Cookie': 'AspxAutoDetectCookieSupport=1'
}

def make_pageFile(path,page_num,order):
    #具体实施的方法：
    #1 先创建一个(keyword)&order=() 格式的文件夹.
    #2 在这个文件夹下以逐渐递增的数字创建文件夹。文件夹的数量与搜索结果页的页数相等。
    #3 存储图片。 将第一页的图片存储到第一页下，以此类推。
    if not os.path.exists(path + order):
        os.mkdir(path + order )
    for num in range(1,page_num):
        if not os.path.exists(path + order + "\\" +str(num)):
            os.mkdir(path + order + "\\" +str(num))

def save(path,page_url,title,page_num,order):
    if not os.path.exists(path + order):
        os.mkdir(path + order)
    try:
        r = requests.get("http:" + page_url, headers = UA)
        path = path + order +"\\" + str(page_num) + "\\"+ title + "." +page_url.split('.')[-1]
        if not os.path.exists(path):
            f = open(path, "wb")
            f.write(r.content)
            f.close()
            print("【-保存于-】:"+path)
        else:
            print("【-已存在-】:"+path)
    except:
        print("【【获取失败】】："+title)

if __name__ == '__main__':
    count = 1
    keyword = input("输入关键词：")
    page = "https://search.bilibili.com/all?keyword=" + keyword + "&page="
    order = "&order=totalrank"
    #关于order的解释:        -
    #   totalrank 综合排序   -
    #   click 最多点击       -
    #   pubdate 最新发布     -
    #   dm 最多弹幕          -
    #   stow 最多收藏        -

    path = "G:\\bilibilispider\\" + keyword #把G:\\bilibilispider\\ 改成 你所要存储的文件夹
    print("--------------------------------------------------------------")
    print("搜索结果将以何种方式显示？(输入未规定数字或不输入数字则为综合排序)")
    print("1: 综合排序 2:最多点击 3:最新发布 4:最多弹幕 5:最多收藏")
    print("--------------------------------------------------------------")
    choice = input("请输入你的选择（数字）:")

    if(choice == '1'):
        order = "&order=totalrank"
    elif(choice == '2'):
        order = "&order=click"
    elif(choice == '3'):
        order = "&order=pubdate"
    elif(choice == '4'):
        order = "&order=dm"
    elif(choice == '5'):
        order = "&order=stow"

    print("现在" + order)

    q = requests.get(page + str(1) + order, headers = UA)
    Soup_q = BeautifulSoup(q.text, 'html5lib')
    page_upper = Soup_q.find('body', class_="report-wrap-module old-ver")
    page_upper_int = int(page_upper['data-num_pages']) + 1
    print("循环上界：" + str(page_upper_int))
    input("输入任意键开始...")
    make_pageFile(path, page_upper_int, order)

    for i in range(1, page_upper_int):
        r = requests.get(page + str(i) + order,headers = UA)
        Soup = BeautifulSoup(r.text,'html5lib')
        all_li = Soup.find_all('li', class_ = "video matrix " )
        for li in all_li:
            print("----------------------------")
            print(li.a['title'])
            video_html = requests.get("http:" + li.a['href'], headers = UA)
            video_soup = BeautifulSoup(video_html.text,'html5lib')
            img_src = video_soup.find('img')
            print (img_src['src'])
            save(path,img_src['src'],li.a['title'],i,order)
            print("----------------------------")
        print("第" + str(i) + "页爬取完毕")
        print("----------------------------")
