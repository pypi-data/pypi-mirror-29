"""This is the nester.py module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists."""





def print_List(Lists,indent=False,level=0,fh=sys.stdout):
    for list_element in Lists :
        if isinstance(list_element,list):
            print_List(list_element,indent,level+1,fh)
        else:
            if indent:
                for tabnum in range(level):
                    print("\t",end="",file=fh)
            print(list_element)






            
