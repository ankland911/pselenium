# -*- coding: UTF-8 -*-
from lib.Linker import Linker as lk
from lib.db import Model

def M(table_name):
	global arrModel
	arrModel = {}
	try:
		return arrModel[table_name]
	except:
		arrModel[table_name] = Model(table_name)
		return arrModel[table_name]

def get_ranks(web):
    table =web.webbrowser.find_element_by_id("increaseAmount_stage")
    ranks = table.find_elements_by_tag_name("h3")
    rank_lst = {}
    rank_lst['1w'] = ranks[0].text
    rank_lst['1m'] = ranks[1].text
    rank_lst['3m'] = ranks[2].text
    rank_lst['6m'] = ranks[3].text
    rank_lst['fromnow'] = ranks[4].text
    rank_lst['1y'] = ranks[5].text
    rank_lst['2y'] = ranks[6].text
    rank_lst['3y'] = ranks[7].text
    prt=''
    for name in rank_lst:
        prt = prt + "," + rank_lst[name]
    print prt
    return rank_lst

		
if __name__ == '__main__':
    urls = M('fund').where('id>348').select()
    #afd = Model('config').sql_exec("insert into config (opt,value) values ('test','test')")
    #print afd
    #print Model('config').db.Db.commit()
    #exit(0)
    web = lk()
    for url in urls:
        web.Get(url[1])
        fid = url[0]
        print "id:",fid
        fund_code = web.webbrowser.find_element_by_class_name("ui-num").text
        print fund_code
        rs = M('fund').where({'id':fid}).update({'fund_code':fund_code})
        try:
            rs = M('fund_links').insert({'fund_code':fund_code})
        except:
            pass
        rs = M('fund').where({'id':fid}).update(get_ranks(web))
        site = web.webbrowser.find_element_by_class_name("fundDetail-footer")
        lst = site.find_elements_by_tag_name("a")
        del lst[0]
        data={}
        for ls in lst:
            href = ls.get_attribute("href")
            print ls.text,";",href
            data[ls.text.encode('utf-8')] = href.encode('utf-8')
        rs = M('fund_links').where({'fund_code':fund_code.encode('utf-8')}).update(data)
    raw_input()

