"""This is the nester.py module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists."""




def print_List(Lists,level=0):
    for list_element in Lists :
        if isinstance(list_element,list):
            print_List(list_element,level+1)
        else:
            for tabnum in range(level):
                print("\t",end="")
            print(list_element)
