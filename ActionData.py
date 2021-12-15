from pandas import read_csv
from VideoGame import VideoGame
NORECORD = 'NORECORD'

class ActionData:
    properties = []
    selection = 0

    # The main interface UI loading event is linked with the WHEN CHANGED property of load_properties()
    # Load the csv file in the specified directory to create all instances
    def load_properties(self, csv_filepath):
        # WHEN CHANGED
        dataFrame = read_csv(csv_filepath)
        # NaN data is processed here
        dataFrame.fillna(NORECORD,inplace=True)  #When inplace = True , the data is modified in place, which means it will return nothing and the dataframe is now updated
        for _, row in dataFrame.iterrows():
            VideoGame(row)
        game_list = VideoGame.games
        return game_list
    
    # Change the content of recommended games
    def change_display(self):
        properties = ActionData.properties
        selection = ActionData.selection
        display_message = '\nFound {} games for you, currently displaying game {}\n\nGame name:{}\nGame type:{}\nRelease time:{}\nRelease platform:{}\nDevelopment Author: {}\nMedia Rating:{}\nPopular Rating:{}\nGame Sales (Millions): {}\nGame Rating:{}\n'.format(
                                len(properties), selection+1,
                                properties[selection].name, properties[selection].genre,properties[selection].year_of_release, properties[selection].platform,
                                properties[selection].developer, properties[selection].critic_score,properties[selection].user_score, properties[selection].global_sales,
                                properties[selection].rating)
        return display_message

    def goto_next_property(self):
        # WHEN CHANGED
        if ActionData.selection < len(ActionData.properties)-1:
            ActionData.selection += 1
        return self.change_display()

    def goto_prev_property(self):
        # WHEN CHANGED
        if ActionData.selection > 0:
            ActionData.selection -= 1
        return self.change_display()