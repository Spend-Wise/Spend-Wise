### SpendWise v3 Features Overview

- Dynamic Ids
  - Change the simple ids with some Dynamic ids. And implement those ids all across the application
  - Ids that should be changed are User, Budget, Expense IDs.
  - Ids should not be random. There should be meaning to the ids created.
  - All the ids should be UNIQUE.

- Options For LogIn and Forgot Password
  - Option for the user to login with USER ID or the USERNAME. But password should be asked for both of the options.\
  - If the user clicks on the ‘Forgot Password’ button he should be given to verify his/her identity by using the Security Question or sending an OTP to the given email address.
  - The option for the Security Question should only be given if the user has already provided the Security Question. If not there should be only one option (i.e., sending OTP).

- Password Restrictions Universally
  - The length of the password should be 6-10 characters only, not less than 6 characters and not more than 10 characters.
  - There should be at least 1 of each of the following in the user provided password:
    - Uppercase alphabet
    - Lowercase alphabet
    - Number
    - Symbol
  - There should be no continuous strings on the keyboard (such as QWERTY, 123456) in any format (UPPERCASE, LOWERCASE, MIXED).
  - There should also not be the words like ‘PASSWORD’ in the password given by the user.
  - The FIRST & LAST NAME also should not be in the password provided.

- Password Change Restrictions
  - Universal Password Restrictions Included.
  - The last 5 passwords should not be the same.

- Import Database Functionality (AUTO)
  - Secret Window for IMPORTING the backed up database if needed.
  - Only the user with specific USER TYPE (i.e., admin) should be able to import the database & also be able to open the Import database Window.
  - This window should open only when the user has been logged in the main Page.
  - Ask for the remark for why importing the database importing from the backup file
  - Keeping the record of the imports in a JSON file of the following:
    - How many times has the database been imported from the backup file?
    - Date and Time of each import.
    - The username of the user who imported the database from the backup file.
    - The remark for importing the database from the backup file.

- Retool Database Transition
  - Transition completely to the RETOOL database. All the tables and all the utilities that are related to the database
    - Database Structure Ensuring System
    - Automatic Database Backup System
    - User Database Backup System
  - Rename the REGISTRATION table to the USERS table..

- USER Backup System
  - Option to backup specific budgets or the selected budgets created by the user.
  - Option should be available in the PROFILE menu
  - TabView for creating and the backup and importing the created backup.
  - If the budget with the same BUDGET ID is in the backup file. Ask the user which budget should be imported in the database either which is in the backup file or which is current. Check this for every budget.
  - Toplevel for the above Window feature which shows the above condition and two buttons
    - IMPORT
    - DON’T IMPORT
  - And the budgets with the different BUDGET IDS should be imported automatically. After all the budgets are imported. Show a message showing all the imported budgets.

- Database Utilities
  - All the Database Utilities only should show up only when the user is logged in with the USER TYPE of ADMIN.
  - User with the USER TYPE user should not be able to open these Database Utilities

- Centralized Queries
  - There should not be queries created in the main code file.
  - There should be a separate file for all the SQL queries that are used in the whole code.
  - And all the queries should be imported from this file to the file where that query is needed.

- Appearance
  - Option of changing the appearance of the application should be available in the PROFILE menu.
  - The appearance changes should be remembered and should be applied when the user logs in to the main page of the application.
  - Appearance Options
    - Theme - Light / Dark / System
    - Full Screen Mode

- Budget Status
  - Remove the archived and closed fields in the database & add a new field called status.
  - There can be only 3 statuses of any budget
    - Open
    - Archived
    - Closed

**Settings Menu**

- Currency - (Dialog)
  - Change Currency Button
  - Options for changing the currency
    - Change only the Symbol
    - Convert current currency to the user selected currency (as per the market status of that currency)
    - Show details if the user want to convert the currency
      - Current Value
      - Converted Value

- Archived Budgets
  - [Toggle] ALLOW / DON'T ALLOW to change the budget settings when the budget is archived. (DEFAULT - Allow)
  - Allow the archived budgets to be deleted from the archived menu directly (DEFAULT - Yes)

- Default One Time Expense Limit (O.T.E.L) for every budget - (Toggle & Input) [DEFAULT - off]
  - If Toggle is ON ask the expense limit to the user (DEFAULT - same amount as the Budget Amount)

- Setting Category (of Budget & Expense) - (Toggle) [Default - OFF]
  - Ask for changing Category Everytime the budget is created - Dialog appears if the toggle is ON

- Export Budget 
  - [Toggle] Send the exported file to the provided Email address by the user. [Default - Ask Every time]
  - [Toggle] Send email after any budget is exported (Default - NO)

- Expenses Related Settings
  - [Toggle] Serialize the expense name only if the expense name is not provided by the user. (Default - NO)
  - [Toggle] Show the date and time of the expense added in the View Expenses [Default - NO]

- [Toggle] Send Email is the status of the budget changes and also include all the details of that budget. (Default - NO)
  - Statuses
    - Open
    - Archived
    - Closed

- Budget Utilities
  - Export Every Budget for all the statuses.
    - Give the option to put all the budgets in a single file, or create a separate file for every budget
    - If the user selects make different export file then put all the files in a .zip
  - Send the whole details to the user on the given email address.
    - Send only for the budgets with the Status OPEN.

**Profile Menu**

- Edit Information
  - First Name
  - Last Name
  - Email
  - Username

- Security Section
  - Update Password
  - Add or Remove
    - Security Question
    - 2FA

- Add a Profile Picture
  - Give a Selected number of options to choose a profile picture.

- Show the date of the account created at the very end of the profile menu.

- Sections in Profile Menu
  - Profile Menu
  - Appearance Menu
