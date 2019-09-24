<?php

/**
 * Curl Obtainnin WebData
 * @param $url
 * @return mixed
 * @author https://blog.csdn.net/flysnownet/article/details/90025384
 */
function get_url($url)
{
    $ifpost = 0;
    $datafields = '';
    $cookiefile = '';
    $v = false;

    // Generate Random IP Address
    $ip_long = array(
        array('607649792', '608174079'), //36.56.0.0-36.63.255.255
        array('1038614528', '1039007743'), //61.232.0.0-61.237.255.255
        array('1783627776', '1784676351'), //106.80.0.0-106.95.255.255
        array('2035023872', '2035154943'), //121.76.0.0-121.77.255.255
        array('2078801920', '2079064063'), //123.232.0.0-123.235.255.255
        array('-1950089216', '-1948778497'), //139.196.0.0-139.215.255.255
        array('-1425539072', '-1425014785'), //171.8.0.0-171.15.255.255
        array('-1236271104', '-1235419137'), //182.80.0.0-182.92.255.255
        array('-770113536', '-768606209'), //210.25.0.0-210.47.255.255
        array('-569376768', '-564133889'), //222.16.0.0-222.95.255.255
    );
    $rand_key = mt_rand(0, 9);
    $ip= long2ip(mt_rand($ip_long[$rand_key][0], $ip_long[$rand_key][1]));
    
    // Simulate HTTP Header
    $header = array("Connection: Keep-Alive","Accept: text/html, application/xhtml+xml, */*", "Pragma: no-cache", "Accept-Language: zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3","User-Agent: Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)",'CLIENT-IP:'.$ip,'X-FORWARDED-FOR:'.$ip);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, $v);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
    $ifpost && curl_setopt($ch, CURLOPT_POST, $ifpost);
    $ifpost && curl_setopt($ch, CURLOPT_POSTFIELDS, $datafields);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    $cookiefile && curl_setopt($ch, CURLOPT_COOKIEFILE, $cookiefile);
    $cookiefile && curl_setopt($ch, CURLOPT_COOKIEJAR, $cookiefile);
    curl_setopt($ch,CURLOPT_TIMEOUT,60);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    $ok = curl_exec($ch);
    curl_close($ch);
    unset($ch);
    return $ok;
}

function link_urldecode($url) {
    $uri = '';
    $cs = unpack('C*', $url);
    $len = count($cs);
    for ($i=1; $i<=$len; $i++) {
      $uri .= $cs[$i] > 127 ? '%'.strtoupper(dechex($cs[$i])) : $url{$i-1};
    }
    return $uri;
}

/** ====================== */
/** RESPONCE TO EXCEPTIONS */
/** ====================== */

$dictList = array(
    /** Spanish */
    'enes',     // English-Spanish
    'esen',     // Spanish-English
    'esfr',     // Spanish-French
    'espt',     // Spanish-Portuguese
    'esit',     // Spanish-Italian
    'esde',     // Spanish-German
    'eses',     // Spanish: definition
    'essin',    // Spanish: synonyms
    'esconj',   // Spanish: conjugations

    /** French */
    'enfr',      // English-French
    'fren',      // French-English
    'fres',      // French-Spanish
    'frconj',    // French: conjugations

    /** Italian */
    'enit',      // English-Italian
    'iten',      // Italian-English
    'ites',      // Italian-Spanish
    'itit',      // Italian definition
    'itconj',    // Italian: conjugations

    /** Catalan */
    'caca',      // Català: definició

    /** German */
    'ende',      // English-German
    'deen',      // German-English
    'dees',      // German-Spanish

    /** Dutch */
    'ennl',       // English-Dutch
    'nlen',       // Dutch-English

    /** Swedish */
    'ensv',       // English-Swedish
    'sven',       //Swedish-English

    /** Russian */
    'enru',       // English-Russian
    'ruen',       // Russian-English

    /** Chinese */
    'enzh',       // English-Chinese
    'zhen',       // Chinese-English

    /** Portuguese */
    'enpt',       // English-Portuguese
    'pten',       // Portuguese-English
    'ptes',       // Portuguese-Spanish

    /** Polish */
    'enpl',       // English-Polish
    'plen',       // Polish-English

    /** Romanian */
    'enro',       // English-Romanian
    'roen',       // Romanian-English

    /** Czech */
    'encz',       // English-Czech
    'czen',       // Czech-English

    /** Greek */
    'engr',       // English-Greek
    'gren',       // Greek-English

    /** Turkish */
    'entr',       // English-Turkish
    'tren',       // Turkish-English

    /** Japanese */
    'enja',       // English-Japanese
    'jaen',       // Japanese-English

    /** Korean */
    'enko',       // English-Korean
    'koen',       // Korean-English

    /** Arabic */
    'enar',       // English-Arabic
    'aren',       // Arabic-English

    /** English monolingual */
    'enen',       // English definition 
    'enthe',      // English synonyms
    'enusg',      // English usage
    'encol',      // English collocations
    'enconj'      // English: conjugations

);

// Compatible with previous version of Python script.
if(isset($_GET['url'])){
    $_GET['word'] = 'default';
}

// Response to language list quary
if(isset($_GET['getLanguageList'])){
    if(!file_exists('LanguageList.wr')){
        file_put_contents(
            'LanguageList.wr', 
            file_get_contents('https://raw.githubusercontent.com/xiawenke/WordReference_Wox_Plugin/master/LanguageList.wr')
        );
    }
    echo file_get_contents('LanguageList.wr');
    exit();
}

if(!isset($_GET['word'])){
    exit();
}

if(!isset($_GET['dict'])){
    $_GET['dict'] = 'enzh';         // Default dictionary: enzh (English to Chinese).
}

if(!in_array($_GET['dict'], $dictList)){
    $_GET['dict'] = 'enzh';
}

/** DETECT LANGUAGE BY WORDREFRENCE */
$reqURL  = "https://www.wordreference.com/redirect/translation.aspx?w=?=WORD?=&dict=?=DICT?=";
$reqURL  = str_replace('?=WORD?=', $_GET['word'], $reqURL);
$reqURL  = str_replace('?=DICT?=', $_GET['dict'], $reqURL);
$headers = get_headers($reqURL, TRUE);
// Process Returned URL
if(!isset($headers['Location'])){
    print('array|ERROR%%Unexpected error happened on PHP API.');
    exit();
}
$wordUrl = 'https:'.$headers['Location'];


/** LOAD WEBDATA */
if(isset($_GET['url'])){
    // Compatible with previous version of Python script.
    $wordUrl = $_GET['url'];
}

$raw = get_url(link_urldecode($wordUrl));

/** FETCH & RETURN DATA */
$returnData = array();
preg_match_all('/<tr.*?>(.*?)<\/tr>/ism', $raw, $match);
$match = $match[1];
$result = False;

foreach ($match as $key => $value) {
    if (strpos($value,'FrWrd')) {
    	if (strpos($value,'<strong>')) {
            $result = True;
            $processedDef = $value;
            $processedDef = str_replace('<br>', ' ', $processedDef);
                            preg_match_all('/<strong.*?>(.*?)<\/strong>/ism', $processedDef, $processedWord);
    		$processedDef = preg_replace("/<em.*?>(.*?)<\/em>/ism", "", $processedDef);
    		$processedDef = preg_replace("/<strong.*?>(.*?)<\/strong>/ism", "", $processedDef);
    		$processedDef = preg_replace("/<[^>]*>/", "", $processedDef);
            $processedDef = str_replace('&nbsp;', ' ', $processedDef);
        	$returnData = $returnData.'|'.$processedWord[1][0].'%%'.$processedDef.'%%'.$wordUrl;
    	}
    }
}

/** Response to no result */
if($result == False){
    $returnData = $returnData.'|Ops... Definition not found!%%Click here to seach on WordReference on your own.%%'.$wordUrl;
}

/** ADD COPYRIGHT FOOTER */
$returnData = $returnData.'| ====== © Powered by WordReference ====== %%            ⚑ Results from wordreference.com ⚑                                                                                %%https://wordreference.com';

echo $returnData;