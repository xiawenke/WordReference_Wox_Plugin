# -*- coding: utf-8 -*-
# 固定写法，导入相关类库和函数
from util import WoxEx, WoxAPI, load_module, Log

# 统一加载模块
with load_module():
    import pyperclip
    import requests
    import webbrowser



class Main(WoxEx):  # 继承WoxEx

    def query(self, keyword):

        thisWord       = 'Unset'
        thisDefinition = 'Unavailable'

        #对keywords空格分隔
        seperatedKeys = keyword.split(' ')
        thisDefinition = 'Go on search with keywords.'

        if(len(seperatedKeys) > 0):
            #若有指定语言
            langDict = {
                'zy'  :   'zhen',   #中英
                'yz'  :   'enzh'    #英中
            }
            specifiedLang = seperatedKeys[0]
            if(specifiedLang in langDict):
                thisDefinition = "Set specific language ["+specifiedLang+']'
                if(len(seperatedKeys) > 1):
                    thisWord = seperatedKeys[1]
                    thisLang = langDict[specifiedLang]
                    thisDefinition = 'Click to Search '+thisWord

                    gotoURL = 'http://www.wordreference.com/'+thisLang+'/'+thisWord
                    #r = requests.get(gotoURL)
                    #open('C:/Users/Wenky/AppData/Local/Wox/app-1.3.578/Plugins/Wox.Plugin.WordReference/text.txt', 'wb').write(r.text.encode('utf-8'))
            
        

        #返回结果
        results = list()
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
