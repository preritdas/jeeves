import utils
import permissions


APP_HELP = (
    "Add permissions for a new user or update those of a current one. "
    "Message content should be the new permissions."
)
APP_OPTIONS = {
    "action": "REQUIRED, either 'create' or 'update'",
    "phone": "REQUIRED, phone number of new or existing user",
    "name": "MAYBE, only needed if adding a new user."
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Update permissions in the database."""
    assert (content := content.lower()), "You must provide the user's permissions " \
        "as content."

    if options["action"] == "create":
        # Check for existence
        db_res = permissions.permissions_db.fetch(
            query = {"Name": options["name"].title()}
        )
        if len(db_res.items) > 0:
            return f"{options['name'].title()} already exists, with " \
                f"permissions {db_res[0]['Permissions']}."

        db_res = permissions.permissions_db.fetch(
            query = {"Phone": options['phone']}
        )
        if len(db_res.items) > 0:
            return f"{options['phone'].title()} already exists, with " \
                f"permissions {db_res[0]['Permissions']}."

        permissions.permissions_db.put(
            {
                "Name": options["name"].title(),
                "Phone": options["phone"],
                "Permissions": content
            }
        )
        
        return f"Added permissions for {options['name'].title()}. {content}."

    if options["action"] == "update":
        name_query = False
        if options.get("name", None):  # if name is provided
            db_res = permissions.permissions_db.fetch(
                {"Name": options["name"]}
            )
            if len(db_res.items) == 1:
                name_query = True

        if not name_query:
            db_res = permissions.permissions_db.fetch(
                {"Phone": options["phone"]}
            ).items

        if len(db_res) > 1:
            return f"Many users were found with the phone number {options['phone']}. " \
                "Correct this."

        if len(db_res) == 0:
            return "No users were found with those options."

        key = db_res[0]["key"]
        name = db_res[0]["Name"]
        permissions.permissions_db.update(
            {
                "Permissions": content 
            },
            key = key
        )

        return f"Successfully changed {name}'s permissions to {content}."
