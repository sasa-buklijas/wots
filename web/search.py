from browser import document, html
import json

#print(f'{dir(html)=}')
# get data from json file
# with open('categories.json') as file: # do not need it
#    categories = json.load(file)
with open('all_data.json') as file:
    all_data = json.load(file)


def find_all_positions(main_string, substring):
    positions = []
    start = 0
    while start < len(main_string):
        #start = main_string.find(substring, start)
        start = main_string.casefold().find(substring.casefold(), start)
        if start == -1:
            break
        positions.append(start)
        start += 1
    return positions


# called every time when dropdown is changed 
def show(event):
    #print(f'{event=}')

    # delete old questions/answers
    document["zone2"].textContent = ""  

    search = event.target.value
    search_len = len(search)
    #print(f'{search=}')
    if search != '':
        counter = 0
        for qs, ql, link, cat in all_data:

            pos = find_all_positions(qs, search)
            if pos:
                counter += 1
                #print(f'{pos=}')
                
                qs_pp = list()
                start = 0
                for p in pos:   
                    #print(f'{p=}')
                    # make manually mark html tag, because html.MARK is not str
                    # qs[p:p+search_len] is used for case insensitive search
                    qs_pp.append(qs[start:p] + '<mark>' + qs[p:p+search_len] + '</mark>')
                    start = p + search_len
                # kada zavrsi dodati kraj    
                qs_pp.append( qs[p+search_len:] )

                qs_pp = ''.join(qs_pp)

                # ok ako se traži samo jedno 
                ### qs_pp = qs[:pos[0]] + html.MARK(qs[p:p+search_len]) + qs[pos[0]+search_len:]
                
                new_row = html.A(qs_pp, href=link, target="_blank", 
                                    Class="list-group-item list-group-item-action")
                document["zone2"] <= new_row

                if counter % 2 == True:
                    new_row.class_name += ' list-group-item-secondary' # must be space
                #break # for DEBUG
    else:
        #print('Empty String !!!')
        pass

document["search"].bind("keyup", show)
