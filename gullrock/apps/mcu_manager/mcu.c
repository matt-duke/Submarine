#include <stdint.h>
#include <stdio.h>

#include <hiredis-vip/hiredis.h>
#include <hiredis-vip/async.h>
#include <hiredis-vip/adapters/libevent.h>
#include <libserialport/libserialport.h>
#include <minihdlc/minihdlc.h>
#include <logger/logger.h>

#include <common.h>
#include <redis_def.h>
#include <hdlc_def.h>
#include "mcu.h"

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;

struct sp_port *port;

/* Functions */
typedef void transition_func_t(McuClass_t *mcu);
typedef void run_func_t(McuClass_t *mcu);

int mcuTransition(McuClass_t *mcu, mcu_state_t new_state);
void mcuRunState(McuClass_t *mcu);

void do_nothing(McuClass_t *mcu);

void do_to_ready(McuClass_t *mcu);
void do_to_init(McuClass_t *mcu);
void do_to_post(McuClass_t *mcu);
void do_to_fault(McuClass_t *mcu);

void do_init(McuClass_t *mcu);
void do_post(McuClass_t *mcu);
void do_running(McuClass_t *mcu);
void do_fault(McuClass_t *mcu);

void hdlc_frame_handler(const uint8_t *buffer, uint16_t length);
void hdlc_send_char(uint8_t data);
int check(enum sp_return result);
void read_hdlc();
void hdlc_status();
void initSerial();

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
    mcu->run = &mcuRunState;
    mcu->transition = &mcuTransition;
    mcu->get = &mcuGet;
    mcu->set = &mcuSet;
    mcu->state = MCU_STATE_INIT;
    mcu->transition(MCU_STATE_INIT);
    return 0;
}

int mcuTransition(McuClass_t *mcu, mcu_state_t new_state) {
    transition_func_t *transition_fn = 
        transition_table[ mcu->state ][ new_state ];
    
    transition_fn(mcu);
    if (mcu->state != new_state) {
        LOG_ERROR("Transition blocked");
        return 1;
    }
    return 0;
}

void mcuRunState(McuClass_t *mcu) {
    run_func_t *run_fn = run_table[ mcu->state ];

    run_fn(mcu);
}

int mcuSet(McuClass_t *mcu, int key, int data) {

}

int mcuGet(McuClass_t *mcu, int key, int data) {

}

void hdlc_frame_handler(const uint8_t *buffer, uint16_t length) {
	switch (buffer[0]) {
		case COMMAND_STATUS:
			mcu_status = buffer[1];
			LOG_DEBUG("STATUS received: %d\n", mcu_status);
			break;
		case COMMAND_SENSOR:
			set_sensor(buffer);
		default:
			LOG_DEBUG("Msg received of type: %d\n", buffer[0]);
	}
}

void hdlc_send_char(uint8_t data) {
	LOG_DEBUG("Sending: %d", data);
	check(sp_blocking_write(port, &data, 1, 100));
}

void read_hdlc() {
	while (sp_input_waiting(port) > 0) {
		uint8_t rx;
		LOG_DEBUG("Received: %d", rx);
		check(sp_blocking_read(port, &rx, 1, 100));
		minihdlc_char_receiver(rx);
	}
}

void hdlc_status() {
	// test connection
	uint8_t data_buffer[PACKET_SIZE] = {COMMAND_STATUS,0,0,0,0,0};
	minihdlc_send_frame(data_buffer, PACKET_SIZE);
	read_hdlc();
	while (mcu_status == STATUS_NONE) {
		read_hdlc();
	}
	/* Set a key */
	pthread_mutex_lock(&mutex);
	redisAppendCommand(c,"SET %s %s", CHANNEL_KEY[CHANNEL_MCU_STATUS], STATUS_NAME[mcu_status]);
	redisAppendCommand(c,"EXPIRE %s %d", CHANNEL_KEY[CHANNEL_MCU_STATUS], VALIDITY_TIMEOUT);
	LOG_DEBUG("SET: %s\n", reply->str);
	freeReplyObject(reply);
	pthread_mutex_unlock(&mutex);
}

void initSerial() {
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
	hdlc_status();
}