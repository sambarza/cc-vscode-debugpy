# Debug Server for VSCode

## Debug your Cheshire Cat plugin?
Would you like to debug your Cheshire Cat plugin running in a Docker container with VSCode? This plugin can assist you!

## How to use
1. Install the plugin `Debug Server for VSCode` from the Plugins registry ([Tab Plugins](http://localhost:1865/admin/plugins))
2. If using a Cat version earlier than 1.7, expose port 5678 by adding the following line to the `compose.yml` file. Newer Cat releases already expose this port (ensure it's closed in production environments):
```yml
    ports:
      - ${CORE_PORT:-1865}:80
      - 5678:5678           < --- add this line
```
3. If you run the Cat using `docker run`, expose the port `5678` by adding `-p 5678:5678` to the `docker run` command:
   
   `docker run --rm -it -v ./data:/app/cat/data -v ./plugins:/app/cat/plugins -p 1865:80 -p 5678:5678 ghcr.io/cheshire-cat-ai/core:latest`
4. Restart the Cat
5. Ask the Cat to help you on debugging, the Cat is now waiting for connections from VSCode:

![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/8c8c12e9-3cff-477a-860d-2b0fc943163e)

6. In the VSCode debug configuration file `launch.json` put this (see [here](#other-launchjson-configuration-for-special-cases) for other configurations):
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
                    "localRoot": "${workspaceFolder}/plugins",
                    "remoteRoot": "/app/cat/plugins"
                }
            ],
            "justMyCode": true
        }
    ]
}
   ```

9. Start the debug in VSCode using the new `Python: Remote Attach to Cat` configuration

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
![alt text](waiting_connection.png)

## Other ´launch.json´ configurations for special cases

### If you cloned the Cat core and ran it with `docker compose up`:
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
### If you cloned the Cat core and ran it with `docker run`:
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
                    "localRoot": "${workspaceFolder}/",
                    "remoteRoot": "/app/cat"
                }
            ],
            "justMyCode": true
        }
    ]
}
```

## Support
If you need support ping me on [Discord](https://discord.com/channels/1092359754917089350/1092360285056159814) @sambarza

