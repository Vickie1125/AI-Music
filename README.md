# AI-music

This project is an extension of the 3D Piano Player demo originally developed using three.js and MIDI.js. The primary enhancement introduced in this version allows users to input a piano note sequence, after which the system predicts the subsequent notes to generate and play new music.

## Features

1. Visulize piano play in 3D using 'three.js'.

2. Allow the user to input a piano sequence.

3. Predict and generate subsequent notes with Megante.

4. Web-based interface served using Flask.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install flask
pip install flask_cors
pip install note_seq
pip install magenta
```

## Usage

```bash
git clone https://github.com/Vickie1125/AI-Music.git
cd path_to_your_project
python flask_server.py
open index.html
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
