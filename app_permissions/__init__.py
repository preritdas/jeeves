import utils
import permissions


APP_HELP = (
    "Add permissions for a new user or update those of a current one. "
    "Message content should be the new permissions."
)
APP_OPTIONS = {
    "action": "REQUIRED, either 'create', 'update', or 'view'.",
    "phone": "REQUIRED, phone number of new or existing user.",
    "name": "MAYBE, only needed if adding a new user, or for convenience."
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Update permissions in the database."""
    content = content.lower()  # all db permissions are in lower case

    if not "action" in options:
        return "You must provide an action. See app help, options: help = yes."

    if options["action"] != "view" and not content:
        return "You must provide the user's permissions as content when not using " \
            "the view action."

    if options["action"] == "view":
        if "phone" in options:
            db_res = permissions.permissions_db.fetch(
                query = {"Phone": options["phone"]}
            )

            if len(db_res.items) == 0:
                return f"{options['phone']} doesn't exist in the database."

            if len(db_res.items) > 1:
                return f"{options['phone']} exists multiple times in the database. " \
                    "This is almost definitely a mistake."

            return db_res.items[0]["Permissions"]

        db_res = permissions.permissions_db.fetch(
            query = {"Name": options["name"].title()}
        )

        if len(db_res.items) == 0:
            return f"'{options['name'].title()}' wasn't found. Try with a phone number."

        if len(db_res.items) > 1:
            return f"Multiple people were found with the name '{options['name'].title()}." \
                "Try re-querying with an absolute phone number, then check the database " \
                "to make sure this isn't a mistake."

        return db_res.items[0]["Permissions"]

    if options["action"] == "create":
        # Check for existence
        db_res = permissions.permissions_db.fetch(
            query = {"Name": options["name"].title()}
        )

        if len(db_res.items) > 0:
            return f"{options['name'].title()} already exists, with " \
                f"permissions {db_res.items[0]['Permissions']}."

        db_res = permissions.permissions_db.fetch(
            query = {"Phone": options['phone']}
        )

        if len(db_res.items) > 0:
            return f"{options['phone'].title()} already exists, with " \
                f"permissions {db_res.items[0]['Permissions']}."

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
                {"Name": options["name"].title()}
            )
            if len(db_res.items) == 1:
                name_query = True

        if not name_query:
            if not (name := options.get("phone", None)):
                return f"Nobody with name '{name}' was found, and you didn't provide " \
                    "a phone number."

            db_res = permissions.permissions_db.fetch(
                {"Phone": options["phone"]}
            )

        if len(db_res.items) > 1:
            return f"Many users were found with the phone number {options['phone']}. " \
                "Correct this."

        if len(db_res.items) == 0:
            return "No users were found with those options."

        key = db_res.items[0]["key"]
        name = db_res.items[0]["Name"]
        permissions.permissions_db.update(
            {
                "Permissions": content 
            },
            key = key
        )

        return f"Successfully changed {name}'s permissions to {content}."
