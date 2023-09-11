from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from note_seq.protobuf import music_pb2
from note_seq import note_sequence_to_midi_file
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2

app = Flask(__name__)
CORS(app)  # enable CORS

# load basic rnn model
bundle = sequence_generator_bundle.read_bundle_file('./basic_rnn.mag')
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()

# @app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/create_midi', methods=['POST'])
def create_midi():
    note_duration = 0.5
    pressed_keys = request.get_json().get('pressedKeys', [])
    note_list = [int(note.lstrip('_'))for note in pressed_keys]
    note_list.reverse()

    input_sequence = music_pb2.NoteSequence()
    for index, note_pitch in enumerate(note_list):
        note = input_sequence.notes.add()
        note.pitch = note_pitch+24
        note.start_time = note_duration * index
        note.end_time = note_duration * (index + 1)
        note.velocity = 80  # this sets the volume of the note
    input_sequence.total_time = note_duration * len(note_list)     # set the total time of the sequence
    input_sequence.tempos.add(qpm=60)

    # generate more notes based on input_sequence(to do)
    num_steps = 128  # change this for shorter or longer sequences
    temperature = 1.0  # the higher the temperature the more random the sequence.

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in input_sequence.notes)
                     if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
        start_time=last_end_time + seconds_per_step,
        end_time=total_seconds)

    # Ask the model to continue the sequence.
    sequence = melody_rnn.generate(input_sequence, generator_options)

    # covert the sequence to a MIDI file
    note_sequence_to_midi_file(sequence, './midi/generated_music.mid')

    # Process the pressedKeys and create a MIDI file...
    # Let's print them for now
    # print(input_sequence)
    return jsonify({'message': 'MIDI file successfully created!'})

if __name__ == '__main__':
    app.run(debug=True)