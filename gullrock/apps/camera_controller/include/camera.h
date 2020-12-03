#ifndef CAMERA_H
#define CAMERA_H

typedef enum { 
    CAMERA_STATE_INIT,
    CAMERA_STATE_POST,
    CAMERA_STATE_IDLE,
    CAMERA_STATE_STREAM,
    CAMERA_STATE_FAULT,
    CAMERA_NUM_STATES } camera_state_t;

typedef struct sCameraClass {
    void (*run)(struct sCameraClass *self);
    int (*transition)(struct sCameraClass *self, camera_state_t new_state);
    int (*take_photo)(struct sCameraClass *self);
    camera_state_t state;
    char *stream_host;
    int stream_port;
    int stream_fps;
    int stream_bitrate;
    int stream_w;
    int stream_h;
} CameraClass_t;

int cameraInit (CameraClass_t *cam);

#endif