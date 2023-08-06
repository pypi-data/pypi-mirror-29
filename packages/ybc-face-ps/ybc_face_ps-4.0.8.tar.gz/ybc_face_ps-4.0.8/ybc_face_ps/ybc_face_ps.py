import requests
import json
import base64
import os
import math


def meizhuang(filename='', cosmetic=1):
    '''人脸美妆'''
    if not filename:
        return -1
    if cosmetic < 1:
        cosmetic = 1
    if cosmetic > 23:
        cosmetic = 23
    url = 'https://www.phpfamily.org/faceCosmetic.php'
    filepath = os.path.abspath(filename)
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['cosmetic'] = cosmetic
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = filename + '_meizhuang.jpg'
        with open(new_file,'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        return new_file
    else:
        return -1

def meizhuang_type():
    '''获取美妆类型'''
    MEIZHUANG_TYPE = {
    1:'日系妆-芭比粉',
    13:'韩妆-玫瑰',
    2:'日系妆-清透',
    14:'裸妆-自然',
    3:'日系妆-烟灰',
    15:'裸妆-清透',
    4:'日系妆-自然',
    16:'裸妆-桃粉',
    5:'日系妆-樱花粉',
    17:'裸妆-橘粉',
    6:'日系妆-原宿红',
    18:'裸妆-春夏',
    7:'韩妆-闪亮',
    19:'裸妆-秋冬',
    8:'韩妆-粉紫',
    20:'主题妆-经典复古',
    9:'韩妆-粉嫩',
    21:'主题妆-性感混血',
    10:'韩妆-自然',
    22:'主题妆-炫彩明眸',
    11:'韩妆-清透',
    23:'主题妆-紫色魅惑',
    12:'韩妆-大地色'
    }
    return MEIZHUANG_TYPE
'''人脸变妆'''
def bianzhuang(filename='', decoration=1):
    if not filename:
        return -1
    if decoration < 1:
        decoration = 1
    if decoration > 22:
        decoration = 22
    url = 'https://www.phpfamily.org/faceDecoration.php'
    filepath = os.path.abspath(filename)
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['decoration'] = decoration
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = filename + '_bianzhuang.jpg'
        with open(new_file,'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        return new_file
    else:
        return -1

def bianzhuang_type():
    '''获取美妆类型'''
    BIANZHUANG_TYPE = {
    1:'埃及妆',
    2:'巴西土著妆',
    3:'灰姑娘妆',
    4:'恶魔妆',
    5:'武媚娘妆',
    6:'星光薰衣草',
    7:'花千骨',
    8:'僵尸妆',
    9:'爱国妆',
    10:'小胡子妆',
    11:'美羊羊妆',
    12:'火影鸣人妆',
    13:'刀马旦妆',
    14:'泡泡妆',
    15:'桃花妆',
    16:'女皇妆',
    17:'权志龙',
    18:'撩妹妆',
    19:'印第安妆',
    20:'印度妆',
    21:'萌兔妆',
    22:'大圣妆'
    }
    return BIANZHUANG_TYPE

def ronghe(filename='', model=5):
    '''人脸融合'''
    if not filename:
        return -1
    if model < 1:
        model = 1
    if model > 50:
        model = 50
    url = 'https://www.phpfamily.org/faceMerge.php'
    filepath = os.path.abspath(filename)
    b64img= base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
    data = {}
    data['b64img'] = b64img
    data['model'] = model
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = filename + '_ronghe.jpg'
        with open(new_file,'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        return new_file
    else:
        return -1

def ronghe_type():
    RONGHE_TYPE = {
	1: '奇迹',
	2: '压岁钱',
	3: '范蠡',
	4: '李白',
	5: '孙尚香',
	6: '花无缺',
	7: '西施',
	8: '杨玉环',
	9: '白浅',
	10: '凤九',
	11: '夜华',
	12: '年年有余',
	13: '新年萌萌哒',
	14: '王者荣耀荆轲',
	15: '王者荣耀李白',
	16: '王者荣耀哪吒',
	17: '王者荣耀王昭君',
	18: '王者荣耀甄姬',
	19: '王者荣耀诸葛亮',
	20: '赵灵儿',
	21: '李逍遥',
	22: '爆炸头',
	23: '村姑',
	24: '光头',
	25: '呵呵哒',
	26: '肌肉',
	27: '肉山',
	28: '机智',
	29: '1927年军装（男）',
	30: '1927年军装（女）',
	31: '1929年军装（男）',
	32: '1929年军装（女）',
	33: '1937年军装（男）',
	34: '1937年军装（女）',
	35: '1948年军装（男）',
	36: '1948年军装（女）',
	37: '1950年军装（男）',
	38: '1950年军装（女）',
	39: '1955年军装（男）',
	40: '1955年军装（女）',
	41: '1965年军装（男）',
	42: '1965年军装（女）',
	43: '1985年军装（男）',
	44: '1985年军装（女）',
	45: '1987年军装（男）',
	46: '1987年军装（女）',
	47: '1999年军装（男）',
	48: '1999年军装（女）',
	49: '2007年军装（男）',
	50: '2007年军装（女）'
    }
    return RONGHE_TYPE

def main():
    res = meizhuang('1.jpg',23)
    print(res)
    res = bianzhuang('1.jpg')
    print(res)
    res = ronghe('1.jpg')
    print(res)
if __name__ == '__main__':
    main()
