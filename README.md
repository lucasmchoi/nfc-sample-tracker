# nfc-sample-tracker

NFC sample tracking using NTAG 21X NFC tags

![pylint](https://img.shields.io/badge/PyLint-9.36-yellow?logo=python&logoColor=white)


# Architecture and processes
## System architecture

![System architecture](readme/architecture.svg)

[Made using Mermaid](https://mermaid.js.org/)

[Mermaid GitHub](https://github.com/mermaid-js/mermaid)



## Database ER model

![Database ER](readme/dbdiagram.svg)

[Made using Mongo Modeler](https://www.mongomodeler.com/)

[Mongo Modeler GitHub](https://github.com/Lemoncode/mongo-modeler)



## Process diagrams
### User processes
#### New user
![User process diagram new user](readme/user_process_diagram_newuser.svg)
[Detailed process diagram new user](readme/process_diagram_newuser.svg)

#### New plate
![User process diagram new plate](readme/user_process_diagram_newplate.svg)
[Detailed process diagram new plate](readme/process_diagram_newplate.svg)

#### New sample
![User process diagram new sample](readme/user_process_diagram_newsample.svg)
[Detailed process diagram new sample](readme/process_diagram_newsample.svg)

#### Send sample
![User process diagram send sample](readme/user_process_diagram_sendsample.svg)
[Detailed process diagram send sample](readme/process_diagram_sendsample.svg)

#### New sample location
![User process diagram new sample location](readme/user_process_diagram_newsamplelocation.svg)
[Detailed process diagram new sample location](readme/process_diagram_newsamplelocation.svg)

#### Sample plate transfer
![User process diagram sample plate transfer](readme/user_process_diagram_sampleplatetransfer.svg)
[Detailed process diagram sample plate transfer](readme/process_diagram_sampleplatetransfer.svg)



### Admin processes
#### Sample damaged or lost
![User process diagram sample damaged or lost](readme/user_process_diagram_sampledamagedlost.svg)
[Detailed process diagram sample damaged or lost](readme/process_diagram_sampledamagedlost.svg)

#### Sample owner transfer
![User rocess diagram sample owner transfer](readme/user_process_diagram_ownertransfer.svg)
[Detailed process diagram sample owner transfer](readme/process_diagram_ownertransfer.svg)



[Made using Mermaid](https://mermaid.js.org/)

[Mermaid GitHub](https://github.com/mermaid-js/mermaid)



# Additional information
## Datasheets

- https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf (https://web.archive.org/web/20240404075504/https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf)
- https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf (https://web.archive.org/web/20240404041534/https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf)

# License

Copyright © 2024 [Luca Choi](https://www.github.com/lucasmchoi)
This work is licensed under [AGPL v3](/LICENSE)

# Third-Party Requirements

- [Python](https://www.python.org) (PSF License)
- [Pip](https://pypi.org/)

- [picamera2](https://github.com/RaspberryPi/picamera2) ([BSD 2-Clause License](LICENSES/picamera2-LICENSE.txt))
- [rpi-lgpio](https://github.com/waveform80/rpi-lgpio) ([MIT License](LICENSES/rpi-lgpio-LICENSE.txt))
- [pi-rc522](https://github.com/kevinvalk/pi-rc522) ([MIT License](LICENSES/pi-rc522-LICENSE.txt))
- [ndeflib](https://github.com/nfcpy/ndeflib) ([ISC License](LICENSES/ndeflib-LICENSE.txt))
- [pillow](https://github.com/python-pillow/Pillow) ([HPND License](LICENSES/pillow-LICENSE.txt))
- [pymongo](https://github.com/mongodb/mongo-python-driver) ([Apache License 2.0](LICENSES/pymongo-LICENSE.txt))
- [fastapi](https://github.com/tiangolo/fastapi) ([MIT License](LICENSES/fastapi-LICENSE.txt))
- [motor](https://github.com/mongodb/motor) ([Apache License 2.0](LICENSES/motor-LICENSE.txt))
- [pydantic](https://github.com/pydantic/pydantic) ([MIT License](LICENSES/pydantic-LICENSE.txt))
- [email-validator](https://github.com/JoshData/python-email-validator) ([Unlicense](LICENSES/email-validator-LICENSE.txt))
- [typing-extensions](https://github.com/python/typing_extensions) ([PSF License](LICENSES/typing-extensions-LICENSE.txt))
- [pandas](https://github.com/pandas-dev/pandas) ([BSD 3-Clause License](LICENSES/pandas-LICENSE.txt))
- [dash](https://github.com/plotly/dash) ([MIT License](LICENSES/dash-LICENSE.txt))
- [dash-bootstrap-components](https://github.com/facultyai/dash-bootstrap-components/) ([Apache License 2.0](LICENSES/dash-bootstrap-components-LICENSE.txt))

- [pylint-github-action](https://github.com/Silleellie/pylint-github-action) ([MIT License](LICENSES/pylint-github-action-LICENSE.txt))
- [pylint](https://github.com/pylint-dev/pylint) ([GPL v2](LICENSES/pylint-LICENSE.txt))
