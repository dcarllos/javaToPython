import pytest
from azuredevops.language.azure_language import detect_repository_language

@pytest.mark.parametrize("files, expected_language", [
    ([{"path": "/src/main.py"}], "python"),
    ([{"path": "/lib/util.js"}], "javascript"),
    ([{"path": "/types/index.ts"}], "typescript"),
    ([{"path": "/app/App.java"}], "java"),
    ([{"path": "/pkg/server.go"}], "go"),
    ([{"path": "/web/index.php"}], "php"),
    ([{"path": "/script/run.rb"}], "ruby"),
    ([{"path": "/src/Program.cs"}], "csharp"),
    ([{"path": "/ios/App.swift"}], "swift"),
    ([{"path": "/src/Project.csproj"}], "C#"),
    ([{"path": "/project/package.json"}], "JavaScript"),
    ([{"path": "/README.md"}], "Unknown"),
    ([], "Unknown"),
])
def test_detect_repository_language(files, expected_language):
    result = detect_repository_language(files)
    assert result == expected_language
