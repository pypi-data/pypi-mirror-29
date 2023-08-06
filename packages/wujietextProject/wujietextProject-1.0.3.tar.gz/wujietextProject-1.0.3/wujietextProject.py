# coding =utf-8
# author:黑亮之星(qq:410445759)
# info: 

def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print('\t',end='')
            print(each_item)
