# Task Manager

A full-featured task management system built with Django, featuring real-time deadline tracking, status filtering, and a responsive UI.

## Features

- Task creation, editing, and deletion
- Status tracking (To Do, In Progress, Done, Missing)
- Automatic deadline monitoring with visual indicators
- Search functionality
- Status filtering
- Responsive UI with animations and visual feedback
- Color-coded task statuses

## Tech Stack

- **Backend**: Django 5.2.1
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Tailwind CSS
- **Database**: SQLite (default)
- **Icons**: Font Awesome

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv env
   # On Windows
   .\env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```bash
   python manage.py migrate
   ```

5. Run the development server
   ```bash
   python manage.py runserver
   ```

6. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

- **Dashboard**: View all tasks with statistics
- **Add Task**: Create new tasks with title, description, status, and deadline
- **Filter Tasks**: Use the filter buttons to view tasks by status
- **Search**: Find tasks by title or description
- **Complete Tasks**: Check the checkbox to mark tasks as complete
- **Edit/Delete**: Use the action buttons in the task list
- **Reschedule**: For missed tasks, use the reschedule option

## Project Structure

- `tasks/` - Main Django app containing models, views, and business logic
- `templates/` - HTML templates using Django's template system
- `static/` - Static assets (CSS, JS, images)
- `task_manager/` - Django project settings

## License

MIT