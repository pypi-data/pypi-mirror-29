#-*-coding:gbk-*-
"""
����һ��python����Ƕ���б��ģ��
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

def print_lol(the_list,indent=False,level=0):
    """
    ������ʵ�ִ�ӡǶ���б��ÿһ����������Ĺ��ܣ��ṩһ��list���͵Ĳ���
    """
    for each_item in the_list:
        if  isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for each_block in range(level):
                    print("\t",end="")
            print(each_item)        
