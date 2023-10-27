# O-Taste ~ CS50 Final Project

The O-Taste project is a web-based social media prototype with the objective of connecting people through their interests.

## Creating a profile

You can create your O-Taste profile while registering to the web page, you just need to enter a username that will identify you, a password, email, birthday, and gender, when logged in you can enter your profile through the navigation bar to add some interests to your profile so other people can see what are you into, you can also see your list of friends and click on their names to enter to their profile.

## The front page

When you log in to O-Taste you'll be redirected to the homepage where you can post whatever you have in mind! you can also see your older posts and your friends' posts.

## Looking for friends

When you first log in you won't have any friends added at first so it's natural that you'll want to look for some, you just need to click the search button in the navigation bar! On the search page, you'll be able to look for people based on their usernames and interests. The search algorithm will look for usernames that contain the string entered in the search field, not exactly that string, the interest field lets you choose one interest to filter people, if you leave all fields blank it will just return a list of all the users in the website, if you fill just one field it will return a list of users filtered by that one parameter, and you fill both fields it will filter the lists by both parameters.

### Checking others' profiles

When you look for friends on the search page it will return a list of users, whose names are clickable and contain links to their profile page, and what they are interested in. If you enter their profile page then you can send them a friend request, and they can accept it by checking their friend requests list accessed through the navigation bar.

### Friend requests

When you receive a friend request you can check it out on your friend request page. It'll show you a list with all your requests, each entry contains the sender's name, which redirects you to their profile's page, and an accept request button. If you enter their profile page you can add them there too, once accepted you'll be able to see their posts on the homepage and check their email in their profile if you ever want to contact them. You can also delete them from your friends.

## Structure 

The web page was built using HTML, CSS, JavaScript, and Python for the server.

### Front End

The HTML works with the Jinja syntax, using a layout.html file that every other .html file extends to. It also uses the basic bootstrap stylesheet.

### Server

The server works with the Python library Flask, through a file called app.py that helps render every .html file while communicating with the database and verifying the data entered by the user. It also uses a file called helpers.py that contains useful functions. 

### Database

The Database was made with SQLite3 and contains foreign key restrictions, which I learned to implement in my university studies, the database file is finalProject.db. 

## Development process

### Plans

I'd like to add the option to edit your personal information through your profile page, the option to block users too, and to expand the interests system.

### Elements that were cut out

The project was intended to have a two-week development cycle so I could attend to my responsibilities while working on this project, due to that the interest system was made much simpler, being limited to just a list of some areas, and the option to interact with posts.

Other than that, the development process of this project was very smooth and I had almost no problems with it.

