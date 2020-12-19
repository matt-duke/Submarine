#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#include <hiredis-vip/hiredis.h>
#include <hiredis-vip/async.h>
#include <hiredis-vip/adapters/libevent.h>
#include <libserialport/libserialport.h>
#include <minihdlc/minihdlc.h>
#include <c-logger/logger.h>

#include <common.h>
#include <redis.h>
#include <hdlc_def.h>
#include "mcu.h"

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;

uint8_t msg_count;
buffer_t* global_buffer;

typedef void transition_func_t(McuClass_t *mcu);
typedef void run_func_t(McuClass_t *mcu);

struct sp_port *port;

/* Functions */
static int transition(McuClass_t *mcu, mcu_state_t new_state);
static void runState(McuClass_t *mcu);

static void do_nothing(McuClass_t *mcu);

static void do_to_ready(McuClass_t *mcu);
static void do_to_init(McuClass_t *mcu);
static void do_to_post(McuClass_t *mcu);
static void do_to_fault(McuClass_t *mcu);

static void do_init(McuClass_t *mcu);
static void do_post(McuClass_t *mcu);
static void do_ready(McuClass_t *mcu);
static void do_fault(McuClass_t *mcu);

static int mcuSet(McuClass_t *mcu, uint8_t key, data_t data);
static int mcuGet(McuClass_t *mcu, uint8_t key);

static void hdlc_frame_handler(const uint8_t *buffer, uint16_t length);
static void hdlc_send_char(uint8_t data);
static void hdlc_read();
static int send_frame(packet_t *packet);
static int check(enum sp_return result);

transition_func_t * const transition_table[ MCU_NUM_STATES ][ MCU_NUM_STATES ] = {
    { do_to_init, do_to_post, do_nothing,  do_to_fault },
    { do_nothing, do_nothing, do_to_ready, do_to_fault },
    { do_nothing, do_to_post, do_nothing,  do_to_fault },
    { do_nothing, do_to_post, do_to_ready,  do_nothing }
};

run_func_t * const run_table[ MCU_NUM_STATES ] = {
    do_init, do_post, do_ready, do_fault
};

void do_to_init(McuClass_t *mcu) {
    LOG_INFO("Entering state INIT");
    mcu->state = MCU_STATE_INIT;

	/* Open and configure each port. */
	LOG_DEBUG("Looking for port %s.\n", PORT_NAME);
	check(sp_get_port_by_name(PORT_NAME, &port));

	LOG_INFO("Opening port.\n");
	check(sp_open(port, SP_MODE_READ_WRITE));

	LOG_DEBUG("Setting port to 9600 8N1, no flow control.\n");
	check(sp_set_baudrate(port, 9600));
	check(sp_set_bits(port, 8));
	check(sp_set_parity(port, SP_PARITY_NONE));
	check(sp_set_stopbits(port, 1));
	check(sp_set_flowcontrol(port, SP_FLOWCONTROL_NONE));

	sleep(1);

	minihdlc_init(hdlc_send_char, hdlc_frame_handler);
}

void do_to_ready(McuClass_t *mcu) {
    LOG_INFO("Entering state READY");
    mcu->state = MCU_STATE_READY;
}

void do_to_post(McuClass_t *mcu) {
    LOG_INFO("Entering state POST");
    mcu->state = MCU_STATE_POST;
}

void do_to_fault(McuClass_t *mcu) {
    LOG_INFO("Entering state FAULT");
    mcu->state = MCU_STATE_FAULT;
}

void do_init(McuClass_t *mcu) {

}

void do_post(McuClass_t *mcu) {
    
}

void do_ready(McuClass_t *mcu) {
    
}

void do_fault(McuClass_t *mcu) {
    
}

int mcuInit (McuClass_t *mcu) {
    mcu->run = &runState;
    mcu->transition = &transition;
    mcu->get = &mcuGet;
    mcu->set = &mcuSet;
    mcu->state = MCU_STATE_INIT;
    mcu->transition(mcu, MCU_STATE_INIT);
    return 0;
}

int transition(McuClass_t *mcu, mcu_state_t new_state) {
    transition_func_t *transition_fn = 
        transition_table[ mcu->state ][ new_state ];
    
    transition_fn(mcu);
    if (mcu->state != new_state) {
        LOG_ERROR("Transition blocked");
        return 1;
    }
    return 0;
}

void runState(McuClass_t *mcu) {
    run_func_t *run_fn = run_table[ mcu->state ];
    run_fn(mcu);
}

int mcuGet(McuClass_t *mcu, uint8_t key) {
	packet_t *packet;
	packet = malloc(PACKET_SIZE);
	packet->type = HDLC_SET;
	packet->key = key;
	//packet->data = data;
	if (send_frame(packet) == 0) {
		free(packet);
		//do stuff with global_buffer
	};
	return 0;
}

int send_frame(packet_t *packet) {
	packet->id = msg_count;
	buffer_t *buffer;
	buffer->packet = *packet;
	minihdlc_send_frame(buffer->bytes, PACKET_SIZE);
	msg_count++;
	hdlc_read();
	if (packet->id != global_buffer->packet.id) {
		LOG_ERROR("TX RX ID out of sync.");
		return 1;
	}
	free(buffer);
	return 0;
}

void hdlc_frame_handler(const uint8_t *buffer, uint16_t length) {
	if (length != PACKET_SIZE) {
		LOG_ERROR("HDLC frame dropped, bad length: %d.", length);
		abort();
	}
	global_buffer = *buffer;
}

void hdlc_send_char(uint8_t data) {
	LOG_DEBUG("Sending: %d", data);
	check(sp_blocking_write(port, &data, 1, 100));
}

void hdlc_read() {
	while (sp_input_waiting(port) > 0) {
		uint8_t rx;
		LOG_DEBUG("Received: %d", rx);
		check(sp_blocking_read(port, &rx, 1, 100));
		minihdlc_char_receiver(rx);
	}
}