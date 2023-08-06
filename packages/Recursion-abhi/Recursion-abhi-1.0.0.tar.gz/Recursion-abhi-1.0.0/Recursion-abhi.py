"""This is the nester.py module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists."""



def print_List(Lists):
    for list_element in Lists :
        if isinstance(list_element,list):
             print_List(list_element)
        else:
             print(list_element)
