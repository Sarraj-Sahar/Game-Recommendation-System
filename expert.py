import os  # The OS module in Python provides functions for interacting with the operating system.

import time

from time import sleep  # Python time method sleep() suspends execution for the given number of seconds. The passed argument indicates a more precise sleep time.

from tkinter import Label, Frame, Button, Checkbutton, Tk, IntVar, HORIZONTAL, Scale, filedialog

from tkinter import  ttk  # The ttk widgets don't have a text widget.The scrolledtext widget is just a text widget and scrollbars

from ActionData import ActionData
from Evaluation import Evaluation
from VideoGame import VideoGame

# tkinter is the standard Python interface to the Tk GUI toolkit
# Buttons , Checkbuttons,Scales... are basic Tkinter widgets , Widgets are basic building blocks of a GUI application

NORECORD = 'NORECORD'

# intVar List associated with 8 different ratings, if value = 1 ,it means it is selected
intVar = []

# The nth record is currently displayed, switch by button
selection = 0

# To Store all game records in the database
game_list = []

# All Rating List Options available
rating_list =  ['E10+', 'T', 'K-A', 'RP', 'E', 'EC', 'AO', 'M']

# Change the UI display content according to user interaction
#  switch_property method to go to "previous" or "next"
def switch_property(direction):
    if direction == 'prev':
        message = action_data_agent.goto_prev_property()
    else:
        message = action_data_agent.goto_next_property()
    result_message['text'] = message


# [Daemon] According to the user's search conditions, traverse the game_list queue to find qualified instances
# Link the components of the interface with the daemon and remove unqualified instances
# Store eligible instances in ActionData.properties
def properties_filter():
    # Get the query conditions selected by the user in the interface from each component
    ActionData.properties.clear()
    
    args = {'pf': platform_select.get(),
            'ge': genre_select.get(),
            'lb': int(from_year_select.get()),
            'rb': int(to_year_select.get()),
            'cs': int(critical_score_scale.get()),
            'us': round((user_score_scale.get()),1)}
    allowed_rating = []
    for idx in range(len(intVar)):
        if intVar[idx].get():
            allowed_rating.append(rating_list[idx])
    args['ar'] = allowed_rating
    evaluate = Evaluation(args)
    evaluate.print_rule()

    for game in game_list:
        if evaluate.qualified(game):
            ActionData.properties.append(game)
    
    # The selection result that meets the user's requirements
    print('RESULT', len(ActionData.properties))
    # Sort the search results in reversed order by year
    ActionData.properties = sorted(ActionData.properties, key=lambda game: game.year_of_release if type(game.year_of_release) == int else -1, reverse=True)

    # Display the first record that meets the user's requirements

    if len(ActionData.properties):
        ActionData.selection = 0
        result_message['text'] = action_data_agent.change_display()
    else:
        result_message['text'] = 'There are no games that meet the requirements in the database'

#Designing the display of our interface

if __name__ == '__main__':

    window = Tk()
    window.title("Game-Recommender.expertsystem")  #title of our expert system
    window.geometry('1024x640')    #dimensions
    window.iconbitmap('./game_128px_1234884_easyicon.net.ico')   #we set an icon
    window.resizable(width=True, height=True)   #this will allow you to resize the window size

    # The recommended game information display
    message = Label(window, text='[EXPERT SYSTEM]', font=('Microsoft YaHei', 18))
    result_window = Frame(window, width=1024, height=180)

    result_window.propagate(0)
    message.grid(row=0, columnspan=5)
    result_message = Label(result_window, text='No recommendations yet')
    result_message.pack()
    result_window.grid(row=1, columnspan=5)

    # Set button in the second row, use the button to switch when there are multiple recommended games
    prev_btn = Button(window, text='Previous', command=lambda:switch_property('prev'))
    next_btn = Button(window, text='Next', command=lambda:switch_property('next'))
    prev_btn.grid(row=2, column=3, sticky='e', ipadx=20, pady=30)
    next_btn.grid(row=2, column=4, ipadx=20)

    # The third line is used to select the platform and game type
    platform_label = Label(window, text='Game platform', font=('tMicrosoft YaHei',12,'bold'))
    genre_label = Label(window, text='Game Type', font=('tMicrosoft YaHei',12,'bold'))
    platform_select = ttk.Combobox(window)
    genre_select = ttk.Combobox(window)
    platform_label.grid(row=3, column=0)
    platform_select.grid(row=3, column=1)
    genre_label.grid(row=3, column=2)
    genre_select.grid(row=3, column=3)

    # Fourth line, select game release year
    time_range_labelA = Label(window, text='Release time ', font=('tMicrosoft YaHei',12,'bold'))
    time_range_labelB = Label(window, text='Until', font=('tMicrosoft YaHei',12,'bold'))
    from_year_select = ttk.Combobox(window)
    to_year_select = ttk.Combobox(window)
    time_range_labelA.grid(row=4, column=0)
    time_range_labelB.grid(row=4, column=2)
    from_year_select.grid(row=4, column=1)
    to_year_select.grid(row=4, column=3)

    # The fifth line, For Game score prefrences
    critical_score_scale = Scale(window, label='Critic rating is higher than', from_=0, to=100, orient=HORIZONTAL,
             length=400, showvalue=1, tickinterval=10, resolution=1)
    critical_score_scale.grid(row=5, column=0, columnspan=2)
    user_score_scale = Scale(window, label='The public rating is higher than', from_=0, to=10, orient=HORIZONTAL,
             length=400, showvalue=1, tickinterval=1, resolution=0.1)
    user_score_scale.grid(row=5, column=2, columnspan=2)

    # The sixth line, submit
    submit_btn = Button(window, text='submit', font=('Microsoft YaHei', 15), command=properties_filter)
    submit_btn.grid(row=6, column=2, ipadx=70, ipady=10, pady=10)

    # In the rightmost column, place a listGroup for selecting game ratings
    rating_frame = Frame(window)
    rating_frame.grid(row=3, column=4, rowspan=3)
    rating_note_label = Label(rating_frame, text='Select Game rating', font=('tMicrosoft YaHei',12,'bold'))
    rating_note_label.pack()
    for idx in range(len(rating_list)):
        intVar.append(IntVar(value=1))
        check = Checkbutton(rating_frame, text=rating_list[idx], variable=intVar[idx], onvalue=1, offvalue=0)
        check.pack(side='top', expand='yes', fill='both')

    # [Load Properties] Load the csv file after the UI interface is loaded
    # Create ActionData object action_data_agent
    # use WHEN CHANGED to instantiate all records in the database
    print('SYSTEM: The expert system needs to load a CSV file')
    print('SYSTEM: Current directory', os.getcwd())
    try:
        result_message['text'] = 'loading data...'
        csv_filepath = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select csv file')
        start = time.time()
        print('SYSTEM: csv file loading...')
        action_data_agent = ActionData()
        game_list = action_data_agent.load_properties(csv_filepath)
        counter = round(time.time() - start, 2)
        result_message['text'] = 'Data is loaded, it took {}s, there is no recommended content yet'.format(counter)
        print('SYSTEM: The csv file is loaded, it took {}s'.format(counter))
    except Exception:
        print('ERROR: Failed to load CSV file')
        window.destroy()
        sleep(1)
        exit()

    # Load the contents of the drop-down menu on the home page according to the dataset
    platform_select['value'] = sorted(list(VideoGame.Platform))
    genre_select['value'] = sorted(list(VideoGame.Genre))
    from_year_select['value'] = list(VideoGame.YearOfRelease)
    to_year_select['value'] = list(VideoGame.YearOfRelease)
    platform_select.current(0)
    genre_select.current(0)
    from_year_select.current(0)
    to_year_select.current(len(VideoGame.YearOfRelease)-1)

    # Used for specific attribute types and specific content in the early output table
    VideoGame.show_genre()
    VideoGame.show_platform()

    window.mainloop()