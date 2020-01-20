# Run client
1. In order to run the client, go into PokerGame, decide in the main function how many players that should compete, default is 5.
2. Thereafter run PokerGame.py
3. Be aware that you may need to start the project from PokerGame directory since there is a static path to reach data in evolution folder

# Run data mining
1. In order to run the data mining, located in evolution/data_mining.py
2. Define a file inside of data that contains information from the server.
3. Observe that if no information of opened files is observed in console the wrong path from which the project is run from might be wrong.
4. The data will be stored insided of minedData.txt which the ML.py and Client.py will use to create and predict a model.

# Run machine learning
1. In order to run the machine learning, run ml.py that is located in evolution folder
2. The machine learning will load the minedData.txt and output information of different models into the console

# Requirements
1. As observed in requirements.txt these packages MUST be included in order to run the project. 