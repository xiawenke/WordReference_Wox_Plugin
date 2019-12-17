# -*- coding: utf-8 -*-

from util import WoxEx, WoxAPI, load_module, Log
import urllib

class Main(WoxEx):  # 继承WoxEx

    def query(self, keyword):

        results = list()

        #######################
        #   LOADING MODULES   #
        #######################

        with load_module():

            issetPyperclip  = True
            issetRequests   = True
            issetWebbrowser = True
            issetOs         = True
            
            try:
                import pyperclip
            except Exception as e:
                issetPyperclip = False

            try:
                import requests
            except Exception as e:
                issetRequests = False

            try:
                import webbrowser
            except Exception as e:
                issetWebbrowser = False

            try:
                from os import path
            except Exception as e:
                issetOs = False
            
            requirements = False

            if (issetRequests == False):
                if(requirements == False):
                    requirements = ''
                else:
                    requirements = requirements + ', '
                requirements = requirements + 'requests'

            if (issetOs == False):
                if(requirements == False):
                    requirements = ''
                else:
                    requirements = requirements + ', '
                requirements = requirements + 'os'
                
            suggestions = False

            if (issetPyperclip == False):
                if(suggestions == False):
                    suggestions = ''
                else:
                    suggestions = suggestions + ', '
                suggestions = suggestions + 'pyperclip'
                
            if (issetWebbrowser == False):
                if(suggestions == False):
                    suggestions = ''
                else:
                    suggestions = suggestions + ', '
                suggestions = suggestions + 'webbrowser'

            
            if requirements != False:
                results.append({
                    "Title": 'Following modules are needed to install:',
                    "SubTitle": 'Modules: ' + requirements + '. (ONLY MODULES ARE INSTALLED, THE PLUGIN CAN PERFORMING SUCCESSFUALLY. )',
                    "IcoPath": "Images/ico.ico",
                    "JsonRPCAction": {
                        "method": "GoOn",
                        "parameters": ['https://github.com/xiawenke/WordReference_Wox_Plugin', issetWebbrowser, issetPyperclip],
                        "dontHideAfterAction": False
                    }
                })
                return results
                
            if (suggestions != False) and (len(keyword.split()) == 0):
                results.append({
                    "Title": '--------- Recommended Plugin Installation ---------',
                    "SubTitle": 'Modules: ' + suggestions + '. (Only those modules are installed, the plugin can perform its full features.)',
                    "IcoPath": "Images/ico.ico",
                    "JsonRPCAction": {
                        "method": "GoOn",
                        "parameters": ['https://github.com/xiawenke/WordReference_Wox_Plugin', issetWebbrowser, issetPyperclip],
                        "dontHideAfterAction": False
                    }
                })
                

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
        GitHubLink     = 'https://github.com/xiawenke/WordReference_Wox_Plugin'
        apiUrl         = APIUrl + '?url=&URL&'
        apiUrlV2ByWord = APIUrl + '/?word=&WORD&'
        apiUrlV2ByDict = APIUrl + '/?word=&WORD&&dict=&DICT&'

        ### Split Keywords ###
        seperatedKeys = keyword.split()
        thisDefinition = 'Go on search with keywords.'

        ### Show User Manual ###
        if len(seperatedKeys) == 0 : 
            supportedCommands = list()
            supportedCommands.append({
                'Name'    : 'Simple Search (Using Default Dictionary)',
                'Command' : 'Command: wr <Word> | Example: wr hello'
            })
            supportedCommands.append({
                'Name'    : 'Simple Search (Using Specific Dictionary)',
                'Command' : 'Command: wr <Dictionary> <Word> | Example: wr enja hello'
            })
            supportedCommands.append({
                'Name'    : 'Multi-Compare Seach (Using Default Dictionary)',
                'Command' : 'Command: wr [<Word1>, <Word2>, <...>] | Example: wr [program, code, software]'
            })
            supportedCommands.append({
                'Name'    : 'Multi-Compare Seach (Using Spechfic Dictionary)',
                'Command' : 'Command: wr [<Word1>(<Dict1>), <Word2>(<Dict2>), <...>(...)] | Example: wr [hello(enja), hello(enzh), world(enpt)]'
            })
            supportedCommands.append({
                'Name'    : 'Show All Supported Dictionaries',
                'Command' : 'Command: wr show dictionaries'
            })

            for thisCommand in supportedCommands:
                results.append({
                    "Title": thisCommand['Name'],
                    "SubTitle": thisCommand['Command'],
                    "IcoPath": "Images/ico.ico",
                    "JsonRPCAction": {
                        "method": "GoOn",
                        "parameters": [GitHubLink, issetWebbrowser, issetPyperclip],
                        "dontHideAfterAction": False
                    }
                })

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

            ### Word Comparing Search ###
            elif ('[' in specifiedLang) or ('【' in specifiedLang):

                multiList = keyword
                multiList = multiList.replace('，', ',').replace('【', '[').replace('】', ']').replace('（', '(').replace('）', ')')   # Chinese symbol support. 

                thisTitle = 'Muti-Searching: Syntax Error'
                thisSub   = 'Failed to interpret the command: ' + multiList
                thisP     = 'https://wordreference.com'

                try:
                    words = multiList.replace('[', '').replace(']', '').replace(' ','')
                    words = words.split(',')

                    ## Search words ##
                    for thisWord in words:

                        ## Specific Dictionary ##
                        try:
                            if ('(' in thisWord) and (')' in thisWord):
                                thisDictionary = thisWord[thisWord.find('(')+1: thisWord.find(')')]
                                thisWord       = thisWord.replace('(', '').replace(')', '').replace(thisDictionary, '')
                            else:
                                raise Exception('NO_CHOOSENED_DICT')
                        except Exception as identifier:
                            thisDictionary = DefaultDictionary

                        ## Establish Connection ##                        
                        try:
                            thisApiReturn = requests.get(apiUrlV2ByDict.replace('&WORD&', thisWord).replace('&DICT&', thisDictionary))
                            thisApiReturn = thisApiReturn.text
                        except Exception as identifier:
                            thisTitle = 'Connection Error...'
                            thisSub   = 'Check your internet connections.'
                        
                        thisApiReturn = thisApiReturn.split('|')
                        
                        ## Fetch Result ##
                        try:
                            thisDef  = thisApiReturn[1].split('%' + '%')
                            thisLink = thisDef[2]
                            thisDef  = thisDef[1]
                        except Exception as identifier:
                            thisDef  = 'No Definition.'
                            thisLink = 'https://wordreference.com'
                        
                        results.append({
                            "Title": thisWord,
                            "SubTitle": thisDef,
                            "IcoPath": "Images/ico.ico",
                            "JsonRPCAction": {
                                "method": "GoOn",
                                "parameters": [thisLink, issetWebbrowser, issetPyperclip],
                                "dontHideAfterAction": False
                            }
                        })
                        
                    
                    thisTitle = 'del'

                except Exception as identifier:
                    pass
                
                if thisTitle != 'del' :
                    results.append({
                        "Title": thisTitle,
                        "SubTitle": thisSub,
                        "IcoPath": "Images/ico.ico",
                        "JsonRPCAction": {
                            "method": "GoOn",
                            "parameters": [thisP, issetWebbrowser, issetPyperclip],
                            "dontHideAfterAction": False
                        }
                    })
            
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
                        "parameters": [APIUrl+'?getLanguageList=True', issetWebbrowser, issetPyperclip],
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
                                "parameters": [APIUrl+'?getLanguageList=True', issetWebbrowser, issetPyperclip],
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
                                    "parameters": [gotoURL, issetWebbrowser, issetPyperclip],
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
                            "parameters": [gotoURL, issetWebbrowser, issetPyperclip],
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
                            "parameters": [gotoURL, issetWebbrowser, issetPyperclip],
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
                    "parameters": [gotoURL, issetWebbrowser, issetPyperclip],
                    "dontHideAfterAction": False
                   }
            })

        return results

    def GoOn(self, keyword):
        
        #######################
        #   LOADING MODULES   #
        #######################

        with load_module():

            issetPyperclip  = True
            issetWebbrowser = True
            
            try:
                import pyperclip
            except Exception as e:
                issetPyperclip = False

            try:
                import webbrowser
            except Exception as e:
                issetWebbrowser = False
            
        if(issetWebbrowser):
            webbrowser.open(keyword)
        if(issetPyperclip): 
            pyperclip.copy(keyword)


if __name__ == "__main__":
    Main()
