# EXPLORE LOCAL
#### Video Demo:  https://www.youtube.com/watch?v=9Zm8TMTyc9I
#### Description:
Explore Local is a web app that allows its users to post ideas about interesting activities or places available in Singapore. Then, users will be able to try out activities and places that they have never experienced, giving them an opportunity to explore the lesser known parts of Singapore.

The functions included in this web app are:
- Register + Login/Logout
- Post
- Edit post
- Search/Filter

#### Register + Login/Logout function:
The homepage can be viewed even if the user is not logged in, or does not have an account. To post or edit one's post, however, the user will have to register for an account (if they have yet to create one), or log in to their own account.

#### Post function:
When users post ideas, they have to include a title, description, and the cost of the activity. The user an choose to include a tag to their post, or give a rating for the activity, having tried it out. This is done under the "Create post" tab.

#### Edit function:
When logged in to their account, users can choose to edit their previous posts. This is done under the "Profile" tab, where they can see their previous posts. When they click on the title of the post they wish to edit, they will be brought a form that is filled in with the previous information, allowing to edit and submit the form.

#### Search function:
The search function is also available to users that do not have an account or are not logged in. By typing in text, the search function will filter through the title, description, rating, cost and tag columns and show the results which contain the search.

#### Possible areas to improve on:
Further functions that can be built for this web app include:
- Comment on posts
- Rate activities posted by other users
- Upload (multiple) images when posting
- Allow users to select multiple tags, and filter for posts by clicking on tags
- Could perhaps combine google maps reviews


### Files in final project
- Static folder
    - favicon.icon (icon for website)
    - styles.css (stylesheet)
- Templates folder
    - apology.html (for displaying errors)
    - edit.html (edit post page)
    - index.html (homepage)
    - layout.html
    - login.html (login page)
    - post.html (for posting posts)
    - profile.html (profile page, showing past posts by specific user)
    - register.html (registering for an account page)
- application.py
- data.db
- helpers.py (apology function + login_required function)
