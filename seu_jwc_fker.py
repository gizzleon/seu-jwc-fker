# -*- coding: utf-8 -*-
#!/usr/bin/python  
#import urllib.request

########################################################################
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
#
#       Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#   Everyone is permitted to copy and distribute verbatim or modified
#   copies of this license document, and changing it is allowed as long
#   as the name is changed.
#
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#            0. You just DO WHAT THE FUCK YOU WANT TO.
########################################################################


import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re
import time
import sys   
reload(sys)  


def loginIn(userName,passWord):
    #����cookie������
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
    urllib2.install_opener(opener)  
    #��ѡ��ҳ��
    h = urllib2.urlopen('http://xk.urp.seu.edu.cn/') 
    #��ȡ��֤��
    image = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/getCheckCode')
    f = open('code.jpg','wb')
    f.write(image.read())
    f.close()
    #��ȡ��֤��
    code = raw_input('���������Ŀ¼�µ�code.jpg���������������������λ������֤�룺')
    #����post����
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' 
    header ={   
                'Host' : 'xk.urp.seu.edu.cn',   
                'Proxy-Connection' : 'keep-alive',
                'Origin' : 'http://xk.urp.seu.edu.cn',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
                }
    data = {
            'userId' : userName,
            'userPassword' : passWord, #������룬  
            'checkCode' : code,           #��֤�� 
            'x' : '33',     #���
            'y' : '5'       #���2
            }
            
    #post��¼����
    text = postData(posturl,header,data)
    print "��¼�ɹ�"
    return text

def selectSemester(semesterNum):
    print "�л�ѧ�ڲ˵���......"
    time.sleep(5)
    #����ѡ��ѧ�ڵİ�
    geturl ='http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=2014&selectXq='+str(semesterNum)+'&selectTime=2014-05-30%2013:30~2014-06-07%2023:59'
    header = {  'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',        
    }
    data = {}
    #get��ȡѧ�ڿγ�
    text = getData(geturl,header,data)
    return text

def postData(posturl,headers,postData):
    postData = urllib.urlencode(postData)  #Post���ݱ���   
    request = urllib2.Request(posturl, postData, headers)#ͨ��urllib2�ṩ��request��������ָ��Url�������ǹ�������ݣ�����ɵ�¼���� 
    response = urllib2.urlopen(request)  
    text = response.read().decode('utf-8')
    return text

def getData(geturl,header,getData):
    getData = urllib.urlencode(getData)
    request = urllib2.Request(geturl, getData, header)
    response = urllib2.urlopen(request)
    text = response.read().decode('utf-8') 
    return text

def stateCheck(textValue):    
    text = textValue.encode('gbk')
    #if (text.find('�ɹ�ѡ��') != -1)or(text.find('�����Ƽ�') != -1):
    if (text.find('�ɹ�ѡ��') != -1)or(text.find('�����Ƽ�') != -1):
        return 0
    if text.find('����') != -1:
        return 1
    if text.find('ʧ��') != -1:
        return 2

def Mode1(semesterNum):
    s =  semesterNum
    text = selectSemester(s)
    #Ѱ�ҿ��ԡ������Ƽ����Ŀγ�
    print "==============\nģʽ1����ʼѡ��\n=============="
    courseList = []
    pattern = re.compile(r'\" onclick=\"selectThis\(\'.*\'')
    pos = 0
    m = pattern.search(text,pos)
    while m:
        pos = m.end()
        tempText = m.group()
        course = [tempText[23:31],tempText[34:51],tempText[54:56],1]
        courseList.append(course)
        m=pattern.search(text,pos)  #Ѱ����һ��
    times = 0
    success = 0
    total = len(courseList)
    while True:
        if total == 0:
            break
        time.sleep(1.5)
        times = times +1
        print "\n��"+str(times)+"��ѡ�Σ��Ѿ��ɹ�ѡ��"+str(success)+"��"
        for course in courseList:
            if 1 == course[3]:
            #����ѡ��post
                posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+course[1]+'&select_xkkclx='+course[2]+'&select_jhkcdm='+course[0]
                headers = { 'Host' : 'xk.urp.seu.edu.cn',
                        'Proxy-Connection' : 'keep-alive',
                        'Content-Length' : '2',
                        'Accept' : 'application/json, text/javascript, */*',
                        'Origin':'http://xk.urp.seu.edu.cn',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        }
                data = {'{}':''
                }
                #postѡ�ΰ�������ȡ����״̬
                flag = stateCheck(postData(posturl,headers,data))
                #����ѡ��״̬������Ϣ
                if 0 == flag:
                    course[3] = 0
                    success = success + 1
                    total = total - 1
                    print 'Nice, �γ�'+str(course[0])+" ѡ��ɹ�"
                if 1 == flag:
                    print '�γ�'+str(course[0])+" ��������"
                if 2 == flag:
                    print '�γ�'+str(course[0])+" ѡ��ʧ�ܣ�ԭ��δ֪"
       
def Mode2(semesterNum,courseName):
    s =  semesterNum
    text = selectSemester(s)
    print "==============\nģʽ2����ʼѡ��\n=============="
    #��ȡ���Ŀ�ҳ��
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    text = getData(geturl1,header1,data1)
    #����RE  
    #print text
    text = text.encode('utf-8') 
    pattern = (courseName+'.*?(\"8%\" id=\"(.{0,20})\" align)').decode('gbk').encode('utf-8')
    #��ȡ�γ̱��
    courseNo = re.findall(pattern,text,re.S)[0][1]
    #�������ݰ�
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+courseNo+'&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = { 
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
    data = {
            '{}':''
            }
    print "�ҿ�ʼѡ����,�γ̱�ţ�"+courseNo
    times = 0
    while True :
        #�ж��Ƿ�ѡ����
        times = times+1
        text = getData(geturl1,header1,data1)
        text = text.encode('utf-8')
        pattern2 = ('��ѡ(.{0,200})align=\"').decode('gbk').encode('utf-8')
        result = re.findall(pattern2,text,re.S)
        #print result
        success = len(result) #Ϊ0Ϊ���ɹ� ����
        if (0 != success)and(result[0].find(courseNo)!=-1):
            print "Nice���Ѿ�ѡ���γ�:"+courseNo
            break
        #����ѡ�ΰ�
        print "��"+str(times)+"�γ���ѡ��γ�"+courseNo+",����ûѡ����"
        postData(posturl,headers,data)
    return 
def postRw(courseNo):
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+courseNo+'&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = { 
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Content-Length' : '2',
                'Accept' : 'application/json, text/javascript, */*',
                'Origin':'http://xk.urp.seu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }
    data = {
            '{}':''
            }
    text = postData(posturl,headers,data)
    return text
def checkRwState(text):
    text = text.encode('gbk')
    if text.find('true') != -1:  #ѡ�γɹ�
        return 0
    if text.find('��������') != -1:
        return 1
    if text.find('��ͻ') != -1:
        return 2
    return
def Mode3(semester):
    s =  semester
    text = selectSemester(s)
    print "==============\nģʽ3����ʼѡ��\n=============="
    #��ȡ���Ŀ�ҳ��
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
                'Host' : 'xk.urp.seu.edu.cn',
                'Proxy-Connection' : 'keep-alive',
                'Accept' : 'application/json, text/javascript, */*',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                }   
    data1 = {}
    text = getData(geturl1,header1,data1)
    text = text.encode('utf-8')
    #��ȡ���еĿγ̱��
    pattern = ('\"8%\" id=\"(.{0,20})\" align').decode('gbk').encode('utf-8')
    courseList = re.findall(pattern,text,re.S)
    #print courseList 
    courseCtList =[]
    #�ҳ���ȥ����ͻ�Ŀγ�
    for course in courseList:
        backText = postRw(course)
        state = checkRwState(backText)
        if state == 2:
            courseCtList.append(course)
        if state == 0:
            print "Nice ѡ����һ�ſΣ�"+course
            return   #�ɹ���
    #print courseCtList
    courseTemp = [i for i in courseList if (i not in courseCtList)]
    #print courseTemp
    times = 0
    while True:
        times = times + 1
        #�ҳ������Ŀγ�
        pattern = ('����.+?(\"8%\" id=\")(.{0,20})\" align').decode('gbk').encode('utf-8')
        courseYmList = [i[1] for i in re.findall(pattern,text,re.S)]
        #print courseYmList
        #�ҳ�����ѡ�Ŀγ̱��
        courseAva = [i for i in courseTemp if (i not in courseYmList) ]
        print courseAva
        #ѡ����
        if len(courseAva) == 0:
                    print "��"+str(times)+"��ˢ�£�ÿ�ſζ�ѡ����.."
        else:
            for course in courseAva:
                state = checkRwState(postRw(course))
                if 0 == state:
                    print "Nice ѡ����һ�ſΣ�"+course
                    return
                if 1 == state:
                    print "��Ʒ���� ��Ƥ�ӵ��µĿα�����"
        #ˢ������ѡ�ν���
        text = getData(geturl1,header1,data1)
        text = text.encode('utf-8')
        time.sleep(2)

    


if __name__ == "__main__":
    print "\n\n\n\n"
    print "===================================================================== "
    print "                    Seu_Jwc_Fker ���ϴ�ѧѡ������\n"
    print "     ���� github.com/SnoozeZ/seu_jwc_fker ���˽Ȿ���ߵ����¶�̬"
    print "===================================================================== "
    print "��ѡ��ģʽ��"
    print "1. ͬԺ����������ģʽ��ֵֻ�������汾Ժ�����С������Ƽ����γ�"
    print "2. ��עһ��ģʽ��ֵֻ���ӽ��桰��������ࡱ����ָ��һ�ſγ�"
    print "3. ����ģʽ��ֵ���ӽ��桰��������ࡱ����һ�ſγ̣���ʣ���ѡ��"
    #print "4. ֵֻ���ӽ��桰��Ȼ��ѧ�뼼����ѧ�ࡱ�е�ָ��һ�ſγ̣������У�"
    #print "5. ����ָ�������ſγ̵����ֲ�ֵ�أ��γ����Ͳ��ޣ��������У�"
    mode = input('\n������ģʽ���(��:1)��')
    userId = raw_input('������һ��ͨ��(��:213111111)��')
    passWord = raw_input('����������(��:65535)��')
    semester = input('������ѧ�ڱ��(��ѧ��Ϊ1����ѧ��Ϊ2)��')
    if 1 == mode:
        loginIn(userId,passWord)
        Mode1(semester)
    if 2 == mode:
        courseName = raw_input('����������ֵ�ص����Ŀ����ƻ�����ؼ��ʣ���:���ּ��ͣ���')
        loginIn(userId,passWord)
        Mode2(semester,courseName)
    if 3 == mode:
        loginIn(userId,passWord)
        Mode3(semester)