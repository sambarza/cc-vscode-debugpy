# Debug Server for VSCode

## Debug your Cheshire Cat plugin?
Would you like to debug your Cheshire Cat plugin running in a Docker container with VSCode? This plugin can assist you!

## How to use
1. Install this plugin by cloning this repo in the folder `core/cat/plugins/`
2. Rebuild the container with `docker-compose build --no-cache`
3. Expose the port `5678` by adding it to the `docker-compose.yml`:
```yml
    ports:
      - ${CORE_PORT:-1865}:80
      - 5678:5678           < --- add this line
```
4. Restart with `docker-compose up`
5. Try to ask the Cat to help you on debugging your plugin...

![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/aa65ceff-db53-4eb8-a8a2-f940d80b27a9)

6. You can connect with vscode using this configuration (if you are running vscode and docker on the same machine...):
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
If you need to debug something during the Cat boostrap process, activate the `Listen on bootstrap` setting, then stop and start the Cat, the bootstrap process will be blocked waiting for a debug connection:
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/c6dc1787-9375-46f9-bf87-2eb122a96df5)

When starting up, there is a message in the console log that indicates the waiting connection:
![image](https://github.com/sambarza/cc-vscode-debugpy/assets/3630051/9c777be7-f114-4947-911d-26ac55e38dec)

