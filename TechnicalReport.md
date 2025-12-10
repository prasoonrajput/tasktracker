Technical Report – Task & Productivity Tracker (Django Backend)

(Without Django REST Framework)

1. Understanding of the Problem

The assignment requires building a backend system for a Task & Productivity Tracker using Django and SQLite.
The backend must expose REST-like API endpoints that allow:

Creating tasks

Listing all tasks

Retrieving a task by ID

Updating tasks (PUT & PATCH)

Deleting tasks

Filtering and sorting tasks

Generating a status-based task summary

Since Django REST Framework is optional, this implementation uses pure Django, meaning all request parsing, validation, and JSON responses are implemented manually.

This demonstrates a deeper understanding of backend fundamentals including request handling, HTTP method routing, validation, and serialization.

2. Database & Model Design

A single model, Task, represents an individual task entry.

Fields
Field	Type	Description
title	CharField	Required short title
description	TextField	Optional detailed text
priority	CharField (choices)	LOW, MEDIUM, HIGH
status	CharField (choices)	PENDING, IN_PROGRESS, COMPLETED
created_at	DateTimeField	Auto timestamp on creation
Design Decisions

Choice fields enforce consistent values for priority and status.

created_at automatically records the creation timestamp.

A custom method to_dict() converts model objects into JSON-compatible dictionaries, replacing the serializer function normally provided by DRF.

The model remains extendable, allowing future additions such as deadlines, user ownership, or task categories.

3. API Architecture & Flow

Since DRF is not used, the API uses Django function-based views with manual logic for parsing, validation, and responses.

Implemented Endpoints
1. /api/tasks/

GET → List all tasks

Supports filtering: ?status=PENDING, ?priority=HIGH

Supports sorting: ?ordering=created_at or -created_at

POST → Create a new task (JSON body)

2. /api/tasks/<id>/

GET → Retrieve task by ID

PUT → Full update (requires all fields)

PATCH → Partial update

DELETE → Remove task

3. /api/tasks/summary/

GET → Returns total number of tasks grouped by status

API Flow
For GET Requests

Retrieve data from the database.

Apply filters (if provided).

Apply sorting (if provided).

Convert objects to Python dictionaries using to_dict().

Return a JSON array.

For POST/PUT/PATCH Requests

Parse raw JSON from the request body.

Validate title, status, and priority.

Perform database operations (create or update).

Convert the resulting task to a dictionary.

Return JSON response with appropriate status codes.

For DELETE Requests

Locate task using primary key (pk).

Delete the object.

Return a confirmation message.

4. Tools, Libraries, and Versions
Tool	Version	Usage
Python	3.x	Language runtime
Django	5.0.4	Backend framework
SQLite	default	Lightweight database
json module	Built-in	Request parsing
JsonResponse	Django	JSON output

No additional packages were used.

5. Error Handling Strategy

Django REST Framework usually manages errors automatically.
Here, since DRF is not used, error handling is implemented manually.

Implemented Error Responses
Invalid JSON
{"detail": "Invalid JSON."}

Missing required fields
{"detail": "Title is required and cannot be empty."}

Invalid priority or status
{"detail": "Invalid priority. Allowed: ['LOW','MEDIUM','HIGH']"}

Task not found
{"detail": "Task not found."}

Unsupported HTTP method

Handled via:

HttpResponseNotAllowed(['GET', 'POST'])

6. Filtering, Sorting, and Summary Logic
Filtering

Tasks can be filtered using query parameters such as:

/api/tasks/?status=PENDING
/api/tasks/?priority=HIGH


Applied through:

qs = qs.filter(status=status_param)

Sorting

Sorting uses:

?ordering=created_at
?ordering=-created_at


Handled manually using:

qs.order_by(ordering)

Summary

The summary endpoint uses Django aggregation:

Task.objects.values('status').annotate(count=Count('id'))


All statuses are included, even if their count is zero.

7. Challenges and Solutions
1. Manual JSON Parsing

Since Django views do not parse JSON automatically, request bodies needed manual parsing using:

json.loads(request.body.decode('utf-8'))

2. Validation

Required fields and choice fields needed custom validation logic.

3. PUT vs PATCH

PUT requires full object replacement; PATCH only updates provided fields.
Both behaviors were implemented manually.

4. Ensuring consistent JSON responses

Every response had to use JsonResponse and follow a consistent schema.

5. Handling unsupported HTTP methods

Added HttpResponseNotAllowed to enforce REST principles.

8. Possible Future Improvements
1. Introduce Django REST Framework

This would simplify:

serialization

validation

pagination

automatic error handling

authentication

2. Add Authentication

Allow tasks to be user-specific.

3. Add Search & Pagination

Improve usability for large task lists.

4. Add Due Dates & Reminders

Better productivity features.

5. Add Logging & Activity History

Helps track user behavior and debugging.

6. Implement Background Jobs (Celery)

For scheduled emails, task reminders, cleanup jobs.

9. Conclusion

This backend system satisfies all assignment requirements:

CRUD operations

Filters, sorting, and summary endpoint

Manual JSON handling

Custom validation

Clean API responses

Proper use of Django ORM and views

The design is clean, extendable, and demonstrates clear understanding of REST principles and Django internals without relying on Django REST Framework’s abstractions.