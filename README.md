# Blog APP

📔️ Feature-rich blog application using Django Framework
## Youtube Video Preview
[![Blog Project Preivew](https://img.youtube.com/vi/OH_paaKBRUU/0.jpg)](https://www.youtube.com/watch?v=OH_paaKBRUU)

## Main Features
*   **User Authentication:**
    
    *   Implemented user registration and login functionalities using Django's built-in authentication system.
*   **Post Management:**
    
    *   Developed Create, Read, Update, and Delete (CRUD) operations for blog posts.
    *   Implemented rich text content creation using Django's TextField for flexible post formatting.
*   **Tagging System:**
    
    *   Designed a tagging system allowing users to categorize posts with relevant tags.

*   **User Interaction:**
    
    *   Implemented a "Like" system allowing users to express appreciation for posts.
    *   Integrated a comment system enabling users to engage in discussions about blog posts.
*   **User Profiles:**
    
    *   Created user profiles with customizable avatars and additional bio information.
*   **Frontend and Backend Integration:**
    
    *   Incorporated AJAX requests for seamless user interactions without full page reloads.
*   **Security Measures:**
    
    *   Ensured proper user authorization to control access to post creation and modification.
*   **Responsive Design:**
    
    *   Developed a responsive user interface for optimal viewing across various devices.


  
## Installation

- open the project folder using any IDE
```bash
pip3 install -r requirement.txt
```

```bash
python3 manage.py makemigrations
```

```bash
python3 manage.py migrate
```

```bash
python3 manage.py runserver
```

- for password reset functionality to work these lines at `core/settings.py` should be replaced with the existing Gmail account 
```python
EMAIL_HOST_USER = '<google email>'
EMAIL_HOST_PASSWORD = '<google email password>'
```
