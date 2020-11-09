# Simple promo system 

to create normal or administrator user please create super user first

./manage.py createsuperuser

then log into admin and add new normal user and administrator user 

# Created endpoints 

1- POST /api/promo  [ for administrator user only ] to create promo

2- GET /api/promo  [ for administrator user only ] to list promos

3- PATCH /api/promo/{promo_id}  [ for administrator user only ] to update promo

4- DELETE /api/promo/{promo_id}  [ for administrator user only ] to delete promo

5- GET /api/me/promo  [ for Normal user only ] to list logged in user promos

6- GET /api/me/promo/{promo_id}/points  [ for Normal user only ] to get promo points

6- POST /api/me/promo/{promo_id}/use  [ for Normal user only ] to use promo points
