
def tool_schema_handler(schema):
    """Recursively clean the schema by removing 'title' fields
    and sanitizing file-like parameters to avoid Gemini file inference.

    Args:
        schema (dict): The schema dictionary.

    Returns:
        dict: Cleaned schema without 'title' fields and unnecessary 'format' keys.
    """

    if isinstance(schema, dict):
        # Remove 'title' if present
        schema.pop("title", None)

        # Remove or sanitize suspicious 'format' fields
        if schema.get("type") == "string" and schema.get("format") in ["uri", "binary"]:
            schema.pop("format")

        # Rename keys like 'file', 'document', etc., if needed
        # (optional: rename keys in 'properties' dict if desired)

        # Recursively clean nested 'properties'
        if "properties" in schema and isinstance(schema["properties"], dict):
            cleaned_properties = {}
            for key, value in schema["properties"].items():
                cleaned_properties[key] = tool_schema_handler(value)
            schema["properties"] = cleaned_properties

        # Also clean items in case of array-type schemas
        if "items" in schema:
            schema["items"] = tool_schema_handler(schema["items"])

    elif isinstance(schema, list):
        return [tool_schema_handler(item) for item in schema]

    return schema


example_schema = {
    "title": "Example Schema",
    "properties": {
        "field1": {
            "title": "Field 1 Title",
            "type": "string"
        },
        "field2": {
            "properties": {
                "nested_field": {
                    "title": "Nested Field Title",
                    "type": "integer"
                }
            }
        }
    }
}


if __name__ == "__main__":
    print(tool_schema_handler(example_schema))
