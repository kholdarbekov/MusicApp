# MusicApp
Capstone design project. Features: karaoke, charts, custom playlists, upload your own cover to website so that others
can listen to it, and many other features are there.

In the following you can find about:

1. How to use this app
2. Additional features

---------------------------------------------------------------------------------

index - list, artists     -------   new songs, top songs
sign up
sign in
about
contact
genre - songs

create playlist, upload songs, karaoke, push notification when someone likes or votes

profile settings
follow other users

left aside:
    home
    news
    top songs
    genres
    uploads

    black:
    playlist +
    2 best playlist

---------------------------------------------------------------------------------
1. How to use this app

* When you open this app you will see login page.
  You need to signup first if you haven't registered yet.
  Then you will be redirectered into main activity.

* In main activity you can add, update, delete your memos
  Press "Add" button to add new memo.
  Then, you will see another activity where you set memo info:
  its date, text, and picture.
  To save memo click on "Save" button, click on "Cancel" to cancel and go back
	    
* When you are adding pcture, you will have 2 options: camera and gallery.
  Before running application, do not forget to give permission for camera and 
  gallery pictures. To do this, press and hold on app icon, drag onto "App info"
  on the top-left corner of your screen, and then, give camera permission.	

* If you want to delete memo, press particular delete icon on the right side of 
  memo.

---------------------------------------------------------------------------------

2. Additional features

* App uses database to store all data, thus if you quit and come back, you can
  see your memos.

* Authorization: when you open app, you will be asked to login, and you can only
  see memos that you have created. You cannot see and modify other user's memo.
  We provided seperate activity for each user.

* Our database consists of two tables, one for auth, and the other is for memos.
  Which means, we store all memos according to user who created them.
  And no any two users with the same username is allowed. 

* When users login into system, we store auth information on sharedPreference,
  where username is unique id and primary key. According to that username,
  app loads all memos created by this user only.

* You can not only add and modify, but can also delete your memo.
  When you click on delete icon, you will be asked confirmation to delete.
  Just in case if you mistakenly clicked the delete icon, you can cancel it.

* While adding and updating memos, it checks validity and abnormal  cases.
  No empty space, particularly, text field, date picker, 
  is accepted. It will warn you on "Save" button click. 
  But user may not upload photo if he wants. Then, he will se default picture.

* Friendly and beautiful look-and-feel for users. In order to make app more
  friendly, we used different layouts, linear, relative and nested (misture
  of many layouts where appropriate)

* We used libraries as well. Particularly, Butterknife, circleimageview to make 
  circle image layout for better design.

* There is MY_PERMISSIONS_REQUEST_READ_EXTERNAL_STORAGE function to check 
  permission, which extends Utility.java class taht we created.
  Both camera and  gallery options requires storage access.
