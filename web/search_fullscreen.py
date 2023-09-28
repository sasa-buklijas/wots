from browser import document, html, window
import json
from functools import partial

#print(f'{dir(html)=}')
# get data from json file
# with open('categories.json') as file: # do not need it
#    categories = json.load(file)
with open('all_data.json') as file:
    all_data = json.load(file)


def close_modal(event):
    """Custom function to close modal"""

    # SHARING URL NOT IMPLEMENTED
    #root_url ,url = window.location.href.split('#', 1)
    # adding '#' so it is not redirecting automatically (bad UX)
    #window.location.href = root_url + '#' 

    # need this because of parse_url(), because I have redirect
    document['myModal'].style.display = 'none'
    
    # this will stop video from playing in background when modal is closed
    document["modalBody"].clear()   
# each element need uniq id, otherwise only first one is registered
document["closeModalTop"] .bind("click", close_modal)
document["closeModalBottom"] .bind("click", close_modal)


def generate_youtube_iframe(url, no_redirect, title):
    """Just generate Youtube iframe
    
    Have it as separate function, because it is used in redirect also 
    """

    # update header
    document["modalHeader"].textContent = ""
    #document["modalHeader"].textContent = all_data[url]
    # best would be to make new dataformat as dict[url]=qs(question short)
    document["modalHeader"].textContent = title
    
    # because url is nor embedded by default I must make it
    # url https://youtu.be/TeALyCQImmw?t=2097 
    start = url.split('t=')[1]
    s_i = url.rfind('/')
    e_i = url.rfind('?')
    video_id = url[s_i+1:e_i]
    #print(f'generate_youtube_iframe - {s_i=} {e_i=} {video_id}')

    embed_url = f'https://www.youtube.com/embed/{video_id}?controls=0&amp;start={start}'

    document["modalBody"].clear()   # delete old content
    document["modalBody"] <= html.IFRAME(width="560", height="315",
                        src=embed_url
                        ,title="YouTube video player" 
                        ,frameborder="0" 
                        ,allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        )
    
    #print(f'2 - {window.location.origin=}')
    #print(f'2 - {window.location.pathname=}')
    #{window.location.origin}{window.location.pathname}

    if no_redirect:
        pass
        """
        # NOT IMPLEMENTED
        # generate new url, so it can be shared
            # if last char in url is #, then we do not need additional
        if window.location.href[-1] == '#':
            window.location.href += url
        else:
            window.location.href += f'#{url}'
        """


def show_youtube_video_fullscreen(event, title):
    """Show Youtube video"""

    href = event.target.attrs["href"]
    #print(f'show_youtube_video_fullscreen - {href=} {title=}')
    generate_youtube_iframe(href[1:], True, title)


def find_all_positions(main_string, substring):
    """Find all positions of substring in main_string"""
    
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


# called every time when kex is released (search text is changed) 
def make_links(event):
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
                
                new_row = html.A(qs_pp, href=f'#{link}',
                                    Class="list-group-item list-group-item-action",
                                    data_bs_toggle="modal", data_bs_target="#myModal")

                #new_row.bind("click", show_youtube_video_fullscreen)
                # this will take last one qs fro lambda
                #new_row.bind("click", lambda event: show_youtube_video_fullscreen(event, qs))
                # partial not supported
                #new_row.bind("click", partial(show_youtube_video_fullscreen, data=qs))

                # Create a closure to capture the current 'value' variable
                def create_click_handler(value):
                    def click_handler(event):
                        show_youtube_video_fullscreen(event, value)
                    return click_handler
                
                new_row.bind("click", create_click_handler(qs))

                document["zone2"] <= new_row

                if counter % 2 == True:
                    new_row.class_name += ' list-group-item-secondary' # must be space
                #break # for DEBUG
    else:
        #print('Empty String !!!')
        pass

document["search"].bind("keyup", make_links)
