# Django_Project
A Django-based social media web app inspired by Instagram, featuring user authentication, photo sharing, social interactions, and performance optimization using Redis.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

### Project Description

**Progetto DJANGO: Social Media Web Application**

This project is a social media web application inspired by Instagram, developed using Django. The app includes the following features:

- **User Management**:
  - Generic users with functionalities for Login (including Google authentication), Logout, and Registration.
  - Personal profile area with options to update user data.

- **Photo Sharing**:
  - Users can share photos from their local device or directly from external websites using jQuery.
  - A dedicated section for users to view all their published images.

- **Social Interaction**:
  - Users can follow each other.
  - Users can like and unlike images using AJAX and jQuery.
  - Users can view other users' profiles, their followers, and their uploaded images.
  - A section to view recent interactions of the users they follow, including actions like new follows and likes on images.

- **Performance and Data Management**:
  - Utilizes Redis for high-speed data storage, caching, and message brokering.
  - Tracks image views and generates a ranking of the most viewed images on the platform.

- **Image Details**:
  - Each image includes the number of likes, view count, title, description, and the image itself.

This project demonstrates the integration of various web technologies and provides a robust platform for social interaction and media sharing.
