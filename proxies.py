import json

_regions = {
    "印度尼西亚": "id",
    "波兰": "pl",
    "黎巴嫩": "lb",
    "巴基斯坦": "pk",
    "挪威": "no",
    "澳大利亚": "au",
    "孟加拉国": "bd",
    "牙买加": "jm",
    "印度": "in",
    "巴西": "br",
    "丹麦": "dk",
    "墨西哥": "mx",
    "哥伦比亚": "co",
    "菲律宾": "ph",
    "厄瓜多尔": "ec",
    "希腊": "gr",
    "中国澳门": "mo",
    "匈牙利": "hu",
    "委内瑞拉": "ve",
    "爱尔兰": "ie",
    "尼日利亚": "ng",
    "斯洛文尼亚": "si",
    "莫桑比克": "mz",
    "白俄罗斯": "by",
    "爱沙尼亚": "ee",
    "葡萄牙": "pt",
    "德国": "de",
    "叙利亚": "sy",
    "新加坡": "sg",
    "阿尔及利亚": "dz",
    "伊朗": "ir",
    "格鲁吉亚": "ge",
    "波黑": "ba",
    "尼泊尔": "np",
    "阿联酋": "ae",
    "奥地利": "at",
    "贝宁": "bj",
    "多米尼加": "do",
    "津巴布韦": "zw",
    "土耳其": "tr",
    "乌干达": "ug",
    "巴拉圭": "py",
    "阿富汗": "af",
    "卢森堡": "lu",
    "巴林": "bh",
    "阿曼": "om",
    "英国": "gb",
    "科威特": "kw",
    "立陶宛": "lt",
    "保加利亚": "bg",
    "中国": "cn",
    "塔吉克斯坦": "tj",
    "以色列": "il",
    "多哥": "tg",
    "秘鲁": "pe",
    "巴勒斯坦": "ps",
    "库拉索": "cw",
    "柬埔寨": "kh",
    "摩尔多瓦": "md",
    "吉尔吉斯斯坦": "kg",
    "黑山": "me",
    "冰岛": "is",
    "科特迪瓦": "ci",
    "安哥拉": "ao",
    "蒙古国": "mn",
    "刚果(布)": "cg",
    "波多黎各": "pr",
    "罗马尼亚": "ro",
    "捷克共和国": "cz",
    "卡塔尔": "qa",
    "意大利": "it",
    "克罗地亚": "hr",
    "中国台湾": "tw",
    "马来西亚": "my",
    "特立尼达和多巴哥": "tt",
    "伊拉克": "iq",
    "瑞士": "ch",
    "塞尔维亚": "rs",
    "哥斯达黎加": "cr",
    "萨尔瓦多": "sv",
    "中国香港": "hk",
    "斐济群岛": "fj",
    "西班牙": "es",
    "洪都拉斯": "hn",
    "肯尼亚": "ke",
    "瑞典": "se",
    "乌克兰": "ua",
    "南非": "za",
    "缅甸": "mm",
    "乌兹别克斯坦": "uz",
    "智利": "cl",
    "文莱": "bn",
    "拉脱维亚": "lv",
    "亚美尼亚": "am",
    "加纳": "gh",
    "荷兰": "nl",
    "美国": "us",
    "马里": "ml",
    "马其顿": "mk",
    "日本": "jp",
    "加拿大": "ca",
    "新西兰": "nz",
    "马达加斯加": "mg",
    "埃及": "eg",
    "韩国": "kr",
    "利比亚": "ly",
    "老挝": "la",
    "俄罗斯": "ru",
    "越南": "vn",
    "法国": "fr",
    "摩洛哥": "ma",
    "哈萨克斯坦": "kz",
    "斯洛伐克": "sk",
    "纳米比亚": "nan",
    "沙特阿拉伯": "sa",
    "玻利维亚": "bo",
    "瓜德罗普": "gp",
    "马尔代夫": "mv",
    "马耳他": "mt",
    "斯里兰卡": "lk",
    "阿根廷": "ar",
    "约旦": "jo",
    "泰国": "th",
    "巴拿马": "pa",
    "比利时": "be",
    "芬兰": "fi",
    "古巴": "cu",
}

# 非账号密码模式下，注意使用前需要在账户中将服务器IP添加到白名单中。
_IPIDEA_BASE_ENTRY = 'http://xmu308xmu2-zone-custom-region-{}:xmu308@proxy.ipidea.io:2334'
_IPIDEA_SESSION = ['xmu308xmu2-zone-custom-region-sg-session-122cz9cib-sessTime-30:xmu308@proxy.ipidea.io:2334'
                   'xmu308xmu2-zone-custom-region-sg-session-1220tdob7-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-12268ivua-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-122h41swg-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-1228eid2g-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-1220ghqzy-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-122nzjmw1-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-122lnstms-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-122gkradg-sessTime-30:xmu308@proxy.ipidea.io:2334',
                   'xmu308xmu2-zone-custom-region-sg-session-1226x2vta-sessTime-30:xmu308@proxy.ipidea.io:2334'
                   ]

_IPIPGO_FIXED = '8lcbk5:2mjk6fdq@45.32.119.219:42000'

_IPIPGO_FIXED_DC = [
    "xyfrqb:2jjcz3ih@38.177.116.239:42000"
]
# 账号密码模式
_IPIDEA_FIXED_DC = ['xmu308xmu2:xmu308@156.229.59.127:2333', 'xmu308xmu2:xmu308@156.229.59.111:2333',
                    'xmu308xmu2:xmu308@156.229.58.224:2333', 'xmu308xmu2:xmu308@156.229.57.191:2333',
                    'xmu308xmu2:xmu308@156.229.59.86:2333', 'xmu308xmu2:xmu308@156.229.58.177:2333',
                    'xmu308xmu2:xmu308@156.229.59.226:2333', 'xmu308xmu2:xmu308@156.229.57.213:2333',
                    'xmu308xmu2:xmu308@156.229.59.87:2333', 'xmu308xmu2:xmu308@156.229.56.209:2333']


def get_proxy(country_code='sg', pid=0, local_proxy=True):  # 注意要指定国家代码与服务器所在国家一致，这样的请求速度才是最快的，否则速度很慢还不如不用代理手动限速
    """

    :param country_code: 国家代码，目前可忽略；在有多个国家地区的代理池时需要选择与使用代理的服务器最近的那个国家
    :param pid: 人为分配的进程id：0～n，用来在每个进程中都取不同的代理
    :param local_proxy: 是否将本地服务器的IP也作为一个代理使用，默认True：pid=0时返回的代理为空，也就是直接通过本地网络请求
    :return:
    """
    # entry = _IPIDEA_BASE_ENTRY.format(country_code)
    # return {  # IPIDEA的代理，默认指定美国地区的代理池，其使用隧道方式，这个只是连接隧道；真实代理IP每次请求都会更换一个。
    #     'http': entry,
    #     'https': entry
    # }

    if local_proxy and pid == 0:
        return None
    entry = 'http://' + _IPIDEA_FIXED_DC[pid-1]
    return {
        'http': entry,
        'https': entry
    }
