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
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

### Instructions for Use

#### Prerequisites

Before you begin, ensure you have installed on your local machine the [requirements.txt](https://github.com/SamueleCentanni/Django_Project/blob/main/requirements.txt) file.

#### Installation Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/SamueleCentanni/Django_Project
    cd Django_Project
    ```

2. **Install the required packages**:
    ```sh
    pipenv install

3. **Create and activate a virtual environment using Pipenv**:
    ```sh
    pipenv shell
    ```  ```

4. **Set up Redis**:
    - Ensure Redis is installed and running on your local machine. You can download it from [redis.io](https://redis.io/download).

5. **Apply database migrations**:
    ```sh
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

8. **Access the application**:
    - Open your web browser and go to `http://127.0.0.1:8000/`.

#### Additional Commands

- **Running tests**:
    ```sh
    python manage.py test
    ```

- **Updating image rankings**:
    - Make sure your `update_ranking` management command is properly set up. You can run it using:
      ```sh
      python manage.py update_ranking
      ```

#### Notes

- Ensure that the Redis server is running before starting the Django development server.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
### Credits

This project was developed as part of a Django course, with inspiration from Instagram's social media features.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

### License

This project is licensed under the MIT License.