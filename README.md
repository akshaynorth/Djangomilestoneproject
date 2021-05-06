# Deployment Instructions

The application is deployed to the Heroku platform. To proceed with the deployment follow
the following steps:

1. Log-in to the Heroku console: www.heroku.com

2. Click on the *Create new app* button

3. In the *App name* field type the name of the application. For this application type:
   *fullstackane*
   
4. Click on the *Deploy* tab on the Heroku dashboard

5. On the *Deployment method* section of the page, click the *GitHub - Connect to GitHub*

6. On the *Connect to GitHub* section click on the **Connect to GitHub** button

7. Tyoe the name of the repo "Djangomilestoneproject" - click on search and then click connect

8. On the pop-up windows that shows up for authorization, click on the **Authorize Heroku**
   button

9. On the GitHub password prompt, type the GitHub account credential password

10. On the Heroku dashboard, go to the *Connect to GitHub* section and type the GitHub repository name then
    click the **Search** button

11. On the repository information show right below the **Search** button, click on the **Connect** button

12. On the *Automatic Deploys* section select the *master* branch as the **Choose a branch to deploy** field selection

13. Leave the *Wait for CI to pass before deploy* unchecked

14. Click on the **Enable Automatic Deploys** button

15. Navigate to the *Settings* tab, then scroll down to the *Config Vars* section

16. Click on **Reveal Config Vars**

17. On the *Key* field enter`DJANGO_SECRET_KEY`

18. On the *Value* field enter secret key, then click on the **Add** button

# MySQL relational database deployment

The Heroku platform provides *Add-ons* that allow the application consumption of third-party services. The 
**JawsDB** add-on was used to deploy the application's MySQL relational database instance.

To deploy the add-on follow these steps:

1. On the Heroku dashboard click on the *Resources* tab

2. In the *Add-ons* text field type *MySQL*

3. From the list of suggested options on the text field select the **JawsDB MySQL** service

4. On the popup window for the **JawsDB MySQL** service order form select the *Kitefin Shared - Free* for the 
   *Plan name*

5. Click on the **Submit Order Form**

6. The **JawsDB MySQL** service appears in the Add-ons section, click on the open icon of the service to open JawsDB
   MySQL console
   
7. On the **JawsDB MySQL** console, take note of the following field values: Connection String, Host, Username, Password
   and Database

8. On the Heroku dashboard, navigate to the *Settings* tab, then scroll down to the *Config Vars* section

9. Click on **Reveal Config Vars**

10. On the *Key* field enter`DATABASE_URL`

11. On the *Value* field enter the database url obtained from the **JawsDB MySQL** console *Connection String*, then 
    click on the **Add** button
    
# Stripe integration deployment

The Stripe payment integration requires both configuration on the Stripe console, and the Heroku platform to store 
and protect API secret keys.

To setup the Stripe payment follow these steps:

1. Go to www.stripe.com on your web browser

2. Click on the Sign-up link

3. Enter your preferred credentials for username and password

4. Provide your personal information: name, address and bank account information. It is important to note that
   the required API secret keys needed to integrate with the service will not be available until all the information
   is provided
   
5. Navigate to https://dashboard.stripe.com/test/apikeys, click on the `Reveal test key`. Notice that for production
   this key will be different. As this site is for testing purposes, click on this button to reveal the test key.
   
6. Click on the secret key to copy it to the clipboard
   
7. Open the Heroku console and navigate to the *Settings* tab, then scroll down to the *Config Vars* section

8. Click on the "Reveal Config Vars" button

9. On the *Key* field enter`STRIPE_API_KEY`

10. On the *Value* field paste the secret key from Stripe copied to the clipboard, then click on the **Add** button

11. Open the following file to provide the Stripe API public key: `static/scripts/recipe_stripe.js`

12. On the Stripe dashboard obtain the public API access key. Navigate to  `https://dashboard.stripe.com/test/apikey`
    then on the publishable API key click on the key to copy it to the clipboard.
    
13. Paste the public key to the parameter of the `Stripe()` object in `static/scripts/recipe_stripe.js`

14. Redeploy the application to the Heroku platform. (e.g. commit, push to Git and deploy application in Heroku)

# Attached Software Architecture Document and Use Case Specification 
# 1.	Introduction
The ComeChop Ecommerce Site (CES) Software Architecture Document (SAD) provides a comprehensive architectural overview of the CES, using a number of different architectural views to depict different aspects of the CES.  It takes the use cases as the guiding source to come up with an CES architecture that satisfies the business and final project requirements.  
# 1.1	Purpose (Fill today)
