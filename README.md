# Teacher Directory

## Execution Steps

1. Install <b>git</b> on the system.
2. Open shell/command prompt and run following command to clone the project:
    <br>`git clone https://github.com/Rashiddev/teacher_directory.git`
3. Make sure <b>python3</b> and <b>pip3</b> is installed on the system.
4. Once inside the project's root directory, install requirements from <b>requirements.txt</b> using below command:
    <br>`pip3 install -r requirements.txt`
5. Run this command inside the project directory to start the server:
    <br>`python3 manage.py runserver 8000`
6. Open this URL to view 'directory':
    <br>http://127.0.0.1:8000/
   <br>Above URL will redirect to http://127.0.0.1:8000/directory/teachers/.
   <br>The teachers page shows list of teachers. Currently, it's showing only <b>first_name</b>, <b>last_name</b> and <b>email</b> on the listing page.
7. There are 2 filters at the top:
    1. In the <i>Last name starts with</i> filter, you can only provide first letter of the last name of the teacher.
    2. In the <i>Subject name</i> filter, you can pass 1 subject at time to search for it's teacher.
8. There is a link on the <b>first name</b> of the teacher, once you'll click on it, it will take you to the detail page.
9. In order to import teachers from CSV into the system:
    1. Go to this url: http://127.0.0.1:8000/admin/login/
    2. Provide following username and password:
       - username: admin
       - password: admin@123$
    3. Once logged in, click on <b>Teachers</b> menu under <b>Directory</b>, that will show all the teachers.
    4. Inside teachers listing page, click on <b>IMPORT</b> button on top right section.
    5. Choose CSV file. Make sure CSV file has following headers:
        `first_name,last_name,profile_picture,email,phone,room_no,subjects`
        Note: Sample file is already given in the root directory.
    6. Select <b>csv</b> format.
    7. Click on <b>Submit</b> button. If there are no errors, that will provide you with the preview of the csv data.
    8. If no image is provided, default image profile image will be '21167.JPG'.
    9. Click on Confirm Import. Once clicked it will import teachers into the system.
10. To export order:
    1. Go back to 'teachers listing page' and click on 'Export' button on top right.
    2. Select the format and click 'SUBMIT' button, that will export the teachers.
    
- <b>Note</b>
    -   In order to add more profile images, upload images to `project/static/images` folder and run following command:
    <br>`python3 manage.py collectstatic`
