
# NORECORD indicates that the record in the data has no corresponding attributes, and special treatment is needed to prevent display errors

NORECORD = 'NORECORD'

#VideoGame class, which contains general features applicable to video games

class VideoGame:
    games = []      #empty list
    Platform = set()    # empty set
    Genre = set()
    YearOfRelease = set()

    def __init__(self, data):      # This mangling (--methodName--) is used to avoid name clashes with names defined by other classes , The Evaluation Class in our case
        # Initialize the object
        # Replace the missing data with the string no_record
        self.name = data.Name
        self.platform = data.Platform
        try:
            self.year_of_release = int(data.Year_of_Release)
        except ValueError:
            self.year_of_release = NORECORD

        self.genre = data.Genre
        self.publisher = data.Publisher
        self.global_sales = data.Global_Sales

        try:
            self.critic_score = int(data.Critic_Score)
        except ValueError:
            self.critic_score = NORECORD
        try:
            self.user_score = round(float(data.User_Score), 1)
        except ValueError:
            self.user_score = NORECORD
        self.developer = data.Developer
        self.rating = data.Rating
        # game Platform type
        VideoGame.Platform.add(self.platform)

        # Avoid NaN game genres in the drop-down menu
        if self.genre != NORECORD:
            VideoGame.Genre.add(self.genre)
        if self.year_of_release != NORECORD:
            VideoGame.YearOfRelease.add(int(self.year_of_release))
        VideoGame.games.append(self)

    # Print out game Genres
    @classmethod
    def show_genre(cls):  #cls is like self BUT cls implies that method belongs to the class while self implies that the method is related to instance of the class
        print(len(cls.Genre), ' genres in total: ', cls.Genre)

    # Print out game Platforms
    @classmethod
    def show_platform(cls):
        print(len(cls.Platform), ' platforms in total: ', cls.Platform)
