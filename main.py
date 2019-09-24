# -*- coding: utf-8 -*-

from util import WoxEx, WoxAPI, load_module, Log
import urllib


#######################
#   LOADING MODULES   #
#######################

with load_module():
    import pyperclip
    import requests
    import webbrowser
    from os import path



class Main(WoxEx):  # 继承WoxEx

    def query(self, keyword):

        ################################
        #     PROCESS CONFIG FILES     #
        ################################

        ### config.txt ###
        try:
            configOpen  = open('config.txt')
            configLines = configOpen.readline()
            while configLines :   
                config = configLines.split()
                
                if config[0] == 'DefaultDictionary:' :
                    DefaultDictionaryVar = config[1]

                if config[0] == 'APIUrl:' :
                    APIUrlVar = config[1]

                configLines = configOpen.readline()   

            configOpen.close()
            
            DefaultDictionary = DefaultDictionaryVar
            APIUrl = APIUrlVar

        except Exception as identifier:
            # If the file not existed, create it. 
            DefaultDictionary = 'enzh'
            APIUrl = 'http://wr.miku-miku.online/'
            open('config.txt', 'w+').write("DefaultDictionary: enzh\nAPIUrl: http://wr.miku-miku.online/")

        ### LanguageList.wr ###
        try:
            lLOpen = open('LanguageList.wr')
            
            if ('###FILE_VALID###' in lLOpen.readline()) == 0 :
                raise RuntimeError('INVALID_LL')

            lLOpen.close()
            

        except Exception as identifier:
            # If the file not existed, download it. 
            recoveryURL = APIUrl + '?getLanguageList=True'
            try:
                LanguageList = requests.get(recoveryURL).text
            except Exception as identifier:
                # Maybe A NetWork Error.
                LanguageList = 'NULL'
            open('LanguageList.wr', 'w+').write(LanguageList)

        lLOpen = open('LanguageList.wr')
        lLLines = lLOpen.readline()
        lLPrepared = list()

        while lLLines: 
            thisLine = lLLines.split()
            for i in thisLine:
                lLPrepared.append(i)
            lLLines = lLOpen.readline()

        lLOpen.close()

        ############################
        #     PREPARE VARIBLES     #
        ############################

        thisWord       = 'Unset'
        thisDefinition = 'Unavailable'
        gotoURL        = 'http://www.wordreference.com/'
        apiUrl         = APIUrl + '?url=&URL&'
        apiUrlV2ByWord = APIUrl + '/?word=&WORD&'
        apiUrlV2ByDict = APIUrl + '/?word=&WORD&&dict=&DICT&'
        results        = list()

        ### Split Keywords ###
        seperatedKeys = keyword.split(' ')
        thisDefinition = 'Go on search with keywords.'

        if len(seperatedKeys) > 0 :
            
            ###########################
            #     ESTABLISH QUERY     #
            ###########################            

            specifiedLang = seperatedKeys[0]

            ### Specific language ###
            if specifiedLang in lLPrepared :
                thisDefinition = "Set specific language ["+specifiedLang+']'
                if len(seperatedKeys) > 1 :
                    thisWord = seperatedKeys[1]
                    thisDefinition = 'Click to Search '+thisWord

                    # Establish API Connection...
                    try:
                        apiReturn = requests.get(apiUrlV2ByDict.replace('&WORD&', thisWord).replace('&DICT&', specifiedLang))
                        apiReturn = apiReturn.text
                    except Exception as identifier:
                        # Maybe A NetWork Error.
                        apiReturn = '0'

            ### Wrong Dictionary Name ###
            elif len(seperatedKeys) > 1:
                
                lLOpen = open('LanguageList.wr')
                lLLines = lLOpen.readline()
                lLLines = lLOpen.readline()
                thisLanguage = 'UNKNOWN_LANGUAGE'

                results.append({
                    "Title": 'Omm... Wrong Dictionary Name!',
                    "SubTitle": 'Check dictionaries below:',
                    "IcoPath": "Images/ico.ico",
                    "JsonRPCAction": {
                        "method": "GoOn",
                        "parameters": [APIUrl+'?getLanguageList=True'],
                        "dontHideAfterAction": False
                    }
                })

                # Show dictionaries.
                while lLLines: 
                    lLLines = lLLines.replace('\n', '')
                    if ('/**' in lLLines) or (len(lLLines) < 1) :
                        pass
                    else:
                        try:
                            splitedLl    = lLLines.split(' - ')
                            thisLanguage = splitedLl[0]
                            thisName     = splitedLl[1]
                        except Exception as identifier:
                            thisName     = lLLines
                            
                        results.append({
                            "Title": thisName,
                            "SubTitle": 'Command: wr '+thisLanguage+' <YOUR WORD>',
                            "IcoPath": "Images/ico.ico",
                            "JsonRPCAction": {
                                "method": "GoOn",
                                "parameters": [APIUrl+'?getLanguageList=True'],
                                "dontHideAfterAction": False
                            }
                        })
                    lLLines = lLOpen.readline()

                lLOpen.close()

            ### No specific language ###
            else:
                thisWord = specifiedLang
                # Establish API Connection...
                try:
                    apiReturn = requests.get(apiUrlV2ByDict.replace('&WORD&', thisWord).replace('&DICT&', DefaultDictionary))
                    apiReturn = apiReturn.text
                except Exception as identifier:
                    # Maybe A NetWork Error.
                    apiReturn = '0'
            

            #########################
            #     FETCH RESULTS     #
            #########################

            try:
                # Make Sure if there's a result.
                if (apiReturn != 'Array') & (apiReturn != '0'):
                    apiReturn  = apiReturn.split("|")
                    for thisApiReturn in apiReturn:
                        if(thisApiReturn != 'Array'):
                            thisReturn     = thisApiReturn.split('%'+'%')
                            thisWord       = thisReturn[0]
                            thisDefinition = thisReturn[1]
                            gotoURL        = thisReturn[2]

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

            except Exception as identifier:
                pass


        #################################
        #     NULL RESULTS RESPONSE     #
        #################################

        # If nothing in results, show the state.
        if len(results) == 0 :
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
