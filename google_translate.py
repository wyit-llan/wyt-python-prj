import re
import traceback
import time

import requests
from requests.exceptions import SSLError
from bs4 import BeautifulSoup

from log_zyb import simple_log_with_time
from proxies import get_proxy


class TranslateError(Exception):  # 翻译异常类，翻译出错直接抛出异常
    def __int__(self, *args):
        super().__init__(*args)


_LANGUAGES = {  # 支持的语言及其代码
    "检测语言": "auto",
    "阿尔巴尼亚语": "sq",
    "阿拉伯语": "ar",
    "阿姆哈拉语": "am",
    "阿萨姆语": "as",
    "阿塞拜疆语": "az",
    "埃维语": "ee",
    "艾马拉语": "ay",
    "爱尔兰语": "ga",
    "爱沙尼亚语": "et",
    "奥利亚语": "or",
    "奥罗莫语": "om",
    "巴斯克语": "eu",
    "白俄罗斯语": "be",
    "班巴拉语": "bm",
    "保加利亚语": "bg",
    "冰岛语": "is",
    "波兰语": "pl",
    "波斯尼亚语": "bs",
    "波斯语": "fa",
    "博杰普尔语": "bho",
    "布尔语(南非荷兰语)": "af",
    "鞑靼语": "tt",
    "丹麦语": "da",
    "德语": "de",
    "迪维希语": "dv",
    "蒂格尼亚语": "ti",
    "多格来语": "doi",
    "俄语": "ru",
    "法语": "fr",
    "梵语": "sa",
    "菲律宾语": "tl",
    "芬兰语": "fi",
    "弗里西语": "fy",
    "高棉语": "km",
    "格鲁吉亚语": "ka",
    "贡根语": "gom",
    "古吉拉特语": "gu",
    "瓜拉尼语": "gn",
    "哈萨克语": "kk",
    "海地克里奥尔语": "ht",
    "韩语": "ko",
    "豪萨语": "ha",
    "荷兰语": "nl",
    "吉尔吉斯语": "ky",
    "加利西亚语": "gl",
    "加泰罗尼亚语": "ca",
    "捷克语": "cs",
    "卡纳达语": "kn",
    "科西嘉语": "co",
    "克里奥尔语": "kri",
    "克罗地亚语": "hr",
    "克丘亚语": "qu",
    "库尔德语（库尔曼吉语）": "ku",
    "库尔德语（索拉尼）": "ckb",
    "拉丁语": "la",
    "拉脱维亚语": "lv",
    "老挝语": "lo",
    "立陶宛语": "lt",
    "林格拉语": "ln",
    "卢干达语": "lg",
    "卢森堡语": "lb",
    "卢旺达语": "rw",
    "罗马尼亚语": "ro",
    "马尔加什语": "mg",
    "马耳他语": "mt",
    "马拉地语": "mr",
    "马拉雅拉姆语": "ml",
    "马来语": "ms",
    "马其顿语": "mk",
    "迈蒂利语": "mai",
    "毛利语": "mi",
    "梅泰语（曼尼普尔语）": "mni",
    "蒙古语": "mn",
    "孟加拉语": "bn",
    "米佐语": "lus",
    "缅甸语": "my",
    "苗语": "hmn",
    "南非科萨语": "xh",
    "南非祖鲁语": "zu",
    "尼泊尔语": "ne",
    "挪威语": "no",
    "旁遮普语": "pa",
    "葡萄牙语": "pt",
    "普什图语": "ps",
    "齐切瓦语": "ny",
    "契维语": "ak",
    "日语": "ja",
    "瑞典语": "sv",
    "萨摩亚语": "sm",
    "塞尔维亚语": "sr",
    "塞佩蒂语": "nso",
    "塞索托语": "st",
    "僧伽罗语": "si",
    "世界语": "eo",
    "斯洛伐克语": "sk",
    "斯洛文尼亚语": "sl",
    "斯瓦希里语": "sw",
    "苏格兰盖尔语": "gd",
    "宿务语": "ceb",
    "索马里语": "so",
    "塔吉克语": "tg",
    "泰卢固语": "te",
    "泰米尔语": "ta",
    "泰语": "th",
    "土耳其语": "tr",
    "土库曼语": "tk",
    "威尔士语": "cy",
    "维吾尔语": "ug",
    "乌尔都语": "ur",
    "乌克兰语": "uk",
    "乌兹别克语": "uz",
    "西班牙语": "es",
    "希伯来语": "iw",
    "希腊语": "el",
    "夏威夷语": "haw",
    "信德语": "sd",
    "匈牙利语": "hu",
    "修纳语": "sn",
    "亚美尼亚语": "hy",
    "伊博语": "ig",
    "伊洛卡诺语": "ilo",
    "意大利语": "it",
    "意第绪语": "yi",
    "印地语": "hi",
    "印尼巽他语": "su",
    "印尼语": "id",
    "印尼爪哇语": "jw",
    "英语": "en",
    "约鲁巴语": "yo",
    "越南语": "vi",
    "中文": "zh",
    "宗加语": "ts"
}

_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

# _ID: int = os.getppid()  # 唯一ID：当翻译失败等待并重试时会有较长时间的阻塞，此时在某个目录下创建诸如'translate_ID'这样的文件夹告诉其他进程这是翻译阻塞，如果翻译成功就删掉该文件夹
_BASE_URL = 'https://translate.google.com/m'  # 移动端谷歌翻译接口，参数：tl=...&sl=...&q=...

_TRANSLATE_ESCAPE = '^$'  # 转义字符：对于翻译文本用不影响翻译的转译字符替代换行符，可以避免某些因为换行而产生的翻译错误，比如"Turkey \n and the United States"会被翻译成"火鸡..."
_REQUEST_COUNT = 0  # 累计请求次数，方便debug和优化程序
_request_limited = False  # 是否被限制IP
_PID: int  # 手动分配的进程id，用来取代理，范围0-n（n为进程数）


def get_languages():
    """返回支持的语言和对应的英文代码"""
    return _LANGUAGES


def _search_last_sentence_index(text: str):
    """从右向左搜索句子的分隔符（?.!？！。,，）并返回索引，也就是找到有多个完整句子（包括逗号子句）组成的最长子串，索引之后的字符串非完整句子"""
    r = list(re.finditer('\.[^\d]|\?|!|\.$|？|,[^\d]|,$|！|。|，', text))  # 注意.后不能有数字与小数点区分开，,之后也不能有数字与千分号记数区别
    return r[-1].start() if r else -1


# 分段翻译
def _split_long_text(text: str, max_length=2048):
    """拆分长文本，因为翻译接口最多单次只能承载max_length个字符

    :param text:
    :param max_length: 最大字符串长度
    :return:
    """
    if len(text) <= max_length:
        return [text]
    start_index = 0
    texts = []
    while start_index < len(text):
        if len(text) - start_index <= max_length:  # 如果剩下的字符串没有超过最大长度就直接划为一个子串
            texts.append(text[start_index:])
            break
        max_sentence_index = _search_last_sentence_index(text[start_index:start_index + max_length])
        if max_sentence_index != -1:
            texts.append(text[start_index:start_index + max_sentence_index + 1])  # 注意子句包括句子符号
            start_index = start_index + max_sentence_index + 1
        else:  # 如果没有逗号句号等任何句子分隔，直接截断
            texts.append(text[start_index:start_index + max_length])
            start_index = start_index + max_length
    return texts


def google_translate(query: str, target_language="zh-CN", src_language="auto", proxy=False, local_proxy=True, interval=1, pid=None):
    """

    :param query: 翻译文本
    :param target_language: 目标语言
    :param src_language: 源语言，默认'auto'代表自动检测
    :param proxy: 是否使用代理
    :param local_proxy: 如果使用代理的话，是否将本机IP当作其中一个代理，是的话其中一个代理为空，也就是直接使用本机发起网络请求
    :param interval: 如果不使用代理的话，两次请求之间间隔的秒数，默认为1；注意：同一个IP最多只支持10个并发请求，超过就会被封，
    所以无代理的情况下或同一个IP不要超过10个进程同时使用这个接口。由于谷歌接口最大不被封速率是10次/s的请求，所以如果并发进程数小于10，可以调小interval。
    比如只有2个进程并发，一个进程允许在1s内有5次请求，则可以调整为0.2。不论这个值为多少，都不能有超过10个进程并发。
    :param pid: 手动分配的进程id，用来取代理，范围0-n（n为进程数），仅在使用代理且不为None的情况下有效。也可以通过赋值给模块变量_PID达到同样的作用。
    :return:
    """
    global _REQUEST_COUNT, _PID
    if not query:
        return query
    if pid:
        _PID = pid
    error_times = 0
    max_try_times = 19  # 出现错误时最大尝试次数，按照平方递增间隔，19次正好可以渡过封禁时间段(大概40min)，这个参数仅在不使用代理的情况下有效
    effective_str = query.rstrip()  # 去除末尾的\n\t之类的空白符号，避免特殊且情况下的一次空请求：比如句子长度2049，最后一个是换行，此时会被划分为一个长2048的子句和一个单独的换行符
    if not effective_str:  # 如果只有空白符号就直接返回
        return query
    effective_length = len(effective_str)
    # 转译中间的换行符，使其不影响翻译，比如Turkey \n and USA第一个词会被翻译成火鸡，转义后不会。注意不能在翻译前直接把单词替换为中文，这样谷歌接口可能会返回原文。
    effective_str = effective_str.replace('\n', _TRANSLATE_ESCAPE)
    texts = _split_long_text(effective_str)
    params = {
        'tl': target_language,
        'sl': src_language,
        'q': ''
    }
    translate_results = ''
    for text in texts:
        ori_text = text
        params['q'] = text
        while error_times < max_try_times or proxy:  # 仅在不使用代理的情况下才会有错误次数限制
            try:
                _REQUEST_COUNT += 1
                if proxy:
                    result = requests.get(_BASE_URL, params=params, headers=_headers, timeout=20, proxies=get_proxy(pid=_PID, local_proxy=local_proxy))
                else:
                    result = requests.get(_BASE_URL, params=params, headers=_headers, timeout=20)
                    time.sleep(interval)
                result.raise_for_status()
            except SSLError:  # 多个进程并发使用代理的时候可能会出现这个错误，握手出现问题，重新请求即可
                simple_log_with_time(f'Translate(request) Error: SSLError. Trying again...')
                continue
            except Exception as e:
                simple_log_with_time(f'Translate(request) Error: {str(e)}. ' + 'Sleeping...' if not proxy else '')
                if not proxy:
                    error_times += 1
                    time.sleep(error_times ** 2)
                continue

            html = result.text
            soup = BeautifulSoup(html, 'html.parser')
            try:
                trans_res = soup.find_all(class_='result-container')[0].text
            except Exception as e:  # 有时候报错：list index out od range...malformed request。多发生于文件翻译完之后的摘要翻译之类的，可能是摘要提取的问题
                # 例如泰语文件423707，摘要字符串本身没问题，但翻译会出问题，后面一小部分（没有实际意义）删除后就不会出问题，有问题的部分各自翻译又是可行的
                simple_log_with_time(f'({_PID})Translate(parse HTML) error: {str(e)}.')
                simple_log_with_time(f'text(to {target_language}): {text}')
                print(f'html: {html}')
                traceback.print_exc()

                if 'unusual traffic' in html:  # IP被谷歌限制了
                    simple_log_with_time('Possibly limited! Sleeping 5s...')
                    time.sleep(5)
                    continue

                if len(text) >= 10:
                    text = text[:int(0.9 * len(text))]  # 直接截断1/10的长度以去除出错的字符，直到不出错或者长度<10为止
                    params['q'] = text
                    error_times += 1
                    continue
                else:
                    trans_res = ori_text  # 实在翻译不了就返回原文

            translate_results += trans_res if trans_res else ''
            break

        if error_times == max_try_times:
            raise TranslateError('Translate Error: tried too much times.')

    translate_results = translate_results.replace(_TRANSLATE_ESCAPE, '\n')
    return translate_results if effective_length == len(query) else (translate_results + query[effective_length:])  # 还原末尾的空白符号

