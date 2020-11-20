#include <stdint.h>
#include <stdio.h>
#include <logger/logger.h>

#include "camera.h"

/* Variables */
#define STREAM_HOST "192.168.10.168"
#define STREAM_PORT 5000
#define STREAM_FPS 26
#define STREAM_BITRATE 2000000
#define STREAM_W 450
#define STREAM_H 600


typedef void transition_func_t(CameraClass_t *cam);
typedef void run_func_t(CameraClass_t *cam);

/* Functions */
void transition(CameraClass_t *cam, camera_state_t new_state);
void runState(CameraClass_t *cam);
int initStream();
int killStream();

void do_nothing(CameraClass_t *cam);

void do_to_init(CameraClass_t *cam);
void do_to_idle(CameraClass_t *cam);
void do_to_stream(CameraClass_t *cam);
void do_to_photo(CameraClass_t *cam);
void do_to_fault(CameraClass_t *cam);

void do_init(CameraClass_t *cam);
void do_idle(CameraClass_t *cam);
void do_stream(CameraClass_t *cam);
void do_photo(CameraClass_t *cam);
void do_fault(CameraClass_t *cam);

transition_func_t * const transition_table[ CAMERA_NUM_STATES ][ CAMERA_NUM_STATES ] = {
    { do_to_init, do_to_idle, do_nothing,   do_nothing,  do_to_fault },
    { do_nothing, do_nothing, do_to_stream, do_to_photo, do_to_fault },
    { do_nothing, do_nothing, do_nothing,   do_to_photo, do_to_fault },
    { do_nothing, do_nothing, do_nothing,   do_nothing,  do_to_fault },
    { do_nothing, do_to_idle, do_nothing,   do_nothing,  do_nothing  },
};

run_func_t * const run_table[ CAMERA_NUM_STATES ] = {
    do_init, do_idle, do_stream, do_photo, do_fault
};

void do_to_init(CameraClass_t *cam) {
    //test camera existance
    cam->state = CAMERA_STATE_IDLE;
}

void do_to_stream(CameraClass_t *cam) {
    initStream(cam);
    cam->state = CAMERA_STATE_STREAM;
}

int cameraInit (CameraClass_t *cam) {
    cam->run = &runState;
    cam->transition = &transition;
    cam->state = CAMERA_STATE_INIT;
    cam->stream_host = STREAM_HOST;
    cam->stream_port = STREAM_PORT;
    cam->stream_fps = STREAM_FPS;
    cam->stream_bitrate = STREAM_BITRATE;
    cam->stream_w = STREAM_W;
    cam->stream_h = STREAM_H;
    cam->transition(&cam, CAMERA_STATE_INIT);
    return 0;
}

void transition(CameraClass_t *cam, camera_state_t new_state) {
    transition_func_t *transition_fn = 
        transition_table[ cam->state ][ new_state ];

    transition_fn(&cam);
}

void runState(CameraClass_t *app) {
    run_func_t *run_fn = run_table[ app->state ];

    run_fn(&app);
}

int initStream(CameraClass_t *cam) {
  LOG_INFO("Starting stream");
  char cmd[248];
  sprintf(cmd,
    "gst-launch-1.0 -v rpicamsrc bitrate=%d ! h264parse ! rtph264pay config-interval=1 pt=96! gdppay ! tcpserversink host=%s port=%d &",
    cam->stream_bitrate,
    cam->stream_host,
    cam->stream_port);
  int status = system(cmd);
  if (status != 0) {
    LOG_ERROR("Failed to start stream with exit code %d.", status / 256);
  }
  return(status/256);
}


int killStream() {
  LOG_INFO("Ending stream\n");
  int status = system("pkill gst-launch*");
  if (status != 0) {
    LOG_ERROR("Failed to kill stream with exit code %d.\n", status / 256);
  }
  return(status/256);
}