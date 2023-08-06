#-*-coding:gbk-*-
"""
这是一个python处理嵌套列表的模块
"""

"""for each_item in movies:
    if isinstance(each_item,list):
        for each_subitem in each_item:
            if isinstance(each_subitem,list):
                for each_subsubitem in each_subitem:
                    print(each_subsubitem)
            else:
                print(each_subitem)         
    else:
        print(each_item)"""

def print_lol(the_list,level=0):
    """
    本函数实现打印嵌套列表的每一个子数据项的功能，提供一个list类型的参数
    """
    for each_item in the_list:
        if  isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for each_block in range(level):
                print("\t",end="")
            print(each_item)        
