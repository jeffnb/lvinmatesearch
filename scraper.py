#!/usr/bin/env python

import scraperwiki
import requests
import re
import urllib
import string

def cityLasVegasInmate():

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    url = 'http://www5.lasvegasnevada.gov/InmateSearch/'
    for lastName in string.lowercase:
        data = {'txtLast': lastName}
        inmates = requests.post(url, data=data, headers=headers)
        oID = re.findall('Offender_ID=(.+?)"', inmates.content)
        for idx, offid in enumerate(oID):
            url2 = 'http://www5.lasvegasnevada.gov/InmateSearch/charges.aspx?Offender_ID='+offid
            detail = requests.get(url2, headers=headers)
            tBail = 0
            if re.findall('"Label1"\>(.+?) \<', detail.content):
                lvname = re.findall('"Label1"\>(.+?) \<', detail.content)[0]
            else:
                lvname = re.findall('Offender_ID\=.+?"\>(.+?)\<', inmates.content)[idx]
            if re.findall('"Label2"\>(.+?)\<', detail.content):
                lvid = re.findall('"Label2"\>(.+?)\<', detail.content)[0]
            else:
                lvid = 'n/a'
            if re.findall('"Label3"\>(.+?)\<', detail.content):
                lvage = re.findall('"Label3"\>(.+?)\<', detail.content)[0]
            else:
                lvage = 'n/a'
            if re.findall('"Label11"\>(.+?)\<', detail.content):
                lvdate = re.findall('"Label11"\>(.+?)\<', detail.content)[0]
            else:
                lvdate = 'n/a'
            if re.findall('_Label8">(.+?)<', detail.content):
                lvbail = re.findall('_Label8">(.+?)<', detail.content)
                for bail in lvbail:
                    if "$" in bail:
                        bail = bail.replace(',','')
                        bail = bail.replace('$','')
                        bail = bail.replace('.00','')
                        tBail += int(bail)
            #with open('swdata.csv', "a") as myfile:
            #    myfile.write('Las Vegas,' + lvname + ','+ lvid +',' + lvage + ',' + lvdate + ',' + str(tBail) + '\n')
            savedata = {'id': lvid,
                        'location': 'Las Vegas',
                        'name': lvname,
                        'book_date': lvdate,
                        'bail': str(tBail)}
            scraperwiki.sqlite.save(unique_keys=['id'], data=savedata)

def clarkCountyInmate():
    #<editor-fold>
    data = ('__VIEWSTATE=%2FwEPDwUIOTE5NTg4NjhkZGvx05uXGR%2BWuRIOdPjT9KzcmuLh1J8Zk1gT0J0aC2Wi&'
            '__EVENTVALIDATION=%2FwEdAAWCIueLxX7W6RwIfnVWJPj0JNOHGRTiA26VmVCqyHoxqsWzilCqUZiLm2Tkt0sWoCWjOglmm5fGSk5Ukp'
            'FsfK4enirgrpbTwEsK9BgCJuFqya%2FmyQJ7PsrYEacOYfCQSaPsSvX6AACoCDB8vMSi31O9&'
            'TxtID=&txtName=__&SearchName=++Submit++')
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Content-Length': '344',
               'Referer': 'http://redrock.clarkcountynv.gov/ccdcincustody/incustodysearch.aspx',
               'Accept-Encoding': 'gzip, deflate',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0',
               'Connection': 'keep-alive'}
    #</editor-fold>
    url = 'http://redrock.clarkcountynv.gov/ccdcincustody/incustodysearch.aspx'
    inmates = requests.post(url, data=data, headers=headers)
    p = re.compile('DataGrid1:_ctl(.+?):_ctl0" value="Find w/ ID" /></td><td>(.+?)</td><td>(.+?)</td>'
                   '<td align="right">(.+?)</td><td><input type="submit" name="DataGrid1:_ctl.+?:_ctl1" '
                   'value="Find w/ Case No." /></td><td>.+?</td><td>(.+?)</td><td>.+?</td><td>.+?</td>')
    viewstate = urllib.quote_plus(re.findall('VIEWSTATE" value="(.+?)"', inmates.content)[0])
    eventval = urllib.quote_plus(re.findall('EVENTVALIDATION" value="(.+?)"', inmates.content)[0])
    #ccindex, ccid, ccname, ccdate, ccage = re.findall(p, inmates.content)[0]
    for a in re.findall(p, inmates.content):
        ccindex, ccid, ccname, ccdate, ccage = a
        url2 = 'http://redrock.clarkcountynv.gov/ccdcincustody/inCustodyReference.aspx'
        data2 = ('__VIEWSTATE=' + viewstate + '&__EVENTVALIDATION=' + eventval + '&DataGrid1%3A_ctl' + ccindex + '%3A_ctl0=Find+w%2F+ID')
        details = requests.post(url2, data=data2, headers=headers)
        tBail = 0
        if re.findall('colspan="2"><font color\="\#ff0000">.+?</font></td><td width="17\%"><font color="\#ff0000">(.+?)<', details.content):
                ccbail = re.findall('colspan="2"><font color\="\#ff0000">.+?</font></td><td width="17\%"><font color="\#ff0000">(.+?)<', details.content)
                for bail in ccbail:
                    if "$" in bail:
                        bail = bail.replace(',','')
                        bail = bail.replace('$','')
                        bail = bail.replace('.00','')
                        tBail += int(bail)
        savedata = {'id': ccid,
                    'location': 'Clark County',
                    'name': ccname,
                    'age': ccage,
                    'book_date': ccdate,
                    'bail': tBail}
        print savedata
        scraperwiki.sqlite.save(unique_keys=['id'], data=savedata)

def hendersonInmate():
    #<editor-fold>
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0'}
    data = ('smViewInmate=UpdatePanel1%7CbtnSearch&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=XTLvGPfDA43vRnIN4ccP7y'
            'NAo7nkQLvOpcWRAx7tgGG%2FtJOzq4NnmW96UMgXM1IXJJundKU24YzTP8aJYA5jZrwuyM%2FoTAbWouZRYJHZk4poBwlgVRC72vdsSLN7'
            'vw6Eh5xASVYSigtiUBwW4ly0fM%2F%2BX7s7VOZPOjM8slsrQvsKYdY0egH7TTQqfvVY3nSu5HLaCtEszlDHWnA2MbqKA2Y%2Ff5Y9ZVv'
            'C%2FgW033s7j1H4c01rVQCAP1yHDFqW9qo%2B7HLuEhTN1iWkz2EGOmJW7nmo5lr9QxRVwlhLiaVqoq57aSTbf2kzQZmSgEpQ2yKAT7Bm'
            '86os22%2Fwv5cA2SxzdQ%3D%3D&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=a%2FnifgsC0kFdy0owjsowJfMF1ga4CVdEUPLA'
            'KayEgH4nmR7rIqD9FgaHhJne1j%2FJ9pQKlJW6B%2BoJb%2Fv2FwvrbJMkQp26zz93CDjTCQ8XiFoW1ULuw5Yd%2FYgVv7%2BrpzKZ2dF'
            '5A0hbxj2k6jC4POYNrW44mqVo0mhjBSS5mCt18f0%3D&txtSearchName=&__ASYNCPOST=true&btnSearch=Search')
    #</editor-fold>
    url = 'http://inmateinfo.cityofhenderson.com/'
    inmates = requests.post(url, data=data, headers=headers)

    barf = '&__VIEWSTATE=' + urllib.quote_plus(re.findall('_VIEWSTATE\|(.+?)\|', inmates.content)[0])
    barf2 = '&__EVENTVALIDATION=' + urllib.quote_plus(re.findall('__EVENTVALIDATION\|(.+?)\|', inmates.content)[0])
    select = re.findall('Select\$(.+?)\&', inmates.content)
    agedate = re.findall('Select\$.+?\&\#39\;\)" style="color:\#993366;">View</a></td><td>.+?</td><td>.+?</td><td>.+?'
                         '</td><td>.+?</td><td>(.+?)</td><td>(.+?)</td>', inmates.content)

    for index in select:
        select2 = '&__EVENTARGUMENT=Select%24' + index
        barf
        data2 = ('smViewInmate=UpdatePanel1%7CgvSearchResults&__LASTFOCUS=&txtSearchName=&' + barf +
                 '&__EVENTTARGET=gvSearchResults&' + select2 + barf2 +
                 '&__VIEWSTATEENCRYPTED=&__ASYNCPOST=true')
        details = requests.post(url, data=data2, headers=headers)
        name = re.findall('lblName"\>(.+?)\<|lblConName">(.+?)<', details.content)
        if re.findall('lblTotalBond"\>(.+?)\<', details.content):
            totalbond = re.findall('lblTotalBond"\>(.+?)\<', details.content)[0]
            totalbond = totalbond.replace(',','')
            totalbond = totalbond.replace('$','')
            totalbond = totalbond.replace('.00','')
            totalbond = str(int(totalbond))
        else:
            totalbond = str(0)
        if name[0][0] == '':
            fname = name[0][1]
        else:
            fname = name[0][0]

        savedata = {'location': 'Henderson',
                    'name': fname,
                    'age': agedate[int(index)][0],
                    'book_date': agedate[int(index)][1],
                    'bail': totalbond}
        scraperwiki.sqlite.save(unique_keys=['name'], data=savedata)
        #with open('swdata.csv', "a") as myfile:
        #    myfile.write('Henderson,' + fname + ',N/A,' + agedate[int(index)][0] + ',' + agedate[int(index)][1] + ',' + totalbond + '\n')


#os.remove('swdata.csv')
#with open('swdata.csv', "a") as myfile:
#            myfile.write('Prison,Last Name,First Name,ID,Age,Book Date,Bail' + '\n')

hendersonInmate()
cityLasVegasInmate()
clarkCountyInmate()