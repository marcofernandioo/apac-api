@echo off
:start
echo Watching requirements.txt...
timeout /t 1 /nobreak > nul
for %%I in (requirements.txt) do (
    if %%~zI gtr 0 (
        echo Change detected in requirements.txt. Rebuilding Docker container...
        docker build -t myapp .
        docker stop $(docker ps -a -q --filter ancestor=myapp --format="{{.ID}}")
        docker run -p 8000:8000 myapp
    )
)
goto start
