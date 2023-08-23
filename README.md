# Debug Server for VSCode

## Debug your Cheshire Cat plugin?
Would you like to debug your Cheshire Cat plugin running in a Docker container with VSCode? This plugin can assist you!

## How to use
Install this plugin, rebuild the container, restart and try to ask the Cat to help you on debugging your plugin...

![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/aa65ceff-db53-4eb8-a8a2-f940d80b27a9)



You can connect with vscode using this configuration (if you are running vscode and docker on the same machine...):
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
Using this plugin to debug this plugin ;-)
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/73b2dfe8-5fdb-4997-b41d-5c3499b99e39)

## How to debug the bootstrap process
If you need to debug something during the Cat boostrap process set the setting `Listen on bootstrap` to `YES` then stop and start the Cat, the bootstrap process will be blocked waiting for a debug connection:
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/ec590851-7091-4fd6-8264-a983a19136bf)
