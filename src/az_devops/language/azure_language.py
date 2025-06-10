def detect_repository_language(files):
    for item in files:
        path = item.get("path", "").lower()
        if path.endswith(".py"):
            return "python"
        elif path.endswith(".js"):
            return "javascript"
        elif path.endswith(".ts"):
            return "typescript"
        elif path.endswith(".java"):
            return "java"
        elif path.endswith(".go"):
            return "go"
        elif path.endswith(".php"):
            return "php"
        elif path.endswith(".rb"):
            return "ruby"
        elif path.endswith(".cs"):
            return "csharp"
        elif path.endswith(".swift"):
            return "swift"
        if path.endswith(".csproj"):
            return "C#"
        elif path.endswith("package.json"):
            return "JavaScript"
    return "Unknown"