## Code Validation

### HTML

HTML code was tested using the [W3C Validator](https://validator.w3.org/) via URI.

<details>
<summary>Screenshots and results for all templates.</summary>
<br>

**HOME**

![No Errors or Warnings to show](documentation/html-home.png)

**IMAGE POST**

![No Errors or Warnings to show](documentation/html-imagepost.png)

**PROFILE**

![No Errors or Warnings to show](documentation/html-profile.png)

**PROFILE POSTS**

![No Errors or Warnings to show](documentation/html-profileposts.png)

**DRAFT POSTS**

![No Errors or Warnings to show](documentation/html-draftposts.png)

**TAGS LIST**

![No Errors or Warnings to show](documentation/html-tagslist.png)

**TAG POSTS**

![No Errors or Warnings to show](documentation/html-tagposts.png)

**UPLOAD IMAGE**

![No Errors or Warnings to show](documentation/html-upload.png)

**NOTIFICATIONS**

![No Errors or Warnings to show](documentation/html-notifications.png)

**REGISTER**

![No Errors or Warnings to show](documentation/html-signup.png)

**LOGIN**

![No Errors or Warnings to show](documentation/html-login.png)

**LOGOUT**

![No Errors or Warnings to show](documentation/html-logout.png)

**ABOUT**

![No Errors or Warnings to show](documentation/html-about.png)

**CONTACT**

![No Errors or Warnings to show](documentation/html-contact.png)

</details>

### CSS

CSS code was tested using the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) via text input. 

<details>

<summary>Screenshots with results for the styles.css file</summary>

![No Error Found](documentation/css-valid.png)

![Valid CSS information](documentation/css-info.png)

</details>

### Javascript

Javascript code was tested using [JSHint](https://jshint.com/).

<details>

<summary>Screenshot with results for the imagepost.js file</summary>

![JSHint feedback](documentation/js-script.png)

the undefined variable of 'bootstrap' is caused by cross referencing scripts

</details>

### Python

### Lighthouse

### Responsivness

All webpages are responsive with the [Boostrap grid](https://getbootstrap.com/docs/5.3/layout/grid/) layout. The breakpoints of col-sm, col-md and col-lg where used respectivley for mobile, tablet and laptop screens

<details>

<summary>Home page examples</summary>

**HOME**

![responsive laptop page](documentation/responsive-laptop.png)

**TABLET**

![responsive tablet page](documentation/responsive-tablet.png)

**MOBILE**

![responsive mobile page](documentation/responsive-mobile.png)

</details>

### Browser Compatability

I have tested the website in Chrome, Firefox and Edge

### Manual Featrures Testing

<details>

<summary>List of all passed tests</summary>

**NAVBAR**

- Navigates to:

  - Home page when logo is clicked
  - Tags page when 'Tags' is clicked
  - Sign up page when 'Register' is clicked
  - Login page when 'Login is clicked
  - Logout page when 'Logout' is clicked
  - Upload page when 'Upload Image' is clicked
  - Notifiactions page when bell icon is clicked
  - Profile page when profile image icon is clicked
  - Search page when 'Search' button is clicked

- On mobile and tablet, opens as dropdown menu when burger button is clicked
- Displays different links based upon user authenticated status

<br>

**FOOTER**

- Navigates to:

  - About page when 'About' is clicked
  - Contact page when 'Contact' is clicked

<br>

**HOME**

- Displays only approved image posts
- Page navbar available when there are greater than 6 images
- Navigates to selected page when clicked
![Pagination page navbar](documentation/test-page-navbar.png)
- Navigate to specific imagepost when image is clicked

<br>

**IMAGEPOST**

- Displays image card with:

  - Image
  - Working link to uploader's profile
  - Title
  - Thumbs up/down icon if liked/not liked
  - Message
  - Created on
  - Update button

- Click on image toggles fullscreen image modal
- Click on modal image exits modal
- Click on image thumbs up redirects to page with alert message:
![Added like to image](documentation/test-alert-likeimage.png)
- Click on image thumbs down redirects to page with alert message:
![Added like to image](documentation/test-alert-unlikeimage.png)

- Comments displayed with:

  - Working link to author's profile
  - Created on 

<br>

**TAGS**

- Displays all tags
- Navigates to specific tag when specific tag is clicked

<br>

**TAG POSTS**

- Displays all approved images with requested tag
- Displays card when no approved images yet with tag
![No approved images with tag card](documentation/test-no-approved-images-with-tag.png)
- Navigate to specific imagepost when image is clicked

<br>

### Automated Testing