# Electric-Vehicle-Database

Overview

This application is based on platform as a service (PaaS) in which user can store information about different Electric Vehicles. User can add, remove and compare different vehicles stored in database. Some of these features only work when user logged in with their login ID only. 
1	INTRODUCTION
1.1	Purpose and Scope
The purpose of this application is to store Electric vehicles according to their name, manufacturer, year, battery size, WLTP, cost and power. And compare them according to the need of user.
1.2	Project Requirements
1.	Python 2.7
2.	Google app engine
3.	Git Repository

2	SYSTEM ARCHITECTURE
1.	JINJA ENVIRONMENT:
We use this to define a variable which we don’t want to change in our program. Since there is no concept of constant in python therefore, we use jinja environment object. The templates used in program by request handlers in jinja were organized and used with the help of loader lines. They locate in root directory in case of google app engine. 
2.	CLASS MAIN HANDLER
Def get(): This method is called by the instances of the class. The URL that will contain login or logout link and the string represents it is passed in python. This will determine whether the user logged in or not.
Then URL string generate the map that contains everything that we need to pass to the template. Jinja is used to pull the template file and render it with given template values.
3.	CLASS ADD HANDLER
Function	Get(), Post()
Object	ev_obj
Parameters	Name, manufacturer, year, battery, wltp, power, cost

Def get(): First this function checks weather the user is logged in or not. After logged in the user can see the ADD button, by the help of which user can add electric vehicle by pulling out the form page where we have mention different information for new vehicle to be stored in database.
Def post(): After we redirect to the page pulled out, by the help of post function we can enter the information about new electric vehicle with different parameters. Here we use ndb.key property in names and manufacturer to avoid the acceptance of electric vehicle with same name and manufacturer.
4.	CLASS QUERY HANDLER
Function	Get(), Post()
Parameters
 ( uc -upper count,
 lc - lower count)	Name, manufacturer, year, battery, wltp, power, cost

Def get(): This function pulls out the query.html form from the ndb datastore. In this stage is don’t depend weather the user is logged in or not. The attributes name and manufacturer are string based and have single string input, and all other with numeric value have predefined upper and lower limit so user can just select according to his need and click on search button.
Def post(): After user clicks the submit button, this method checks the database for the selected values given by user and displays the electric vehicle where all the parameters are true. If user doesn’t select any given parameters, then the function will show the full list of electric vehicles.
5.	CLASS DETAILS HANDLER
Function	Get(), Post()
Object	ev_obj
Parameters	Name, manufacturer, year, battery, wltp, power, cost

Def get(): When the user clicks on the electric vehicle this function pulls out all the information from ndb datastore and showed in the next page on details.html. This depends on two parameters ‘ev’ electric vehicle and ‘user’ current user.
Def post(): After the details form pulls out, we can view the electric vehicle name, manufacturer, year, battery, wltp, power, cost and ratings given by the users. The information fetches are totally depending on name parameter. 
6.	CLASS DELETE AND EDIT HANDLER
Def get(): Fist of all this check whether the user is logged in or not, since these functions depend on ndb.key values if it is true than it works and pulls out the desired function of edit and deleting the electric vehicle form ndb datastore.
Def post(): After edit method pulls out and allows user to edit the current vehicle, but the name passes through ndb.key therefore no two-electric vehicle with same name stored in datastore.
7.	CLASS COMPARE HANDLER
Def get(): By the help off this function user is able to pull the form from compare.html, where user can compare two or more electric vehicles and compare them on their parameters. If user select only one or none of the electric vehicle displays it show an error message.
Def post(): This function works by the name selected from the compare form. The two or more EV’s selected by the user displayed by their properties. For all the properties the green value shows the best and red shows the lowest and vice versa in the case of cost. User can also view the detail view of electric vehicle and view ratings as well as comments by different user by simply click on the name that work as a hyperlink that leads them directly to the information needed. 

8.	CLASS REVIEW HANDLER
Def get(): Checks weather the user is logged in or not. This function also depends on the ndb.key value of the current user logged in. This pulls out the form from reviews.html.
Def post(): After we redirected to the pulled-out form from reviews.html, user can write the comments and rate the current electric vehicle according to the level of satisfaction. After click on submit button it displays the message for successfully added review to the database.
9.	Webapp2.WSGIApplication
This is the function used to define the route to access the specific requests made by the user. By default, it doesn’t know which page user wants to access therefore, we must define the expected route through routing table in python.

3. DATASTRUCTURE USED (NOSQL) 
This application works on google app engine which supports NoSQL database to store information and don’t rely on traditional database structures and stored more flexible data models. NoSQL database is schema free can handle variety of data even in huge amount, it also helps in replication of data to avoid the single point failure. The data can be store by their key values in the database, all other parameters were stored in wide column structure. This will help us to store huge amount of data with speed development and increased horizontal scalability. 
This data structure is used by google app engine to fully managed the cloud service, which helps replication and handles shredding to ensure the consistent working of the database.

4. DATAMODEL (NDB) 
	This model depicts the structure of the entities stored in the database. Model classes define in the application to indicate the desired entities and their structure. The model is inherited by the given class model can be directly or indirectly inherited from main model. 
NDB model is also used to describe the definition of class declared straightforward used to declare the model class structure. The definition of property helps the system to identify the names and types of field stored in the cloud storage. We used two property of ndb in our application:
1.	String property: is used for name of the electric vehicle, manufacturer and reviews which are limited to store at most 1500 bytes from str.

2.	Integer property: is used to store the values of year, battery, wltp, cost, power and ratings into a singed 64-bit integer.
We also use ndb.key values in put() function, which helps to retrieve the same entity later in the application.




5. DOCUMENTATION OF USER INTERFACE:
1.	This application works on old school color combination of white background and the texts are given in black, which helps in better visibility of text and give good clarity of the user.
2.	Headings are bold and large so can be easily seen and understandable by user.
3.	Simple buttons with good label show the exact functions done by that button.
4.	After login user can use functions which are reserved only for use after login.
5.	Add electric vehicle page consists of simple fields and shows what values we must entre in particular field.
6.	In query page we tried to make the page user friendly by adding two text field for name and manufacturer and sliding bars for the numeric value.
7.	Sliding bar consist of min and max values which shows the vehicle lies in between the values given by user.
8.	Buttons are clearly visible with their desired functions.
9.	In compare page use can select two or more vehicles with the help of check boxes. This give user a friendly interface which is easy to understand and use.
10.	By comparing two or more electric vehicles user can see the cons and pros of the compared vehicles. Green values show the highest or good and red shows the lowest bad, which are easily distinguish while comparing.
11.	User can also see the electric vehicle stored on the database on the main page after login.
12.	This helps the user to find the desired vehicle if the stored list is small.
