## 2. Key Personas

### Sally Student

Students are the main users of the CSXL. They might use it frequently to work and study or go
to office hours if they are held there. In this case, they are familiarized with the CSXL website and possibly have communication with the ambassadors.

Students can also not frequently or never use the lab. Then they are probably unfamiliar to the website and have no personal communciation with ambassadors.

In any case, the student should have a smooth experience viewing and reserving equipments through the website and going to the lab to pick them up or use them. This means the student needs to be able to choose the equipment through the website and see its availability. Then, they should be guided through the process of picking it up and be informed about when the session ends (it would help if they are also notified via message or email at that time).

The student should also be able to sign agreements required to reserve an equipment through the website, in case of breaking or losing pieces of equipments.

### Amy Ambassador

Ambassadors are the main personas responsible for organizing the lab. They will be the people adding and removing items from the library, keeping track of returns, and compeleting other essential parts of the equipment reservation process. The majority of their tasks will be completed through the CSXL website, although they can probably rely on communicating with students personally during the reservation.

Also, ambassadors should be able to confirm information about reservations, notify any unpredicted changes to students that made reservations, and edit reservations.

The main task of an ambassador will be tracking items through unique identifiers (given they might be of the same model/type) and checking them back in upon return. They should also be able to describe any damage or abnormalities with the material when they check it in.

## 3. User Stories

### Story A

As any persona, I want to be able to access the equipments reservation page through the main menu.

Subtasks:

1. Students should be taken to the URL path of `"/equipment-reservations/student"`
2. Ambassadors should be taken to the URL path of `"/equipment-reservations/admin"`

### Story B

As Sally Student, I will be prompted with a proposal to sign the liability agreement at my first access on the equipment reservation page or if the agreement chganges, so that I don't have to sign it every time I want to lend an equipment.

Subtasks:

1. Make a database column for the Student model called `agreement_status` and set it to false.
2. Show the liability agreement when the student enters the URL path `"/equipment-reservations/student"` if the current version is not yet signed.
3. Save the status to a database after signed.

### Story C

As Amy Ambassador, I want to have an add button that allows me to add a new item to the library of available equipment to be reserved through a form, so that they appear to students through the website.

Subtasks:

1. The ambassador should be able to submit a piture of the item, write a title, and a description.
2. That information should be saved to the database.

### Story D

As Sally Student, I want to view the library of equipments and if they are currently available, so that I can pick what I want to reserve.

Subtasks:

1. Show cards of equipments with title, picture, and availability.
2. Order each equipment first by type, then by availability. This means available items will be shown first.

### Story E

### Story \_\_

As Amy Ambassador, I should be able to check the procuts in through its unique ID and log details about the equipment that was returned or any abnormalities noted by the student, so that I can track returns.

- Logging details will serve as an incentive to review the equipment with more attention, besides tracking when products were damaged.

Subtasks:

1. Entering unique ID number or scanning a QR code to find the item in the database.

### Opportunities

1. Filtering items by availability, type, etc.
2. Saving favorite equipments or most used.
