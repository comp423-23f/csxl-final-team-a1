# The Equipment Reservation Station

> A1 Team Members: Benjamin Eldridge, Jacob Fessler, Vitor Inserra, and Andrew Lockard

## 1. Overview

The equipment reservation station is a resource for students to have access to a
system for reserving and borrowing various tech equipment such as AR/VR
Headsets, iPads, iPhones, Androids, Keyboards, and Arduinos. This will enable
learning and development opportunities for students who might not have had
access to more expensive items such as AR/VR headsets, or have never had the
chance to utilize a different platform like iPad, iPhone, Android. An online
system running through the CSXL will make borrowing equipment convenient with
multi-day reservations and the ability to view equipment availability.

## 2. Key Personas

### Sally Student

Students are the main users of the CSXL. They might use it frequently to work and study or go
to office hours if they are held there. In this case, they are familiarized with the CSXL website and possibly have personal communication with the ambassadors.

Students can also not frequently or never use the lab. Then they are probably unfamiliar to the website and have no personal communciation with ambassadors. Therefore, it is important to have the feature be accessible through the main menu and possibly have a description of it on the landing page of the CSXL (for non-logged users).

In any case, the student should have a smooth experience viewing and reserving equipments through the website and going to the lab to pick them up or use them. This means the student needs to be able to choose the equipment through the website and see its availability. Then, they should be guided through the process of picking it up and be informed about when the session ends (it would help if they are also notified via message or email at that time).

The student should also be able to sign agreements required to reserve an equipment through the website, in case of breaking or losing pieces of equipments.

### Amy Ambassador

Ambassadors are the main personas responsible for organizing the lab. They will be the keeping track of returns, communicating with students and compeleting other essential parts of the equipment reservation process. The majority of their tasks will be completed through the CSXL website, although they can probably rely on communicating with students personally during the reservation.

Also, ambassadors should be able to confirm information about reservations, notify any unpredicted changes to students that made reservations, and edit reservations.

The main tasks of an ambassador will be tracking items through unique identifiers (given they might be of the same model/type) and checking them back in upon return. They should also be able to describe any damage or abnormalities with the material when they check it in.

### Rhonda Root

Roots will be responsible for the one-time operations such as adding and removing items from the library. They should be able to submit a new item with all its details so be shown in the library.

## 3. User Stories

### Story A

As any persona, I want to be able to access the equipments reservation page through the main menu.

Subtasks:

1. Students should be taken to the URL path of `/equipment-reservations/student`. Users who are not logged in should not be allowed on this path.
2. Ambassadors should be taken to the URL path of `/equipment-reservations/ambassador`. Students and users who are not logged in should not be allowed in this URL path.

### Story B

As Sally Student, I will be prompted with a proposal to sign the liability agreement at my first access on the equipment reservation page or if the agreement changes, so that I don't have to sign it every time I want to lend an item.

Subtasks:

1. Add a database column on the Student model called `agreement_status` and set it to false.
2. Show the liability agreement when the student enters the URL path `/equipment-reservations/student` if the current version is not yet signed.
3. Save the status to a database after signed.

### Story C

As Rhonda Root, I want to have an add button that allows me to add a new item to the library of available equipment to be reserved through a form, so that they appear to students through the website. I also want an edit button that allows changing information about the item and a delete button that removes the item from the database.

Subtasks:

1. There should be a field to add a picture of the item, a title, and a description. (Also possibly a field for max reservation span).
2. Equipment information should be saved to the database.

### Story D

As any Persona - that is, on both URL paths `/ambassador` and `/student` - I want to view the library of equipments and their availability status (available at that moment or not), so that I can pick what I want to reserve.

Subtasks:

1. Show cards of equipments with title, picture, and availability.
2. Order each equipment first by type, then by availability. This means item available at that moment will be shown first.

### Story E

As any Persona, I want to click on an item and be taken to the items page on path `/equipment-reservations/<user type>/<item name>`, so that I can expand the item details and see information about reserving the item.

Subtasks:

1. Showing a reservation chart (possibly an hourly calendar of the week). This will be developed in next steps, so for now just have this item exist here and call a `show_reservation_calendar` widget.

### Story F

As Sally Student, I should be able to reserve equipment using the calendar item, so that I can easily set the preffered times or dates.

Subtasks:

1. Set a notification for when the user's reserved session ends.
2. Implement the `show_reservation_calendar` widget.

### Story G

As Amy Ambassador, I should be able to check the equipment in through its unique ID and log details or any abnormalities noted by the student about the equipment on return.

- Logging details will serve as an incentive to review the equipment with more attention, besides tracking when products were damaged.

Subtasks:

1. Entering unique ID number or scanning a QR code to find the item in the database.
2. Save the check-in to a database.

### Story H

As Amy Ambassador, I should be able to change that equipment's status to unavailable or change it back to available.

Subtasks:

1. Uniquely unavailable or available items are marked accordingly in the database. (To make the frontend work easier, mark the item as unavailable for a long period of time [1 semester or year]).

### Opportunities for Extra Stories

1. Filtering items by availability, type, etc.
2. Saving favorite equipments or most used.
3. Instead of showing every single unique item and its availability, show just the type of equipment and a single calendar for all their combined availability.
4. Club leaders can checkout multiple materials.

## 5. Technical Requirements Implementation Opportunities and Planning

### 1. Direct Dependencies from Original Code Base

a. Authentication and permissions˝this will be essential for access to the each URL path.

b. User model: will be used for all reservation and agreement functionalities.

c. Ambassador model: will be used for all CSXL-side functionalities, except permanently adding or removing equipments.

d. Root model: will be used for permanently adding and removing equipments.

e. Menu component: should continue to appear or collapse into hamburger (in case of smaller screens).

f. Search bar: may be available for search when there are multiple items to choose from.

g. `XL` icons: should continue to be used in tab title.

### 2. Planned Page Components and Widgets

a. Library Component: includes a list of all the types of equipments available, by exact model.

b. Ambassador's View Component: includes a list of all unique items and at least filter or ordering by type. Should allow displaying or removing an item from display.

c. Root's Management Component: includes a list of all unique items and allow adding, editing and deleting.

c. Equipment Component: includes all details about an equipment type.

d. Agreement Component: shows the liability agreement and allow signing.

e. Calendar Widget: shows all the available and unavailable dates for each item, as well as how many items are available.

f. Check-in Component: allows checking items back in.

### 3. Additional and Editted Models

a. User Model:

- `agreement_status` column should be added to track if the student has signed it or not.

b. Equipment Type Model: additional model that contains equipment specifications.

- `title`
- `picture`
- `description`
- `max_reservation_time` should be used to make limit the time of a reservation appointment.

c. Unique Item Model: additional model contains unique items and necessary information.

- `id` column should be a unique identification number.
- `equipment_type` relational mapping that connects the unique item to the Equipment Type Model.
- `reserved_dates` hash map relating student reservation time.
- `return_date` hash map relating students to return statuses.
- `return_description` hash map relating students to return descriptions.
