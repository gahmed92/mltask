# ML Task
## Sentiment analysis for political YouTube videos' comments.

This task works on python2.7 using keras tensorflow for the sentiment analysis model.

### How to run?

`utils.py`
This file loads the database engine all over the scripts and contains the API key for YouTube.
Please change it to your API key.
 
`get_videos.py`
This script will automatically get list of political videos and comments and it will store the data in the database.

`train.py`
Will train an lstm model for this task using imdb dataset, and it will save the best epoch and calculate the accuracy and the F1 score for each epoch.
15 epochs are set to be trained.

`classify_comments.py`
Will load the lstm model to classify the sentiments for the stored comments in the database.



