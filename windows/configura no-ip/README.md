| Step 1: Registration on No-IP                                                                           |
|---------------------------------------------------------------------------------------------------------|
| 1. Go to the No-IP website at [No-IP](https://www.noip.com/).                                           |
| 2. Create an account or log in if you already have one.                                                   |
| 3. After logging in, navigate to the "Dynamic DNS" section and click on "Add a Host".                     |
| 4. Choose a hostname (what will be used to access your computer remotely) and select the desired domain   |
|    (e.g., no-ip.org).                                                                                    |
| 5. Select your hostname renewal time (interval at which your IP will be automatically updated).            |
| 6. Click "Add Host" to save the settings.                                                                 |

| Step 2: Download and Install No-IP Software                                                              |
|---------------------------------------------------------------------------------------------------------|
| 1. Download the No-IP DUC (Dynamic Update Client) client from [No-IP Download](https://www.noip.com/download).|
| 2. Install the software by following the on-screen instructions.                                           |
| 3. During installation, log in with your No-IP account.                                                    |
| 4. Choose the hosts you want to associate with your dynamic IP.                                             |

| Step 3: Router Configuration (Port Forwarding)                                                            |
|---------------------------------------------------------------------------------------------------------|
| To access your computer remotely, configure port forwarding on your router. The exact details vary by     |
| router model, but generally involve:                                                                      |
| 1. Access your router's settings through a browser by entering the router's IP address (see your router's |
|    manual for information on the default IP address).                                                      |
| 2. Locate the port forwarding or "Port Forwarding" section.                                                |
| 3. Add a rule to forward connections on the desired port (e.g., port 80 for HTTP access) to your         |
|    computer's local IP address.                                                                            |

| Step 4: Verification                                                                                      |
|---------------------------------------------------------------------------------------------------------|
| 1. Open the No-IP DUC software on your computer.                                                           |
| 2. The DUC will automatically detect your public IP and update the host in No-IP with that IP.             |
| 3. Access your computer remotely using the hostname you configured in No-IP.                               |
