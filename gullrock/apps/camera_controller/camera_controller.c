#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#include <hiredis-vip/hiredis.h>
#include <hiredis-vip/async.h>
#include <hiredis-vip/adapters/libevent.h>
#include <logger/logger.h>

#include <common.h>
#include <definitions.h>

extern const char *__progname;
redisContext *c;
redisReply *reply;
pthread_mutex_t mutex;

bool video_running = false;

const char *stream_host = "192.168.10.168";
int stream_port = 5000;
int stream_fps = 26;
int stream_bitrate = 2000000;
int stream_w = 450;
int stream_h = 600;


int initStream() {
  printf("Starting stream\n");
  char cmd[248];
  sprintf(cmd,
    "gst-launch-1.0 -v rpicamsrc bitrate=%d ! h264parse ! rtph264pay config-interval=1 pt=96! gdppay ! tcpserversink host=%s port=%d &",
    stream_bitrate,
    stream_host,
    stream_port);
  int status = system(cmd);
  if (status != 0) {
    LOG_ERROR("Failed to start stream with exit code %d.\n", status / 256);
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

int main() {
  init_logging();
  
	LOG_INFO("Starting %s", __progname);
  pthread_t thread_id;
  pthread_create(&thread_id, NULL, heartbeatThread, (void*)__progname);

  mutex = init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);

  //initStream();

  while (1) {
    sleep(1);
  }
}
