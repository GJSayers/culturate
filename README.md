<h1 align="center">Culturate</h1>
-------
![Mockups](static/images/screen-shots/mock-ups.png)

[View the live project here.](https://culturate.herokuapp.com/)

Culturate is a cultural places, exhibitions and events site. It is designed to be responsive and accessible on a range of devices, making it easy to navigate for potential contributors and people looking for information across a number of devices.

## Strategy 
-------
### User Stories - First Time User A (Community User)
-------
1. As a **First time user**, I want to have a clear visual impact on landing on the site to demonstrate the **artistic** / **cultual sharing** & **listing** purpose of the site. 
2. As a **First time user**, I want to be able to **browse at least some listings** without having to sign up / login. 
3. As a **First time user** I want to be able to **join** the community **easily and securely** 

#### User Stories - Existing User B (Community User)
-------
1. As an **Existing User** I want to be able to **login** easily. 
2. As an **Existing User** I want a **Personalised experience** by being able to **like** or **save listings** for future reference.  
3. As an **Existing User** I would like to be **addressed by my username**
4. As an **Existing User** I would like to be able to **upload listings** for others to see. 


##### User Stories - Repeat/ Frequent User C (Logged in / joined member)
1. As a **Repeat User** I would like to be able to **edit my likes and saves** 
2. As a **Repeat User** I would like to be able to **search the listings** 
3. As a **Repeat User** I would like to be able to **edit and update my profile**
4. As a **Repeat User** I would like to be able to **edit or update the comments on my listings**


#### User Stories - Site Manager / Admin User D
-----
1. As a **Site Manager / Admin User** I want to be able to **create new categories**
2. As a **Site Manager / Admin User** I want to be able to **edit / delete listings** if necessary. 
2. As a **Site Manager / Admin User** I want to be able to **edit / users** if necessary. 
3. As a **Site Manager / Admin User** I want to ensure that the website **stays up to date**, and **automatically deletes** events that have passed. 

#### Website Owner Goals
-------
* The possibility to in the future gain commission from being a referrals site if the site were to become popular.  For this to happen, the site must look polised and have great UX for user buy-in. 

## Scope
-------

#### Product Objectives & Functional Requirements

* Listing pages that can store **user ratings** and **be favourited** by the user. 
* Easy UI to **upload listings**
* **Admin dashboard/ admin access** to be able to monitor and edit content. 

#### Scope 
* Responsive layout to ensure **optimal visuals**
* The site must **store data securely**
* The administrator must be able to access data through the website to edit or delete the records of users or listings. 
* The website should be able to function as close as possible to the following user-story based requirements:
![Functional-Testing](static/testing/functional-testing-design.png)
* The website should aim to have good browser performance and follow accessibility guidelines

#### Core Features
-----

#### Feature Feasibility *MVP vs Full Features
-----
#### 1st Round Selected Production Features 
-----
#### Future Implementations
-----
#### Content and Structure requirements
-----

### Structure
#### Conceptual Design 
* I used Lucid Chart to put together a flow chart of the relationships between the data and actions taken by users as an initial guide to aide the design process.  
![Conceptual Design Chart](static/images/screen-shots/culturate_conceptual_design_chart.png)
* This also helped to identify secutiry measures to be taken into account, and which CRUD operations are performed by which user - The flow was slightly modified throughout design to satisfy the user stories.  The 'liked/saved' block also represents the read part of CRUD. 
#### Database Schema
* Original database Schema design consisted of 3 collections in MongoDB Users, Galleries, Categories: 
![Original Schema](static/images/screen-shots/schema-original.png)

* In the practicality of actually constructing the user journeys and features it was necessary to edit the schema to include more generic term listings instead of galleries so that on-page semantics were correct.  
* As well as this, there was the need to add array of dictionaries to store the user-ratings. During the process of the project, I also solidified the terminology and named the final schema in a more semantically correct manner.
* Final Schema was still 3 collections and during the project I learnt how to access the sub-collections:
![Final Schema](static/images/screen-shots/schema-final.png)

### Skeleton
#### Element arrangement considerations
#### User feedback arrangements

#### Wireframes 
------
The initial designs were sketched out of Balsamiq with some of the form views being the same across device sizes to ensure more impact on the visual pages such as the listing pages.  
Here are the wireframes for the skeleton design planning:
![Wireframes](static/images/skeleton/culturate-form-all-devices.png)
![Wireframes](static/images/skeleton/culturate-home-desktop.png)
![Wireframes](static/images/skeleton/culturate-home-ipad.png)
![Wireframes](static/images/skeleton/culturate-home-page-mb.png)
![Wireframes](static/images/skeleton/culturate-listings-categories-dtop.png)
![Wireframes](static/images/skeleton/culturate-listings-categories-ipad.png)
![Wireframes](static/images/skeleton/culturate-listings-categories-mb.png)
![Wireframes](static/images/skeleton/culturate-submission-form-ipad.png)

### Surface & Prototypes
I then wanted to get an idea of how the colours and imagery would work so I did some planning on Figma too - I just selected a few key pages to illustrate an idea of houw the colours would come out:
![Prototypes](static/images/screen-shots/surface/figma-screen-design.png)

#### Design Inspiration & Colour choices 
* The over-all concept came from the anticipation of getting out to access cultural activities after the lockdown period.  
My hometown of Eastbourne has an inspirational gallery - the Towner Gallery, which is painted in rainbow by artist Iothar Gotz.  
I used an image of the gallery for landing page, and took colour design inspiration from this pallet - offering an alternative to the sometimes staid and serious gallery website design approach to give a vibrant design feel that will appeal to multiple user-groups and elicit a vibrant positive feeling for users. 
![Towner](static/images/screen-shots/towner-gallery.png)
I translated the colour pallet using Coolors to get the hex and RGB codes to use in CSS:
![Color-Palette](static/images/screen-shots/colour-palette.png)

##### Typography
* For the Typography, it was necessary to chose classically no nonsense font, so I chose Archivo, but to complement for forms (where information is being shared) and profile pages where the user is likely to be already an engager used, I chose Permanenet Marker to personalise. 
##### Imagery
The Imagery of the website will be based on the user contributions, but to set the theme, the homepage is a parallax containing two striking colourful artworks. 
Where there may be times where an image is not uploaded, there is a standby image to populate incase.
Here is the homepage ![Homepage](static/images/screen-shots/surface/home-page-imagery.png)
Here is an example of a listing page: ![Listing-Page](static/images/screen-shots/surface/listing-page.png)
You will see that I decided to dial back the yellow, and keep most backgrounds aside from forms with the #1a2017 and use the colour as pops, letting the art imagery sign it's own song. 


## Implementation 

## Technologies Used

### Languages Used

*  [HTML5](https://en.wikipedia.org/wiki/HTML5)
*  [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
*  [Javascript]
*  [Jquery]
*  [Python3] (https://www.python.org/)

### Frameworks, Libraries & Programs Used

*  [Jinja] (https://en.wikipedia.org/wiki/Jinja_(template_engine))
*  [MaterializeCSS] (https://materializecss.com/) is used as a css framework to ensure responsive design delivery within the timeframe. 
*  [Heroku](https://www.heroku.com) is the cloud-based platform used to deploy the project. 
*  [MongoDB](https://www.mongodb.com) is used for the document database.
*  [Flask] (https://en.wikipedia.org/wiki/Flask_(web_framework)) is used as a micro-framework and supports the use of Jinja templates. 
*  [Figma] (https://www.figma.com/)
*  [JQuery] (https://jquery.com/)
*  [Hover.css](https://ianlunn.github.io/Hover/) I used hover to make elements more interactive.
*  [Google Fonts](https://fonts.google.com/) 
*  [Font Awesome](https://fontawesome.com/) Font awesome is where I sourced all the icons for the site.
*  [GitHub](https://github.com/) is used to file the repository and record the version control. 
*  [GitPod](https://gitpod.io) was used for development and version control.

)

## Testing

Detailed testing documentation can be found in [TESTING.MD] (/workspace/culturate/TESTING.MD)

### Known Bugs

## Deployment

### Forking the GitHub Repository

### Making a Local Clone

### Credits
* Content
* Media
* default image (if no listing image uploaded) https://www.isupportstreetart.com/students-benefit-street-art/


### Acknowledgements
