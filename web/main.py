from browser import document, html
import json


with open('categories.json') as file:
    categories = json.load(file)

with open('all_data.json') as file:
    all_data = json.load(file)

def test_f(event):
    #print(f'#### {event=}')
    #data = document["id"]
    print(f'JE LI OVO LINK {event.target.attrs["link"]}')
    #print(f'#### {dir(event.target)=}')

    link = event.target.attrs["link"]
    url = link.split('?')[0]
    start_time = link.split('=')[1]
    #new_link = f'{url}{}'

    # ovo radi OK
    document["zone3"] <= html.IFRAME(width="560", height="315",
                        src="https://www.youtube.com/embed/lJIrF4YjHfQ?si=1C2UrN_gAvQZQV2y&amp;start=11"
                        ,title="YouTube video player" 
                        ,frameborder="0" 
                        ,allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        )

def show(event):
    print(f'{event=}')
    if event == None: # just hack to call on load
        category_id = 'a'
        category_text = 'Other traditions'
    else:
        dropdown = event.target
        category_id = dropdown.value 
        num = dropdown.selectedIndex
        category_text = dropdown.options[num].text

    
    #dropdown = event.target
    #num = dropdown.selectedIndex
    #category_id = dropdown.value 
    #category_name = dropdown.options[num].text

    # delete old questions
    document["zone2"].textContent = ""  
    document["question_title"].textContent = f'Questions for category - "{category_text}":'  

    counter = 0
    for qs, ql, link, cat in all_data:
        if category_id in cat:  
            counter += 1

            # old way, just link separated by new line
            #document["zone2"] <= html.BR()
            #document["zone2"] <= html.A(qs, href=link, target="_blank")

            """
            # Create a new row
            new_row = html.TR()
            # Create a cell (TD) element to wrap the anchor element
            cell = html.TD()
            anchor_element = html.A(qs, href=link, target="_blank")

            # test for embed youtube
            #anchor_element = html.A(qs, link=link)
            #anchor_element.bind('click', test_f)
            
            # Add the anchor element to the cell
            cell <= anchor_element
            # Add the cell to the new row
            new_row <= cell
            document["zone2"] <= new_row
            """

            new_row = html.A(qs, href=link, target="_blank", 
                                Class="list-group-item list-group-item-action")
            document["zone2"] <= new_row

            if counter % 2 == True:
                new_row.class_name += ' list-group-item-secondary' # must be space

            # ovo radi OK
            #document["zone2"] <= html.IFRAME(width="560", height="315",
            #                    src="https://www.youtube.com/embed/hSHFd4FJAxs?start=1527" 
            #                    ,title="YouTube video player" 
            #                    ,frameborder="0" 
            #                    ,allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            #                    )


def insert_dropdown():
    #dropdown = html.SELECT(style={'height':100, 'width':200})
    #dropdown = html.SELECT(style={'font-size':'3vh'})
    
    #dropdown = html.SELECT()
    dropdown = html.SELECT(Class="form-select", id="category")
    for k, v in categories.items():
        dropdown <= html.OPTION(v, value=k) 
    #dropdown.class_name = 'form-select' # set class separately

    dropdown.bind("change", show)
    document["zone1"] <= dropdown


insert_dropdown()
show(None)  # just hack to call on load

