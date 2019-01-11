import requests
from pyquery import PyQuery as pq
import json
import datetime
import time
import re
from tqdm import tqdm
class Bjharticle:
    def __init__(self):
        self.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                'Cookie':'BAIDUID=C0F239571F90268C0A34B27A8A6A0B73:FG=1; BIDUPSID=C0F239571F90268C0A34B27A8A6A0B73; PSTM=1540373237; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=pnbnAtYllXNldXcFBxSGt-Sm5qekFzUXZ6dFA2fmZMY1I3MXFTQVJEbEYwRDVjQUFBQUFBJCQAAAAAAAAAAAEAAADNI9BUcGdiZXZjcm0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEVDF1xFQxdcbF; H_PS_PSSID=27774_1444_21080_18560_28131_27750_27244_27509; BDSFRCVID=GGkOJeC62ulLQTb9y_q2o9AcPelg1XRTH6aIO5wFizSZdiyX7zHvEG0PqM8g0KubyeI3ogKKymOTHrAF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=tJujVIIhtI-3fP36q4OH5-o05eT22-usLH7T2hcH0KLKEI3N3j7ceq-uhhQyqxo2LIIton7wQUb1MRjv3pDahJ88QljtXqjmBmOTVl5TtUJaeCnTDMRh-lk_hqJyKMniMCj9-pn-0lQrh459XP68bTkA5bjZKxtq3mkjbIOFfDD2MDDGe5KKePFS-qb0b-4XKKOLsJO8fhji_p7_bf--Dx_DLJOg2jcUL2rQWKTpKMJqhlAx246xy5K_hprr3q5Cy67nbJbtBq5sjpTHQT3mKfrbbN3i-CrwbnTBWb3cW-TV8UbSKxQPBTD02-nBat-OQ6npaJ5nJq5nhMtRy6CaePD_Mf6054vKa-oa3RTeb6rjDnCrQPnTKUI8LPbO05JztbrHVlRm0CJcHqDG0qoI0J5yLp3ah6Olt2LEoCvtKRT8jJjd-tP_-4_tbh_X5-RLfbAJ54OF5lOTJh0RW6-KK6FT3b6JBURTWebu5fjKthO2H4IxQ6bke6jBDN-tq6Fef5vfL5rXbRrSjJjkKRoHh4It-fIX5-Cs3RkL2hcH0KLKfP-xMxrKefA75mcyqxo2LTnh2DnlJfb1MRjvLUC2K4IZjtc9LhcvB57w0l5TtUJ8SDnTDMRh-lF-WtcyKMniMCj9-pn-0lQrh459XP68bTkA5bjZKxtq3mkjbIOFfD_KhCP9j6uMenKtK2T0b4c824o2WbCQ3h3O8pcNLTDK5tAT0JOaqRcd-RryVljJLn5SeIjy0lO1j4_PXNof0tcELaQbB4T9J-c1fl5jDh3aXjksD-Rt5Jc-WR7y0hvcMR6cShn4LfjrDRLbXU6BK5vPbNcZ0l8K3l02VKO_e4bK-TrLjNLqJxK; delPer=0; PSINO=2'
            }
    def article(self, id):
        try:
            artjsurl = f'https://author.baidu.com/pipe?tab=2&app_id={id}&num=6&pagelets[]=article'
            response = requests.get(artjsurl,headers=self.headers).text
            p1 = re.compile(r'[(](.*)[)]', re.S)
            cutjson = re.findall(p1, response)
            global artjson
            artjson = json.loads(cutjson[0])
        except:
            print('%s链接解析出现错误' % id)
        try:
            if artjson['html'] == "   ":
                filename = 'baijiahaofail.txt'
                with open(filename, 'a') as f:
                    f.write(id + '\n')
                self.delid(id)  #删除空号id
            else:
                try:
                    url = 'https://author.baidu.com/list?type=article&context=' + '{' + f'%22app_id%22:%22{id}%22,%22pageSize%22:20' + '}'
                    global resp
                    resp = requests.get(url, headers=self.headers).json()
                except:
                    print('%s链接解析出现错误' % id)
                try:
                    items = resp['data']['items']
                    for item in items:
                        if items != [] and item['type'] == 'news':
                            PostPid = item['id']  # 文章ID
                            PostTitle = item['title']  # 文章标题
                            PostThumbnail = [x['src'] for x in item['cover_images']]  # 封面图
                            PostUrl = item['url']  # 文章url
                            PostPv = item['read_amount']  # 浏览量
                            PostType = 0  # 文章类型
                            content = requests.get(PostUrl, headers=self.headers).text
                            docsub = pq(content)
                            PostContent = str(docsub('#article > div.article-content'))  # 文章内容
                            CreatedAt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 采集时间
                            timestamp = item['updated_at']
                            time_local = time.localtime(timestamp)
                            PublishedAt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 文章发表时间
                            Typeid = 4
                            IsDeleted = 0
                            data = {
                                'PostPid': PostPid,
                                'PostTitle': PostTitle,
                                'PostThumbnail': PostThumbnail,
                                'PostUrl': PostUrl,
                                'PostPv': PostPv,
                                'PostType': PostType,
                                'PostContent': PostContent,
                                'ActAid': id,
                                'TypeId': Typeid,
                                'CreatedAt': CreatedAt,
                                'PublishedAt': PublishedAt,
                                'IsDeleted': IsDeleted
                            }
                            self.updata(data, id)  # 上传文章
                        else:
                            continue
                except Exception as e:
                    print('%s文章解析出现错误%s' % (id, e))
        except:
            print('%s判断页面为空出现错误' % id)
    #上传文章
    def updata(self, data, id):
        try:
            upapiurl = 'http://10.0.8.28:5000/Post/Add'
            requests.post(upapiurl, data=data)
        except Exception as e:
            print('%s 上传文章失败 %s' % (id, e))
    #删除ID
    def delid(self, id):
        try:
            delapiurl = 'http://10.0.8.28:5000/Account/Del'
            data = {
                'aid': id
            }
            requests.post(delapiurl, data=data)
            print('%s 删除成功' % id)
        except Exception as e:
            print('%s 删除出错 %s' % (id, e))

    def main(self):
        while 1:
            counturl = 'http://10.0.8.28:5000/Account/GetCount?typeid=4'
            resp = requests.get(counturl).text
            apiurl = f'http://10.0.8.28:5000/Account/GetAccounts?page=1&size={resp}&t=4'
            items = requests.get(apiurl).json()
            for item in tqdm(items):  # 进度条
                actaid = item['actAid']
                self.article(actaid)
if __name__ == '__main__':
    Bjharticle().main()