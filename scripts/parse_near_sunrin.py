from pickle import dump
from requests import get
from xml.dom import minidom

from sunrinseed.settings.local_nero import DAUM_API_KEY, NAVER_API_HEADERS


def get_location_by_naver(addr):
    url = "https://openapi.naver.com/v1/map/geocode?encoding=utf-8&coord=latlng&output=json&query={}"
    headers = NAVER_API_HEADERS

    json = get(url.format(addr), headers=headers).json()
    try:
        item = json['result']['items'][0]
    except (IndexError, KeyError):
        return False

    full_addr = item['address']
    addr_detail = item['addrdetail']
    sido = addr_detail['sido']
    sigugun = addr_detail['sigugun']
    dongmyun = addr_detail['dongmyun']
    point = item['point']
    lng = point['x']
    lat = point['y']
    return lng, lat, sido, sigugun, dongmyun, full_addr


def get_gps_by_mapxy(mapx, mapy):
    url = "http://apis.daum.net/local/geo/transcoord?apikey={}&x={}&y={}&fromCoord=ktm&toCoord=WGS84".format(
        DAUM_API_KEY, mapx, mapy
    )
    html = get(url).content
    doc = minidom.parseString(html)
    elem = doc.getElementsByTagName("result")[0]
    x = elem.getAttribute("x")
    y = elem.getAttribute("y")
    return float(x), float(y)


def get_info_by_name(name):
    url = "https://openapi.naver.com/v1/search/local.xml?query={}"
    headers = NAVER_API_HEADERS
    html = get(url.format(name), headers=headers).content
    doc = minidom.parseString(html)
    info = {}
    try:
        info['title'] = doc.getElementsByTagName("title")[1].firstChild.nodeValue
    except IndexError:
        info['title'] = doc.getElementsByTagName("title")[0].firstChild.nodeValue
    try:
        info['telephone'] = doc.getElementsByTagName("telephone")[0].firstChild.nodeValue
    except IndexError:
        info['telephone'] = ''
    except AttributeError:
        info['telephone'] = ''
    try:
        info['addr'] = doc.getElementsByTagName("address")[0].firstChild.nodeValue
        info['category'] = doc.getElementsByTagName("category")[0].firstChild.nodeValue
        info['x'] = doc.getElementsByTagName("mapx")[0].firstChild.nodeValue
        info['y'] = doc.getElementsByTagName("mapy")[0].firstChild.nodeValue
    except IndexError:
        print("error, %s" % name)
        with open("error.txt", "a") as fp:
            fp.write(name + "\n")
    except AttributeError:
        print(html)
    return info


def run():
    places = [
        "육쌈냉면", '마카나이',
        '스타벅스', '투썸플레이스',
        '커피니', '알촌',
        '코피티암', '서울쌈냉면',
        '엉터리생고기',
        '쓰리팝피시방', '롯데리아',
        "KFC", "대관령목장",
        "굿뉴스", "정가할인마트",
        "빨강떡볶이", "진영각",
        "알파문구", "위아더월드 노래방",
        "달려라팬", "신내떡",
        "닌자초밥", "홍콩반점",
        "맘스터치", "빨봉분식",
        "두끼", "카니발피자",
        "국수나무", "할머니국수",
        "가마로강정", "까치네",
    ]
    data_list = []
    for idx, place in enumerate(places):
        info = get_info_by_name("숙대 {}".format(place))
        try:
            info['x'], info['y'] = get_gps_by_mapxy(info['x'], info['y'])
        except KeyError:
            continue

        data_list.append(info)
    print(data_list)
    with open("place_tmp_saved.txt", "w") as fp:
        dump(data_list, fp)
