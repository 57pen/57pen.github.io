import urllib.request
from bs4 import BeautifulSoup
import re
import json
import bs4
import os
import urllib.parse
import math
import urllib.error
import time
import random
import requests
import tkinter as tk
from tkinter import ttk
import urllib.parse
from multiprocessing.dummy import Pool


baseurl = "https://www.luogu.com.cn/problem"
difficulty = {"无选择": -1, "暂无评定": 0, "入门": 1, "普及-": 2, "普及/提高-": 3, "普及+/提高": 4, "提高+/省选-": 5, "省选/NOI-": 6, "NOI/NOI+/CTSC": 7}
difficultyMap = dict(zip(difficulty.values(), difficulty.keys()))
tagss = {'语言入门（请选择[入门与面试]题库' : '-2','顺序结构':'353','分支结构':'354','循环结构':'355','数组':'356','字符串（入门)':'357','结构体':'358','函数与递归':'359','算法':''}
def askURL(url):
    with open('user_agents.txt', 'r') as f:
        lines = f.readlines()
        custom_user_agent = random.choice(lines).strip()
    # 设置请求头
    headers = {
        'User-Agent': custom_user_agent,
        "Cookie": "__client_id=36c26470355e2c004dc4e2f167ba0be9c7117ea0; _uid=1095039 ; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000"
    }
    html = ""
    try:
        html = requests.get(url, headers=headers)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html.text

def decodeJs(html):
    bs = BeautifulSoup(html, "html.parser")
    core = bs.select("script")[0]
    script = str(core)
    node1 = script.index('"')
    node2 = script.index('"', node1 + 1)
    script = script[node1 + 1: node2]
    decodedStr = urllib.parse.unquote(script)
    js = json.loads(decodedStr)
    return js

def getNo(html):
    soup = BeautifulSoup(html, "html.parser")
    s = soup.find_all('div', class_="")
    No = re.findall(r'<a href="(P\d+)">',str(s))
    return No

def getName(html):
    soup = BeautifulSoup(html, "html.parser")
    name = soup.find_all('li')
    return name
def getNum(tag='',difficulty='',key = ''):
    url = baseurl + "/list?" + "difficulty=" + str(difficulty) + "&tag=" + tag + "&keyword=" + key + "&page=" + '1'
    html = askURL(url)
    js = decodeJs(html)
    number = re.findall(r'\'count\': (\d+)', str(js))
    total = str(number)
    index1 = total.index('\'')
    index2 = total.index('\'',index1 + 1)
    total = total[index1 + 1: index2]
    page = math.ceil(int(number[0])/50)
    num = [total,page]
    return num

def getMD(html,name):
    print("正在爬取{}".format(name))
    bs = bs4.BeautifulSoup(html,"html.parser")
    core = bs.select("article")[0]
    while not core:
        print("正在重试...")
        core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    print("{}爬取完成".format(name))
    return md

def getsolutionMD(html,name):
    print("正在爬取\"{}\"的题解".format(name))
    js = decodeJs(html)
    solutions = js["currentData"]["solutions"]["result"]
    if len(solutions) > 0:
        bestSolution = solutions[0]
        md = bestSolution["content"]
    else:md = ''
    print("\"{}\"题解爬取完成".format(name))
    return md

def getInfo(html):
    js = decodeJs(html)
    dif = re.findall(r'difficulty\': (\d),', str(js))
    return str(dif[0])

def saveData(data,filename,saveDir,fatherDir):
    savePath = "D:\\Code\\Python\\Software Engineering\\Text2\\"
    dirPath = savePath + fatherDir + "\\" + saveDir
    
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    
    f = open(dirPath + "\\" + filename + ".md", "w", encoding="utf-8")
    f.write(data)
    f.close()

def clearData():
    savePath = "D:\\Code\\Python\\Software Engineering\\Text2\\"
    for root, dirs, files in os.walk(savePath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def openfile():
    os.startfile("D:\\Code\\Python\\Software Engineering\\Text2\\")



def total():
    def rep(Dif = '', Tags = '', keyword = ''):
        Dif = str(bnt1.get())
        if(Dif == '请选择难度'):
            Dif = ''
        else:
            Dif = str(difficulty.get(Dif))
        Tags = str(bnt2.get())
        if(Tags == '算法'):
            Tags = ''
        else:
            Tags = str(tagss.get(Tags))
        keyword = search_entry.get()
        if (keyword == '请输入关键词'):
            keyword = ''
        num = getNum(difficulty = Dif,tag = Tags,key = keyword)
        tag = ''
        output_text.insert(tk.END, "共计"+ num[0] + "条结果\n")
        output_text.update()
        output_text.see(tk.END)
        print("共计{}条结果".format(num[0]))
        for i in range(1,num[1]+1):
            url = baseurl + "/list?" + "difficulty=" + Dif + "&tag=" + Tags + "&page=" + str(i)
            html = askURL(url)
            No = getNo(html)
            Name = getName(html)
            cnt = 0;
            for k in No:
                work = 50*(i-1) + cnt + 1
                name = Name[cnt].text
                name = name.replace('/','')
                name = re.sub(r"[\\/:\*\?\"<>\|]", "_", name)
                name = name.replace(' ','')
                url = baseurl + "/" + k
                html = askURL(url)
                output_text.insert(tk.END, "正在爬取" + name + "\n")
                output_text.update()
                output_text.see(tk.END)
                data = getMD(html,name)
                output_text.insert(tk.END, name + "爬取完成" + "\n")
                output_text.update()
                output_text.see(tk.END)
                js = decodeJs(html)
                dif = re.findall(r'difficulty\': (\d),', str(js))
                tags = re.findall(r'\'tags\': \[(.*?)]',str(js))
                s = name.find('[')
                if(name.find('[')>0):
                    index1 = name.index('[')
                    index2 = name.index(']')
                    tag = name[index1 + 1: index2]
                fatherDir = difficultyMap.get(int(dif[0])) + '-' + tag
                saveData(data, name, name, fatherDir)
                solutionurl = baseurl + "/solution/" + k
                html = askURL(solutionurl)
                output_text.insert(tk.END, "正在爬取\"{}\"的题解".format(name) + "\n")
                output_text.update()
                output_text.see(tk.END)
                data = getsolutionMD(html, name)
                output_text.insert(tk.END, "\"{}\"题解爬取完成".format(name) + "\n")
                output_text.update()
                output_text.see(tk.END)
                saveData(data, name + '-题解', name, fatherDir)
                print('当前进度（' + str(work) + '/' + num[0] + ')')
                output_text1.insert(tk.END, '当前进度（' + str(work) + '/' + num[0] + ')' + '\n' )
                output_text1.update()
                output_text1.see(tk.END)
                cnt += 1
                time.sleep(random.randint(0, 1))

    window = tk.Tk()
    window.title("爬取--洛谷习题")

    window.geometry("500x450")
    window.configure(bg="white")

    bnt1 = ttk.Combobox(window, values=["请选择难度", "暂无评定", "入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-","NOI/NOI+/CTSC"])
    bnt1.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    def on_entry_click(event):
        if search_entry.get() == '请输入关键词':
            search_entry.delete(0, tk.END)
            search_entry.config(foreground='black')

    def on_focus_out(event):
        if search_entry.get() == '':
            search_entry.insert(0, '请输入关键词')
            search_entry.config(foreground='gray')

    search_entry = tk.Entry(window, width=15)
    search_entry.insert(0, '请输入关键词')
    search_entry.config(foreground='gray')
    search_entry.bind('<FocusIn>', on_entry_click)
    search_entry.bind('<FocusOut>', on_focus_out)
    search_entry.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    bnt2 = ttk.Combobox(window,values=["算法", "语言入门（请选择[入门与面试]题库", "顺序结构", "分支结构", "循环结构", "数组","字符串（入门)", "结构体", "函数与递归"])
    bnt2.grid(row=0, column=3, padx=10, pady=10, sticky='w')

    window.grid_columnconfigure(0, weight=1)
    bnt1.current(0)
    bnt2.current(0)

    output_text = tk.Text(window, height=20, width=66)
    output_text.grid(row=6, column=0, rowspan=3, columnspan=10, padx=10, pady=10, sticky='w')
    output_text1 = tk.Text(window, height=1, width=66)
    output_text1.grid(row=3, column=0, rowspan=3, columnspan=10, padx=10, pady=10, sticky='w')

    button = tk.Button(window, text="开始", command=rep)
    button.grid(row=1, column=3, padx=15, pady=15, sticky='e')

    button1 = tk.Button(window, text="清除数据", command=clearData)
    button1.grid(row=1, column=2, padx=15, pady=15, sticky='w')

    button2 = tk.Button(window, text="打开文件夹", command=openfile)
    button2.grid(row=1, column=1, padx=15, pady=15, sticky='w')

    window.mainloop()

def main():
    window = tk.Tk()
    window.title("爬虫")

    window.geometry("600x300")
    window.configure(bg="white")

    button = tk.Button(window, text="进入程序", command=total, width=20, height=5)
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    window.mainloop()

if __name__ == "__main__":  # 当程序执行时
    main()

      