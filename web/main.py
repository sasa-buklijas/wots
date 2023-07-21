from browser import document, html
from browser.widgets.dialog import InfoDialog
import json

with open('categories.json') as file:
    categories = json.load(file)

with open('all_data.json') as file:
    all_data = json.load(file)

def show(event):
    dropdown = event.target
    num = dropdown.selectedIndex
    #InfoDialog("Demo", "Selected: {}".format(dropdown.options[num].text))
    #InfoDialog("Demo2", "Selected: {}".format(dropdown.value))

    category_id = dropdown.value 
    category_name = dropdown.options[num].text
    #InfoDialog("Demo3", f"Selected: {category_id} {category_name}")

    #document["zone2"] <= html.BR()

    # delete old 
    document["zone2"].textContent = ""  

    for qs, ql, link, cat in all_data:
        if category_id in cat:  
            document["zone2"] <= html.BR()
            #document["zone2"] <= qs
            # need button
            document["zone2"] <= html.A(qs, href=link, target="_blank")

            
            # ovo radi OK
            #document["zone2"] <= html.IFRAME(width="560", height="315",
            #                    src="https://www.youtube.com/embed/hSHFd4FJAxs?start=1527" 
            #                    ,title="YouTube video player" 
            #                    ,frameborder="0" 
            #                    ,allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            #                    )


def insert_dropdown():
    document["zone1"] <= "Select category: "
    #dropdown = html.SELECT(
    #    html.OPTION(v, value=k) for k, v in categories.items())
    
    #dropdown = html.SELECT(style={'height':100, 'width':200})
    #font-size: 16px
    dropdown = html.SELECT(style={'font-size':'3vh'})
    for k, v in categories.items():
        dropdown <= html.OPTION(v, value=k) 


    dropdown.bind("change", show)
    document["zone1"] <= dropdown
    document["zone1"] <= html.HR()
    

#document <= html.BR()
#document <= "Hello before dropdown"

insert_dropdown()
#document <= html.BR()
#document <= "Hello After Dropdown "