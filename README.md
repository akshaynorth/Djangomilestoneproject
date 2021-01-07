# Deployment Instructions

The application is deployed to the Heroku platform. To proceed with the deployment follow
the following steps:

1. Log-in to the Heroku console at: www.heroku.com

2. Click on the *Create new app* button

3. In the *App name* field type the name of the application. For this application type:
   *fullstackane*
   
4. Click on the *Deploy* tab on the Heroku dashboard

5. On the *Deployment method* section of the page, click the *GitHub - Connect to GitHub*

6. On the *Connect to GitHub* section click on the **Connect to GitHub** button

7. On the pop-up windows that shows up for authorization, click on the **Authorize Heroku**
   button

8. On the GitHub password prompt, type the GitHub account credential password

9. On the Heroku dashboard, go to the *Connect to GitHub* section and type the GitHub repository name then
   click the **Search** button

10. On the repository information show right below the **Search** button, click on the **Connect** buton

11. On the *Automated Deploy* section select the *master* branch as the **Choose a branch to deploy** field selection

12. Leave the *Wait for CI to pass before deploy* unchecked

13. Click on the **Enable Automatic Deploys** button

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
   
7. On the **JawsDB MySQL** console, take note of the following field values: Host, Username, Password and Database

8. Use the values obtained for the `DATABASES` dictionary in the `settings.py` for the Django project
