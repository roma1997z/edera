# General info
Backend: Django
Frontend: bootstrap, jquery, ...

#Structure

- landpage (main page)
- lms (the platform) https://www.edera-school.com/lk
- templates (for signup, login)

## LMS module
 
### strater.html:
main template for all patform pages
- global design here
- create great menu

### teacher_list.html:
searching, like/dislike teachers
filter applied changes user interests in database
- improve ui

### interest_form.html:
filter form for teacher search, can be embedded in different pages
Form is backend-automized: gets keys and interests form database

### profile.html:
to change name, contacts, ...
- second priority

### lesson_list.html:
list of lessons and liked teachers
- second priority

### teacher_desc.html:
change teacher descriptions for certain fields
Form is backend automized: gets label key and textareas for them
- third priority as only visible for teachers


## Login/logout (templates/)

### base.html
main look for all sign-in/auto actions

###registartion/login.html
login form
- improve ui

### signup.html
sign up form
- improve ui