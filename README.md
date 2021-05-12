# Interactive sales report in Dash Python

## Introduction
The repository contains the files that make up a project representing an interactive sales report. The web application was created using the Dash framework. The report was created on the basis of sales data from the Polish electronic market. It consists of two subpages: "Summary" and "Comparison". The first one contains statistics by products, individual companies and sales map by regions. In the second tab we can compare two companies for selected products. You can also choose Full view, which contains both tabs on one page

Repository structure:
* Folder assets - you can find css styles, which determine the appearance of the page. 
* Folder Dane_do_raportow - there are raw sales data divided into weeks.
* Folder Dane_do_strony contains the prepared data used in the report. 
* Folder pages contains the scripts that define the individual pages of the application.
* File app.py - defines page server.
* File design_header.py -  there is a part that appears on each subpage. 
* File log_in.py contains the username and password needed to log into the page.
* File prepare_data.py prepares the raw data for visualization.

The whole project was realized in February 2020 for the purpose of passing classes and was prepared in Polish language. The basis of this project is a sample application presented in the [Dash gallery](https://dash-gallery.plotly.host/dash-financial-report/)

## Technologies
* Python 3.9.2
* pandas 0.25.1
* plotly 4.5.0
* dash 1.8.0
* Css styles

Rest of required packages in requirements.txt file

## Setup
To run the project:
1. Download the entire repository and unzip it.
2. Install the required packages included in the requirements.txt file:
     * Launch any command-line interface (e.g. Anaconda Prompt).
     * If you have one, set up a custom virtual environment for the program in which the project will run.
     * Set the destination path to the folder with the project: "cd 'your destination path to project'"
     * Type "pip install -r requirements.txt".
3. Choose the index.py file and start the application in a program that handles files with the .py extension.

Login data to the report:
Username: bartek
Password: python

Application developed and tested in Spyder. 
