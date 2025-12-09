this is a test to ensure i have git set up correctly
requirements:/imports that exist at the moment for the venv:

black
django
python-decouple   <--for getting env vars for secert key 
stripe
brew install stripe/stripe-cli/stripe <-- this is for getting messages from the stripe api


Model structure:
if you want to see the model structure see the file/image named model_back in this dicectory


super user(i think thislly work for other people)
username: jerry
password: testpasss123

another one:
username: test
password: testpasss123

*note that the password has 3 s's in it*



this is the test credit card, the CV number is any 3 digit number and the mouth date just needs to be 
anny date in the future, like '12/28'
4242 4242 4242 4242

also for like billing info you dont have to bother putting anything really, like 77777 will work for that one
5 digit billing number


to use fake stripe checkout need 
stripe_fake_checkout=True (this can be changed to False if needed but only really me(Noah) would need to use that for now)

stripe commands:

stripe logs tail          <--this displays api messages post/gets that stripe gets
stripe listen --forward-to {insert the url for the webhooks view}

stripe listen --forward-to localhost:8000/payments/webhooks/stripe/



https://onetimesecret.com/en/
to be used for sharing secret key


pip install model-bakery




ada stuff, styling fixing the stuff on the products move the footer to the actual bottom of the screen for forum 