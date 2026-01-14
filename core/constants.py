CUSTOMER_ROLE_ID = 2         # Customer
FREELANCER_ROLE_ID = 4       # Freelancer
ADMIN_ROLE_ID = 1            # Admin
DELIVERY_PARTNER_ROLE_ID = 3 # Delivery Partner
STUDENT_ROLE_ID = 5          # Student
VENDOR_ROLE_ID = 6           # Vendor

# Master Status Table
STATUS_APPROVED = 1      # Approved
STATUS_PENDING = 2       # Pending
STATUS_REJECTED = 3      # Rejected
STATUS_ASSIGNED = 4      # Assigned
STATUS_NOT_ASSIGNED = 5  # Not Assigned

# Booking Status (if mapped to master_status)
BOOKING_STATUS_PENDING = STATUS_PENDING
BOOKING_STATUS_ASSIGNED = STATUS_ASSIGNED

# ==========================
# WORK STATUS (JOB EXECUTION)
# Table: master_work_status
# ==========================
WORK_STATUS_ON_THE_WAY = 1
WORK_STATUS_REACHED_LOCATION = 2
WORK_STATUS_JOB_STARTED = 3
WORK_STATUS_JOB_COMPLETED = 4