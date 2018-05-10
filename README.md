# Clover
### Presented by J-HEX
#### Eric Li, Xing Tao Shi, Jacqueline Woo, Henry Zheng<br>SoftDev1 pd8<br>Project 02 -- The Final Frontier

## Demonstration Video
[Youtube [insert link here]](https://youtu.be/[insert_link_here])

## Description
Finance Manager

Our idea is a financial manager where the user will be able to make an account and input data about their finances such as how much they spend and what they spent it on. The user will then be able to see a history of their past spending and will also be able to set goals for the future. We will use d3 in order to show how much they are currently spending with each slice of a pie chart being a different category. In addition, the user will be able to see graphs of how much they have spent and saved in each category. The user will also be able to input their stocks, see a history of how the stock has grown, and search up stocks to add to their portfolio.

## Dependencies
* `from flask import Flask, render_template, request, session, redirect, url_for, flash`
  * requires `pip install flask`
* [`python2.7`](https://www.python.org/download/releases/2.7/)
* `import os, sqlite3`

## Launch Instructions
0. Enter your terminal and go into the directory that you want to have this program in
2. Enter this command to clone our repo
```
git clone https://github.com/JackieW001/J-HEX.git
```
3. Run your virtualenv from wherever you have it (if needed)
```
. <PATH_TO_VIRTUALENV>/bin/activate
```
4. Go into the softdev1-finalproj folder using this command
```
cd J-HEX/
```
5. Run the program
```
python app.py
```
6. Go to localhost:5000 in your web browser and enjoy the site!


## API Key Instructions

#### API_1
1. [insert steps here]

## Bugs and Issues
* [insert bugs and issues here]

## File Structure
```
data/
  |  database.db
static/
  css/
    |  home.css
  images/
    |  background.jpg
templates/
  |  home.html
utils/
  |  api.py
  |  database.py
app.py
changes.txt
design.pdf
devlog.txt
log.sh
README.md
```
