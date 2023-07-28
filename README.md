[![Test and Deploy](https://github.com/aalmobin/task_management_system/actions/workflows/build_test.yml/badge.svg)](https://github.com/aalmobin/task_management_system/actions/workflows/build_test.yml)

# task_management_system

## Project Description
The project idea was to create a task management system

## Python version: 3.11+

## Instructions to run the script

1. Goto the directory where you want to store your project.
2. Clone the git repository to the project directory.
3. Open the terminal and navigate to the project directory from the terminal.
4. If you don't have `pdm` installed then install it by typing `pip install --user pdm`.
5. Install the project dependencies by typing `pdm sync` on the terminal.
7. Migrate the database by typing `pdm migrate` on the terminal.
8. Create admin user if you want by typing `pdm createsuperuser` and give the required credentials on the terminal.
9. Now, Run the project from your **localhost** by typing `pdm start`
10. You can Run Unit Tests by typing `pdm test`
11. Navigate to the URL [127.0.0.1:8000](127.0.0.1:8000) or [localhost:8000](localhost:8000) from your browser.
12. You can terminate the server anytime by **CTRL+c**.

### URL's I've implemented:
* api/v1/tasks/
* api/v1/tasks/{task_id}/
* api/v1/tasks/{task_id}/add_assignee_in_task/
* api/v1/tasks/{task_id}/remove_assignee_in_task/
* api/v1/tasks/{task_id}/change_is_completed/
* api/v1/comments/
* api/v1/comments/{comment_id}
* api/v1/register/
* api/v1/token/
* api/v1/token/refresh/
* api/v1/users/
