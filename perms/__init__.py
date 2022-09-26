import permissions


def handler(content: str, options: dict) -> str:
    if options["action"] == "create":
        permissions.permissions_db.put(
            {
                "Name": options["name"],
                "Phone": options["phone"],
                "Permissions": content
            }
        )
        
        return f"Added permissions for {options['name']}. {content}."

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
