# Project Proposal for Atomic ACO Freebies Web Application

## Introduction
The Atomic ACO Freebies web application aims to provide a streamlined platform for users to sign up for freebies through a multi-step registration process. The application is built using Flask and integrates multiple external APIs to enhance functionality and user experience.

## Objective
The primary objective of this project is to:
- Create an engaging web interface where users can register for freebies.
- Integrate external APIs such as Stripe for payment processing and Discord for OAuth2 authentication.
- Use Google Sheets for data persistence to store user registration data securely.

## Proposed Solution
The application will feature a multi-step form process, allowing users to input their information, choose optional add-ons like coupons, and complete their registration through a secure payment gateway.

### Flow of the Project
1. **User Registration:**
   - Users start at the homepage and are redirected to the signup page.
   - The signup process is divided into multiple steps, each handled by separate routes within the Flask application.

2. **Login and Authentication:**
   - Users can log in or register using their Discord account, facilitated by OAuth2.

3. **Form Submission:**
   - Users fill out forms to input personal details, preferences, and payment information.
   - Data validation is performed at each step to ensure accuracy and completeness.

4. **Coupon Application (Optional):**
   - Users can enter a coupon code during the registration process.
   - The application verifies the coupon validity using Stripe’s PromotionCode API.

5. **Payment Processing:**
   - On completion of the form, users are directed to a Stripe checkout session for payment processing.
   - After payment, users are redirected to a confirmation page with details of their registration.

6. **Data Storage:**
   - All user data from the registration process is stored securely in Google Sheets, ensuring data persistence and easy access for administration.

7. **Notifications and Confirmation:**
   - Users receive confirmation of their registration via a direct message on Discord from the application’s bot.

### Technologies Used
- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** Stripe, Discord OAuth2, Google Sheets
- **Database:** Google Sheets as a makeshift database

## Goals
- To ensure a seamless and secure user experience from start to finish.
- To integrate and utilize external APIs effectively within the Flask framework.

## Conclusion
This project will leverage modern web development technologies and practices to deliver a comprehensive solution for managing user registrations for freebies. It will demonstrate the capabilities of integrating multiple APIs and services to create a functional and responsive web application.
