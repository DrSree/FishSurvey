**NOTE**This program does not work if you are using the Anaconda distribution of python.
	I think the specific issue is their version of matplotlib.

This app analyzes the fish survey data that was obtained from :
	http://limnoweb.eeob.iastate.edu/fishpub/weight.aspx

List of columns available
        lakeCode
        lakeName
        lakeDir - The directions to reach a lake
        lakeSize - Size of the lake in acres
        countyID - Foreign key to county 
        countyID
        countyName
        countySize - Size of the county (sq mi)
        countyZone - Zone of the county (NORTHERN, CENTRAL, SOUTHERN)
        lakeCode - Foreign key to lake
        fishType
        countCaught - How many of the fishType were found during the survey
        avgLen - Average length of the fishType caught
        avgWt - Average weight of the fishType caught
        surveyDt - Date the survey was performed
        score - A score of countCaught, avgLen, and avgWt
                (Used to find which lakes have the best fishType)

The program is contained entirely in gui.py

gui.py reads FullData.csv (contained in the data folder of the project) into a DataFrame

The starting page contains
	-buttons that link to pages which display plots.
	-a text widget that displays some simple statistics.

The top ten page contains 
	-a horizontal bar chart of the top ten lakes to find a certain fish
		-the fish is selectable by the user.
			-the default chart displays information for walleye
		-the y axis shows the name of the lake
		-the x axis show the average length and average weights of the fish

The lake survey page contains
	-a bar chart of all the fish that were surveyed for a certain lake
		-the lake is selectable by the user
			-the default chart displayed information for Clear Lake
		-the y axis is a numerical value
		-the x axis shows the type of fish and its average length and weight

The scatter page contains
	-a scatter plot to display the relationship of length and weight in fish
	-a navigation toolbar that allows the user to navigate the plot


The data retrieval process:
-I created an api in Kimono labs for all of the fish information

-Since each lake had its own page, I manually parsed the HTML to get the lake URL parameters

-Kimono hadn't supported URL parameters very well at the time, though they do have good support now,
	-so i created a script to iterate through the URL parameters and to also
	-keep track of errors along the way.

-I also created a Kimono api to retrieve information about the lakes and counties in iowa
	-(I was not able to get some data through the apis so some manual research was involved)

	I was initially going to use SQL for the project, which is why I also have the data split up in a more 
normalized way which can be seen in the data folder. I decided to use pandas dataframes instead, since 
I already have a good amount of SQL knowledge through work.


Challenges:
	I have never written a gui before, so that was a challenge/learning experience as a whole.
It took a lot of time to understand how widgets interact and work, but I thought a gui would be the 
best option to allow the user to interact with the data in the way that I wanted. I wanted the user
to be able to easily switch between options for what they wanted to see on the graphs. This lead me
to one of my main challenges, animating the graph.

	Trying to get the graph to change when a different option was selected was much more of a 
challenge than I had initially expected. I first tried to use an animation function through matplotlib.
This way worked, but it worked because it would constantly check for changed in the data. This turned
out to be a problem because, with the frequency that it was looking for updates, the program would become
very unstable. This would be interesting to use with live data, but since I had a static set, I decided
it would be best to force the user to manually refresh the selection. So I created a refresh to destroy
the current plot and replace it with a new one.

	Another challenge was trying to figure out how to make multiple pages within one window. My first
attempts would open a completely new window for any button that was pressed. I wanted more fluent movement
throughout my app. The solution was to create a frame for each of my pages and a function to lift the frame
corresponding to the button pressed. The logic for this solution was not mine. I found it on a YouTube tutorial
which was one of the parts of this playlist (I don't remember which one specifically):
https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk

	Before I was even trying to animate the charts that were displayed on the page, I was struggling to even
display a chart in a tkinter widget. My attempt was to create the plots as a .png and display it in the PhotoImage widget.
I got this approach to work, but I was not a fan of it just because I thought there had to be a better way. I found a better
way through matplotlibs documentation found here:
http://matplotlib.org/1.4.2/examples/user_interfaces/embedding_in_tk.html

	Those were the challenges that took the longest to sort out.  Overall, this project challenged me a lot, which
helped me learn a great deal. I am confident that I could start a new project and be able to plan and execute on it
much better. Also, once I had my data, I found that it wasn't as interesting as I had hoped it would be. I was planning
on actually continuing to develop the app after the course ended, but I changed my mind part of the way through the process.
It is not a complete loss, though. This project has really motivated me to start a new data analysis project in python.
I haven't decided entirely on what my new project will be, but I want to make sure it will be something worth maintaining
and putting effort into. This project has made me feel much more comfortable with programming. I can even recognize a lot
of my own bad code in this project that I keep wanting to clean up, but I forced myself to quit revising it so much.


Wish Lish for the app:
-Better data - the data that I was able to recieve from the DNR was basically just a summary of their data. I would
	like to get my hands on more specific data elements of the fish surveys. I also wish that the surveys were
	conducted more frequently and allow for a time series analysis. More specific data would allow for a much more
	interesting analysis.

-Better plots - I would have liked to spend more time customizing the plots and making them much more interactive.
	Also, if the data was better, more interesting plots could be made. I also would like to plot geographically
	like a heat map of the counties in Iowa.

-Better layout - I spent most of the time trying to get everything to work, so the layout is very rushed.

-Split it into different scripts















