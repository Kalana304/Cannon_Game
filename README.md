# Tkinter
Tkinter is the standard Python interface to the Tk GUI toolkit which provides tools for an easy and simple GUI creation. This is a good toolkit to start with for GUI design specially when you need some sort of simple GUI to show your work running in the backend. <https://docs.python.org/3/library/tkinter.html> <br/>
This repo consists few works where a simple GUI was required to show the works in a more user attractive way. 

## Cannon_Game
<p align="justify">
  This is a simple GUI development of the famous canon game using Tkinter package of python. The GUI interface created can select the Angle of the canon to shoot in a range of 0 to 90 degrees using a slider and select the Strength with which the ball is shot in a continuous scale from 0-200N slider. 
Goal is to select the correct combination of Strength and Angle such that the Canon Ball flies over the obstacle and land on the target place. The path of the canon ball is rendered on to the canvas. There is the option of taking air friction into consideration while the ball is moving. 
The script can be further developed to refresh at every attempt rather than drawing on the same canvas. 
 </p>
<p align="center">
  <img src="images/CanonBall_GUI.png">
</p>

## Simple Calculator design
<p align="justify">
Thsi is a simple calculator designed using Tkinter that is capable of performing general mathematical operation, i.e. addition, subtraction, division and multiplication. Further, it is capable of performing the square root function, power of 2 and +/- operations. This can be extended for a scientific calculator as well with extra functions. 
</p>

<p align="center">
  <img src="images/calculator_GUI.png" align="center">
</p>

## Simple Analytical Dashboard
<p align="justify">
Here a simple dashboard is created using tkinter. Data for each company is saved in seperate sheets of an excel file with the company name as the sheet name. The sheet names are loaded and are shown as a drop down menue from which you can select the company we need to explore the details. Each company is provided with main catgories (can be products or services) and sub_catgories with the scores as a percentage for each section. Goal of this GUI is to visulaize the relative proportions of scores of the categories and when clicked on a particular category on the visualization, it should pop up a similar visualization of the sub_categories of it. <br/>
For the visualization I chose pie charts and when clicked on a wedge, it draws the second pie chart for sub categories. Following samples shows an example of the data file the script has considered. 
</p>

<p align="center">
  <img src="images/Company.png" align="center"/> <br/>
</p>

<p align="justify">
The following shows the visualization of the data on the GUI created from Tkinter.
</p>

<p align="center">
  <img src="images/Window01.png" align="center"/> <br/>
</p>
<p align="center">
  <img src="images/CategoryView.png" align="center">
</p>

There are alot of open-source tutorials that let you to learn on how to design GUIs using Tkinter. This is ideal when you require a simple GUI to be designed using python, rather than using new frameworks. However, Tkinter does not provide much options to make your GUI more user attractive like using php or javascript. 

## Number Grid Copy/Paste GUI
![Watch the video]("images/GUI with Tkinter - Demo.mp4")
