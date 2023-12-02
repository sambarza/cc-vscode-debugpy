# Debug Server for VSCode

## Debug your Cheshire Cat plugin?
Would you like to debug your Cheshire Cat plugin running in a Docker container with VSCode? This plugin can assist you!

## How to use
1. Install the plugin `Debug Server for VSCode` from the Plugins registry ([Tab Plugins](http://localhost:1865/admin/plugins))
1. Expose the port `5678` by adding the following line to the `docker-compose.yml`:
```yml
    ports:
      - ${CORE_PORT:-1865}:80
      - 5678:5678           < --- add this line
```
3. Restart the Cat
1. Ask the Cat to help you on debugging, the Cat is now waiting for connections from VSCode:

![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/8c8c12e9-3cff-477a-860d-2b0fc943163e)

6. Open the root Cat folder with VSCode, the root folder is the folder that contains the `core` folder
7. Add the following configuration inside the `launch.json` VSCode file:
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
7. Start the debug in VSCode using the new `Python: Remote Attach to Cat` configuration

## What I can do?
All the VSCode debugging feature are available:
- Breakpoints
- Watching Variables
- Call Stack
- Debug Console
- Conditional Breakpoints
- Logpoints
- ...

## Screenshot
Using this plugin to debug this plugin ;-)
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/73b2dfe8-5fdb-4997-b41d-5c3499b99e39)

## How to always listen for debug
In the plugin settings, there is an option to always start listening for debugging without the need to ask the Cat for debugging each time:
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/b4fe1c0e-7b9b-401b-9ab2-61cf6b5c2ce9)

## How to debug the bootstrap process
If you need to debug something during the Cat boostrap process, activate the `Listen on bootstrap` setting, then stop and start the Cat, the bootstrap process will be blocked waiting for a debug connection:
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/d936f939-8393-4fd7-82da-077086d0c04c)

When starting up, there is a message in the console log that indicates the waiting connection:
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/9c777be7-f114-4947-911d-26ac55e38dec)

