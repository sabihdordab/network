# Network
## About Project :

A Twitter-like social network website for making posts and following users.

## [Specification/Features](https://cs50.harvard.edu/web/2020/projects/4/network/)
- **New Post:** Users who are signed in can be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
- **All Posts:** The “All Posts” link in the navigation bar take the user to a page where they can see all posts from all users, with the most recent posts first.
    - Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.
- **Profile Page:** Clicking on a username loads that user’s profile page. This page could:
    - Display the number of followers the user has, as well as the number of people that the user follows.
    - Display all of the posts for that user, in reverse chronological order.
    - For any other user who is signed in, this page also displays a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts.
- **Following:** The “Following” link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
    - This page behaves just as the “All Posts” page does, just with a more limited set of posts.
    - This page only be available to users who are signed in.
- **Edit Post:** Users are able to click an “Edit” button on any of their own posts to edit that post.
- **“Like” and “Unlike”:** Users are able to click a button or link on any post to toggle whether or not they “like” that post.

### Languages And Technologies :

**Back-end** :

- Python ( Django Framework )
- SQLite
- Java Script

**Front-end** :

- HTML
- CSS & Bootstrap
- Java Script



## How to run the Project:

- Install project dependencies by running `pip install -r requirements.txt`
- Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
- Run the project by running `python manage.py runserver`


