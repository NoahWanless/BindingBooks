console.log("Hello, things are working when this page is loaded!")

fetch("/config/") //goes to this link and gets the jsonresponse it returns
.then((result) => { return result.json(); }) //then takes the resulst and its its json
.then((data) => { //using that data it makes a const of the public key
  // Initialize Stripe.js
  const stripe = stripe(data.publicKey);
});

