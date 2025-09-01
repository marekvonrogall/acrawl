# acrawl

This project collects solar and space weather data from NASA, SIDC, SWPC, and GFZ, including sunspot numbers, CMEs, Kp/AP indices, and solar flares.
It processes and normalizes the data, storing it in a database ready for visualization in Grafana.

The project also:
- Downloads daily solar images, 48-hour videos and CME movies.
- Generates a plot using Matplotlib, showing sunspot numbers (SSN) with highlighted M/X solar flares.
- Serves fetched media via a lightweight HTTP server.

### some media

<img width="1920" height="912" alt="CME movie page" src="https://github.com/user-attachments/assets/c1e7c603-ef28-44b8-bfdc-f643de8a5ed9" />
<img width="1509" height="777" alt="sun images page" src="https://github.com/user-attachments/assets/3d08f237-e0b8-4e93-a808-65adba597320" />
