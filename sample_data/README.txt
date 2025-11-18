to start fresh, if you want to have only the sample data and not any of the stuff you created prior to right now, follow these instructions. this gets rid of the model objects for ALL of the apps, not just yours

step 1: delete db.sqlite3 file
step 2: run python manage.py migrate

for windows folks
step 3:
run python manage.py loaddata sample_data/<filename>.yaml 
repeat step 3 for each sample data file in the folder.
or
python manage.py loaddata sample_data/accounts.yaml sample_data/products.yaml sample_data/forums.yaml

for macOS/linux ***note i didnt test this since i use windows***
step 3: run python manage.py loaddata sample_data/*.yaml


if you make changes to a previously existing sample_data, and want to remove old instances of just that model do this

step 1: run python manage.py shell
step 2: >>>from <app_name>.<models> import <model_name>
step 3: >>><model_name>.objects.all().delete()

example
from accounts.models import base_user
base_user.objects.all().delete()

then be sure to run 
run python manage.py loaddata sample_data/<filename>.yaml 


if you are having issues, i suggest deleting the .sqlite3, migrating, and then running loaddata again. any time a model is updated, you will need to migrate at the very least.