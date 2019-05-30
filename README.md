# ML Task
How to run?

utils.py
This files load the database engine sll over the scripts and contains the API key for YouTube.
Please change it to you API key.
 
get_videos.py
This script will automatically get list of political videos and comments and it will stores the data in the database.

train.py
Will train anstm model for this task using imdb dataset, and it will save the best epoch and calculates tge accuracy and the F1 score for each epoch.
15 epochs are set to be trained.

classify_comments.py


