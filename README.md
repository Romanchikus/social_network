# social_network

It's a ready-made REST application, for adding posts by user.

## :white_check_mark:api/:

Any logged and authorized user can see posts and their owners - "posts/". 
By link "users/<str:username>/" we see all posts for this user.
"users/" - List of users and their activity.
Owner of the post can edit this post - "posts/<int:post_id>/manage".
"posts/<int:post_id>/" - Details of post.
Users can create  new posts by yourself - "posts/create/".
Users can estimate all posts [ "posts/<int:post_id>/like_toggle/", "posts/<int:post_id>/dislike_toggle/" ].
We can see some analytics for posts in the date range - "analytics/".

## :white_check_mark:auth/:

And of course you can register - "users/" and create JWT token - "/auth/jwt/create/".
