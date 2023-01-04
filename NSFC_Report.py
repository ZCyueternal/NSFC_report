import requests,json,os,datetime
import urllib.request
import os
from PIL import Image

def getUrl(reportID):
    pngUrl=[]
    pageIndex = 1

    while True:
        # 获取img链接
        payload=reportID+"&"+"index="+str(pageIndex) 
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        response=requests.request("POST",APIurl,headers=headers,data=payload)
        jsonRes = json.loads(response.text) # str数据转为json(dict)
        resUrl = jsonRes["data"]["url"]
        imgUrl = rootWeb+resUrl

        # 验证img链接是否有效
        try:
            imgRes = urllib.request.urlopen(imgUrl)
            print("INFO",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"正在获取...第%d页url"%(pageIndex))
        except Exception as err:
            print(err)
            break
        pageIndex += 1 # 循环获取报告全部页数
        pngUrl.append(imgUrl) # 保存img链接数据
    return pngUrl

def downloadPNG(imgUrl,i):
    # 创建png保存路径
    saveDir="./png"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        print("INFO","创建文件夹")
    imgRes = urllib.request.urlopen(imgUrl)
    print("正在下载",i,imgUrl)
    with open(saveDir+"/%s.png"%(str(i)), 'wb') as f:
        f.write(imgRes.read()) # 保存图片

def toPDF(reportName):
    file_path = './png'
    files = os.listdir(file_path)
    order = []
    png_files = []
    sources = []
    for file in files:
        # print(file.split('.')[0])
        order.append(eval(file.split('.')[0]))
    order.sort()
    # print(order)
    for i in order:
        file = str(i) + '.png'
        png_files.append(file)
    print(png_files)

    output = Image.open(file_path + '\\' + png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file_path + '\\' + file)
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)

    pdfName = reportName + '.pdf'
    output.save('.\\' + pdfName, "pdf", save_all=True, append_images=sources)
    print("已输出 " + pdfName)

if __name__ == "__main__":

    rootWeb = "https://kd.nsfc.gov.cn"

    reportURL = 'https://kd.nsfc.gov.cn/finalDetails?id=f203a0d14e98ac5b91a33a3ad3ae1c16'

    APIurl = "https://kd.nsfc.gov.cn/api/baseQuery/completeProjectReport"  # 默认值

    # download in batch
    # reportURList=[
    #     '',
    #     '',
    #     '',
    #     ''
    # ]
    # for reportURL in reportURList:
    try:
        reportID = reportURL.split("?")[-1]
    except:
        print("ERROR", "请检查报告url是否有id关键字")
    print(reportID)

    res = getUrl(reportID)

    for ind,resU in enumerate(res):
        downloadPNG(resU,ind+1)

    reportName= '高维流式大数据的增量特征提取算法研究'
    os.mkdir('./'+reportName)
    toPDF(reportName)