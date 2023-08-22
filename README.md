# Vcc-Vscode-Debugpy
Do you want to debug you Cheshare Cat plugin with vscode?

Install this plugin, rebuild the container, restart the containers and try to ask the Cat to help you on debugging you plugin...

![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/aa65ceff-db53-4eb8-a8a2-f940d80b27a9)



You can connect with vscode using the configuration (if you are running vscode and docker on the same machine...):
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach to Cat",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/core",
                    "remoteRoot": "/app"
                }
            ],
            "justMyCode": true
        }
    ]
}
```
