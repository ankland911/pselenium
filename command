# -*- coding: UTF-8 -*-
from Linker import Linker as lk
from db import Model

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
    for name in rank_lst:
        print rank_lst[name]
    return rank_lst

		
if __name__ == '__main__':
    urls = M('fund').where({'id':'1'}).select()
    M('fund').sql_exec("update fund set `fund_code`='161724' where `id`='1'")
    M('fund').db.Db.close()
    exit(0)
    web = lk()
    for url in urls:
        web.Get(url[1])
        fid = url[0]
        print "id:",fid
        fund_code = web.webbrowser.find_element_by_class_name("ui-num").text
        print fund_code
        rs = M('fund').where({'id':fid}).update({'fund_code':fund_code})
        print rs,";",M('fund').LastSql
        rs = M('fund').where({'id':fid}).update(get_ranks(web))
        print rs,";",M('fund').LastSql
        site = web.webbrowser.find_element_by_class_name("fundDetail-footer")
        lst = site.find_elements_by_tag_name("a")
        for ls in lst:
            print ls.text
    raw_input()
