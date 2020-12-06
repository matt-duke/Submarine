#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <logger.h>
#include <stdbool.h>

#include "common.h"
#include "camera.h"

/* Variables */
#define STREAM_HOST "192.168.10.168" //get from redis
#define STREAM_PORT 5000
#define STREAM_FPS 26
#define STREAM_BITRATE 2000000
#define STREAM_W 450
#define STREAM_H 600


typedef void transition_func_t(CameraClass_t *cam);
typedef void run_func_t(CameraClass_t *cam);

/* Functions */
static int transition(CameraClass_t *cam, camera_state_t new_state);
static void runState(CameraClass_t *cam);
static int take_photo(CameraClass_t *cam);

static int start_stream();
static int kill_stream();

static void do_nothing(CameraClass_t *cam);

static void do_to_init(CameraClass_t *cam);
static void do_to_post(CameraClass_t *cam);
static void do_to_idle(CameraClass_t *cam);
static void do_to_stream(CameraClass_t *cam);
static void do_to_fault(CameraClass_t *cam);

static void do_post(CameraClass_t *cam);
static void do_idle(CameraClass_t *cam);
static void do_stream(CameraClass_t *cam);
static void do_fault(CameraClass_t *cam);

transition_func_t * const transition_table[ CAMERA_NUM_STATES ][ CAMERA_NUM_STATES ] = {
    { do_to_init, do_to_post, do_to_idle,  do_nothing,   do_to_fault },
    { do_nothing, do_nothing, do_to_idle,  do_nothing,   do_to_fault },
    { do_nothing, do_nothing, do_nothing,  do_to_stream, do_to_fault },
    { do_nothing, do_nothing, do_nothing,  do_nothing,   do_to_fault },
    { do_nothing, do_to_idle, do_nothing,  do_nothing,   do_nothing  },
};

run_func_t * const run_table[ CAMERA_NUM_STATES ] = {
    do_nothing, do_post, do_idle, do_stream, do_fault
};

void do_nothing(CameraClass_t *cam) {

}

void do_to_init(CameraClass_t *cam) {
    //test camera existance
    cam->state = CAMERA_STATE_INIT;
    cam->transition(cam, CAMERA_STATE_POST);
}

void do_to_idle(CameraClass_t *cam) {
  cam->state = CAMERA_STATE_IDLE;
}

void do_to_post(CameraClass_t *cam) {
  cam->state = CAMERA_STATE_POST;
  bool result = true;
  char *cmd = "/opt/vc/bin/vcgencmd get_camera";
  char *output;

  if(run_cmd(&cmd, &output)) {
    LOG_ERROR("Error running cmd");
    result = false;
  } else if (strcmp(output, "supported=0 detected=0") != 0) {
    result = false;
  }
  if (!result) {
    cam->transition(cam, CAMERA_STATE_FAULT);
  } else {
    cam->transition(cam, CAMERA_STATE_IDLE);
  }
}

void do_to_stream(CameraClass_t *cam) {
    cam->state = CAMERA_STATE_STREAM;

    start_stream(cam);
}

void do_to_fault(CameraClass_t *cam) {
  cam->state = CAMERA_STATE_FAULT;
  kill_stream();
}

void do_post(CameraClass_t *cam) {

}
void do_idle(CameraClass_t *cam) {

}
void do_stream(CameraClass_t *cam) {

}
void do_fault(CameraClass_t *cam) {

}

int cameraInit (CameraClass_t *cam) {
    cam->run = &runState;
    cam->transition = &transition;
    cam->take_photo = &take_photo;
    cam->state = CAMERA_STATE_INIT;
    cam->stream_host = STREAM_HOST;
    cam->stream_port = STREAM_PORT;
    cam->stream_fps = STREAM_FPS;
    cam->stream_bitrate = STREAM_BITRATE;
    cam->stream_w = STREAM_W;
    cam->stream_h = STREAM_H;
    cam->transition(cam, CAMERA_STATE_INIT);
    return 0;
}

int transition(CameraClass_t *cam, camera_state_t new_state) {
    transition_func_t *transition_fn = 
        transition_table[ cam->state ][ new_state ];

    transition_fn(cam);
    if (cam->state != new_state) {
      LOG_ERROR("Unable to transition from %s to %s.", cam->state, new_state);
      return 1;
    }
}

void runState(CameraClass_t *cam) {
    run_func_t *run_fn = run_table[ cam->state ];

    run_fn(cam);
}

int take_photo(CameraClass_t *cam) {
  if (cam->state == CAMERA_STATE_STREAM) {
    kill_stream();
    //take photo
    start_stream(cam);
    return(0);
  }
}

int start_stream(CameraClass_t *cam) {
  LOG_INFO("Starting stream");
  char cmd[248];
  sprintf(cmd,
    "gst-launch-1.0 -v rpicamsrc bitrate=%d ! h264parse ! rtph264pay config-interval=1 pt=96! gdppay ! tcpserversink host=%s port=%d &",
    cam->stream_bitrate,
    cam->stream_host,
    cam->stream_port);
  int status = system(cmd)/256;
  if (status != 0) {
    LOG_ERROR("Failed to start stream with exit code %d.", status);
  }
  return(status);
}


int kill_stream() {
  LOG_INFO("Ending stream\n");
  int status = system("pkill gst-launch*");
  if (status != 0) {
    LOG_ERROR("Failed to kill stream with exit code %d.", status);
  }
  return(status);
}