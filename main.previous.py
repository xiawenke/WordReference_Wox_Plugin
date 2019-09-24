# -*- coding: utf-8 -*-
# 固定写法，导入相关类库和函数
from util import WoxEx, WoxAPI, load_module, Log
import urllib

# 统一加载模块
with load_module():
    import pyperclip
    import requests
    import webbrowser



class Main(WoxEx):  # 继承WoxEx

    def query(self, keyword):

        thisWord       = 'Unset'
        thisDefinition = 'Unavailable'
        gotoURL        = 'http://www.wordreference.com/'
        apiUrl         = 'http://wr.miku-miku.online/?url=&URL&'
        results        = list()

        # 对keywords空格分隔
        seperatedKeys = keyword.split(' ')
        thisDefinition = 'Go on search with keywords.'

        if len(seperatedKeys) > 0 :
            # 若有指定语言
            langDict = {
                'zy'  :   'zhen',   #中英
                'yz'  :   'enzh'    #英中
            }
            specifiedLang = seperatedKeys[0]
            if(specifiedLang in langDict):
                thisDefinition = "Set specific language ["+specifiedLang+']'
                if len(seperatedKeys) > 1 :
                    thisWord = seperatedKeys[1]
                    thisLang = langDict[specifiedLang]
                    thisDefinition = 'Click to Search '+thisWord

                    # Establish API Connection...
                    gotoURL = 'https://www.wordreference.com/'+thisLang+'/'+urllib.parse.quote(thisWord)
                    try:
                        apiReturn = requests.get(apiUrl.replace('&URL&', gotoURL))
                        apiReturn = apiReturn.text
                    except Exception as identifier:
                        # Maybe A NetWork Error.
                        apiReturn = '0'

                    # Make Sure if there's a result.
                    if (apiReturn != 'Array') & (apiReturn != '0'):
                        apiReturn  = apiReturn.split("|")
                        for thisApiReturn in apiReturn:
                            if(thisApiReturn != 'Array'):
                                thisReturn     = thisApiReturn.split('%'+'%')
                                thisWord       = thisReturn[0]
                                thisDefinition = thisReturn[1]

                                results.append({
                                    "Title": thisWord,
                                    "SubTitle": thisDefinition,
                                    "IcoPath": "Images/ico.ico",
                                    "JsonRPCAction": {
                                        "method": "GoOn",
                                        "parameters": [gotoURL],
                                        "dontHideAfterAction": False
                                    }
                                })

                    # NetWork Error State.
                    elif apiReturn == '0':
                        thisWord       = 'NetWork Error'
                        thisDefinition = 'Please check the network connection...'
                        results.append({
                            "Title": thisWord,
                            "SubTitle": thisDefinition,
                            "IcoPath": "Images/ico.ico",
                            "JsonRPCAction": {
                                "method": "GoOn",
                                "parameters": [gotoURL],
                                "dontHideAfterAction": False
                            }
                        })
                            
                    # Word Not Found State.
                    else:
                        thisDefinition = 'Definition Not Found. (Click to go details)'
                        results.append({
                            "Title": thisWord,
                            "SubTitle": thisDefinition,
                            "IcoPath": "Images/ico.ico",
                            "JsonRPCAction": {
                                "method": "GoOn",
                                "parameters": [gotoURL],
                                "dontHideAfterAction": False
                            }
                        })

        return results

    def GoOn(self, keyword):
        webbrowser.open(keyword)
        pyperclip.copy(keyword)


if __name__ == "__main__":
    Main()