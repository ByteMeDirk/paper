# RBAC (Roll-Based Access Control)

## Standard Out-Of The Box Django Roles

Django comes with a few standard roles that are used to manage access to the admin interface. These roles are:

- **Superuser**: A superuser has full access to all objects and actions.
- **Staff**: A staff user has access to the admin interface and can perform actions on objects.
- **User**: A user is a regular user that can log in and perform actions on objects.

## Papers Defined Roles

- **Admin**:  (Not the Superuser) This role will be responsible for managing the overall platform, including user
  management, content moderation, and algorithmic content matching. The admin will have full control over the platform
  and will be able to perform any action, including creating, editing, and deleting content, managing user permissions,
  and configuring the platform's settings.
- **Moderator**: (Like Staff)This role will be responsible for reviewing and moderating user-posted content. Moderators
  will have the ability to flag content for removal, edit content, and manage user permissions. They will also be
  responsible for ensuring that the platform's content guidelines are being followed.
- **Creator**: This role will be responsible for creating and posting content on the platform. Creators will have the
  ability to upload and manage their own content, including adding tags and descriptions. They will also be able to
  interact with other users through comments and messaging.
- **Viewer**: (Registered & Unregistered) This role will be responsible for viewing and interacting with content on the
  platform. Viewers will have the ability to browse and search for content, view comments and discussions, and engage
  with other users through messaging and commenting.