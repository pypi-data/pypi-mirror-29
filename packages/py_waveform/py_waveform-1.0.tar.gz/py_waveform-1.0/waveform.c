#include<Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <groove/groove.h>
#include <limits.h>


typedef struct {
  int size;
  float *data;
  float duration;
} Samples;

int getSoundPoints(Samples* soundPoints, char* in_file_path, int fps) {

    float min_sample = -1.0f;
    int samples_to_take = 635;
    int frame_count = 0;
    int frames_until_emit;
    int emit_every;

    printf("Using libgroove v%s\n", groove_version());
    groove_init();
    groove_set_logging(GROOVE_LOG_INFO);
    struct GrooveFile *file = groove_file_open(in_file_path);
    if (! file) {
        fprintf(stderr, "Error opening input file: %s\n", in_file_path);
        groove_finish();
        return 1;
    }

    float duration = groove_file_duration(file);

    struct GroovePlaylist *playlist = groove_playlist_create();
    struct GrooveSink *sink = groove_sink_create();
    struct GrooveBuffer *buffer;


    sink->audio_format.sample_rate = 44100;
    sink->audio_format.channel_layout = GROOVE_CH_LAYOUT_MONO;
    sink->audio_format.sample_fmt = GROOVE_SAMPLE_FMT_FLT;
    if (groove_sink_attach(sink, playlist) < 0) {
        fprintf(stderr, "error attaching sink\n");
        return 1;
    }

    struct GroovePlaylistItem *item =
        groove_playlist_insert(playlist, file, 1.0, 1.0,NULL);

    // scan the song for the exact correct duration
    while (groove_sink_buffer_get(sink, &buffer, 1) == GROOVE_BUFFER_YES) {
        frame_count += buffer->frame_count;
        groove_buffer_unref(buffer);
    }
    groove_playlist_seek(playlist, item, 0);


    // Calculate best sample resolution for file
    // duration * fps
    // samples_to_take = ; // take sample every 125ms (at 8)
    emit_every = frame_count / samples_to_take;
    frames_until_emit = emit_every;

    // Initialize vector
    soundPoints->size = 0;
    soundPoints->data = calloc(samples_to_take+1, sizeof(float));
    soundPoints->duration = duration;
    int i;
    while (groove_sink_buffer_get(sink, &buffer, 1) == GROOVE_BUFFER_YES) {
        // process the buffer
        for (i = 0; i < buffer->frame_count && soundPoints->size < samples_to_take;
                i += 1, frames_until_emit -= 1)
        {
            if (frames_until_emit == 0) {
                soundPoints->data[soundPoints->size++] = min_sample;
                frames_until_emit = emit_every;
                min_sample = -1.0f;
            }
            float *samples = (float *) buffer->data[0];
            float sample = samples[i];
            if (sample > min_sample) min_sample = sample;
        }

        groove_buffer_unref(buffer);
    }

    // emit the last column if necessary. This will have to run multiple times
    // if the duration specified in the metadata is incorrect.
    while (soundPoints->size < samples_to_take) {
        soundPoints->data[soundPoints->size++] = 0.0f;
    }

    groove_sink_detach(sink);
    groove_sink_destroy(sink);

    groove_playlist_clear(playlist);
    groove_file_close(file);
    groove_playlist_destroy(playlist);
    groove_finish();

    return 0;
}

float getSample(Samples *vector, int index){
    return vector->data[index];
}

static PyObject* extractWaveform(PyObject* self, PyObject* args)
{
    char* input;

    if(!PyArg_ParseTuple(args, "s", &input)) {
        return NULL;
    }
    Samples result;
    int err = getSoundPoints(&result, input, 8);
    if (err != 0){
      PyErr_SetString(PyExc_TypeError, "Oh no!");
      PyErr_Print();
      return Py_BuildValue("i", err);
    }


    PyObject *pylist = PyTuple_New(result.size);
    PyObject *item;
    int i;
    for (i=0;i < result.size-1; ++i)
    {
         item = Py_BuildValue("f",result.data[i]);
         Py_INCREF(item);
         PyTuple_SetItem(pylist, i, item);;
         Py_DECREF(item);
    }


    return Py_BuildValue("bfO", result.size, result.duration, pylist);
}

static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "1.0");
}

static PyMethodDef wfMethods[] = {
  {"extractWaveform", extractWaveform, METH_VARARGS, "returns the waveform sample from the audio file."},
  {"version", (PyCFunction)version, METH_NOARGS, "returns the version."},
  {NULL, NULL, 0, NULL}
};


static struct PyModuleDef wfModule = {
    PyModuleDef_HEAD_INIT,
    "waveform",
    "Waveform Module",
    -1,
    wfMethods
};

PyMODINIT_FUNC PyInit_waveform(void)
{
    return PyModule_Create(&wfModule);
}
