import requests
import re
from lxml import etree

start_url = 'https://cd.esf.fang.com/chushou/3_210242832.htm'
html = requests.get(start_url).text
# print(html)
# re提取url参数部分，并拼接出url
real_url = start_url + '?' + re.findall(r't3=\'(.*?)\'', html)[0]
print('real_url:', real_url)
# response = requests.get(real_url).text
# xpath提取标题
# title = etree.HTML(response).xpath('//*[@id="lpname"]/h1/span')
# print('title:', title)