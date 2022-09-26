import permissions


def handler(content: str, options: dict[str, str]) -> str:
    """Update permissions in the database."""
    assert (content := content.lower()), "You must provide some content here."

    if options.get("help", None):
        return "Add permissions for a new user, or update those of a current one.\n\n" \
            "Message content should be the new permissions.\n\n" \
            "Available options:\n" \
            "- action: REQUIRED, either 'create' or 'update'" \
            "- phone: REQUIRED, phone number of new or existing user" \
            "- name: MAYBE, only needed if adding a new user."

    if options["action"] == "create":
        permissions.permissions_db.put(
            {
                "Name": options["name"].title(),
                "Phone": options["phone"],
                "Permissions": content
            }
        )
        
        return f"Added permissions for {options['name'].title()}. {content}."

    if options["action"] == "update":
        db_res = permissions.permissions_db.fetch(
            {"Phone": options["phone"]}
        ).items

        if len(db_res) > 1:
            return f"Many users were found with the phone number {options['phone']}. " \
                "Correct this."

        key = db_res[0]["key"]
        name = db_res[0]["Name"]
        permissions.permissions_db.update(
            {
                "Permissions": content 
            },
            key = key
        )

        return f"Successfully changed {name}'s permissions to {content}."
