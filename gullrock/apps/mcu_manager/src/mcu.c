#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>

#include <libserialport.h>
#include <minihdlc.h>
#include <logger.h>

#include <common.h>
#include <hdlc_def.h>
#include "mcu.h"

/* Variables */
//#define DEBUG_PORT "/dev/ttyAMA0"
#define DEBUG_PORT "/dev/ttyUSB0"
#define PORT "/dev/ttyACM0"

static pthread_t mcu_log_thread;
extern const char *__progname;
redisContext *c;
redisReply *reply;

uint16_t msg_count = 1;
packet_t global_packet = {};

typedef void transition_func_t(McuClass_t *mcu);
typedef void run_func_t(McuClass_t *mcu);

struct sp_port *port;
struct sp_port *debug_port;

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

static int get(McuClass_t *mcu, uint8_t key, data32_t *data);
static int set(McuClass_t *mcu, uint8_t key, data32_t *data);
static void flush();
static void reset();

static void hdlc_frame_handler(const uint8_t *packet, uint16_t length);
static void hdlc_send_char(uint8_t data);
static void hdlc_read();
static int send_frame(packet_t *packet);
static int check(enum sp_return result);

static void *mcuLogThread(void *arg);

transition_func_t * const transition_table[ MCU_NUM_STATES ][ MCU_NUM_STATES ] = {
    { do_to_init, do_to_post, do_nothing,  do_to_fault },
    { do_nothing, do_nothing, do_to_ready, do_to_fault },
    { do_nothing, do_to_post, do_nothing,  do_to_fault },
    { do_nothing, do_to_post, do_to_ready,  do_nothing }
};

run_func_t * const run_table[ MCU_NUM_STATES ] = {
    do_init, do_post, do_ready, do_fault
};

void do_nothing(McuClass_t *mcu) {return;}

void do_to_init(McuClass_t *mcu) {
    LOG_INFO("Entering state INIT");
    mcu->state = MCU_STATE_INIT;

	//pthread_create(&mcu_log_thread, NULL, mcuLogThread, NULL);

	mcu->reset();

	minihdlc_init(hdlc_send_char, hdlc_frame_handler);
}

void do_to_post(McuClass_t *mcu) {
    LOG_INFO("Entering state POST");
    mcu->state = MCU_STATE_POST;
	data32_t tests = {1};
	int reply = mcu->set(mcu, HDLC_TEST, &tests);
	if (reply == HDLC_TYPE_FAILURE) {
		LOG_ERROR("Error requesting MCU to enter POST");
		mcu->transition(mcu, MCU_STATE_FAULT);
		return;
	}
}

void do_to_ready(McuClass_t *mcu) {
    LOG_INFO("Entering state READY");
    mcu->state = MCU_STATE_READY;
}

void do_to_fault(McuClass_t *mcu) {
    LOG_INFO("Entering state FAULT");
    mcu->state = MCU_STATE_FAULT;
}

void do_init(McuClass_t *mcu) {

}

void do_post(McuClass_t *mcu) {

	data32_t data = {};
	if (HDLC_TYPE_SUCCESS == mcu->get(mcu, HDLC_STATE, &data)) {
		LOG_INFO("MCU status: %d", data.ui8[0]);
		if (data.ui8[0] == MCU_STATE_READY) {
			mcu->transition(mcu, MCU_STATE_READY);
		} else if (data.ui8[0] == MCU_STATE_FAULT) {
			mcu->transition(mcu, MCU_STATE_FAULT);
		}
	} else {
		LOG_INFO("Status request failed");
	}
}

void do_ready(McuClass_t *mcu) {
	data32_t data = {};
	if (HDLC_TYPE_SUCCESS == mcu->get(mcu, HDLC_STATE, &data)) {
		LOG_INFO("MCU status: %d", data.ui8[0]);
		if (data.ui8[0] == MCU_STATE_POST) {
			mcu->transition(mcu, MCU_STATE_POST);
		} else if (data.ui8[0] == MCU_STATE_FAULT) {
			mcu->transition(mcu, MCU_STATE_FAULT);
		}
	} else {
		LOG_INFO("Status request failed");
	}
}

void do_fault(McuClass_t *mcu) {
    
}

void mcuInit (McuClass_t *mcu) {
    mcu->run = &runState;
    mcu->transition = &transition;
    mcu->get = &get;
    mcu->set = &set;
	mcu->flush = &flush;
	mcu->reset = &reset;

	mcu->state = MCU_STATE_INIT;
	mcu->transition(mcu, MCU_STATE_INIT);
}

int transition(McuClass_t *mcu, mcu_state_t new_state) {
	mcu_state_t old_state = mcu->state;
    transition_func_t *transition_fn = 
        transition_table[ mcu->state ][ new_state ];
    
    transition_fn(mcu);
    if (mcu->state != new_state) {
		LOG_ERROR("Transition from %d to %d blocked.", old_state, new_state);
		return 1;
    }
    return 0;
}

void runState(McuClass_t *mcu) {
    run_func_t *run_fn = run_table[ mcu->state ];
    run_fn(mcu);
}

int get(McuClass_t *mcu, uint8_t key, data32_t *data) {
	packet_t packet = {};
	packet.s.type = HDLC_TYPE_GET;
	packet.s.key = key;

	if (0 == send_frame(&packet)) {
		hdlc_read(); // will block until response
	} else {
		LOG_ERROR("Error reading.");
		return HDLC_TYPE_FAILURE;
	}
	if (packet.s.id != global_packet.s.id) {
		LOG_ERROR("Global packet ID mismatch: %d != %d", packet.s.id, global_packet.s.id);
		mcu->flush();
		return HDLC_TYPE_FAILURE;
	} else if (packet.s.type == HDLC_TYPE_NOT_IMPLEMENTED) {
		LOG_WARN("Not implemented");
		return HDLC_TYPE_NOT_IMPLEMENTED;
	} else {
		//LOG_INFO("Received data: %d", global_packet.s.data32.value);
		memcpy(data->ui8, global_packet.s.d32.ui8, 4);
		return global_packet.s.type;
	}
}

int set(McuClass_t *mcu, uint8_t key, data32_t *data) {
	packet_t packet = {};
	packet.s.type = HDLC_TYPE_SET;
	packet.s.key = key;
	memcpy(packet.s.d32.ui8, data->ui8, 4);

	if (0 == send_frame(&packet)) {
		hdlc_read(); // will block until response
	} else {
		LOG_ERROR("Error reading.");
		return HDLC_TYPE_FAILURE;
	}
	if (packet.s.id != global_packet.s.id) {
		LOG_ERROR("Global packet ID mismatch: %d != %d", packet.s.id, global_packet.s.id);
		// Out of sync error, clear input buffer
		mcu->flush();
		return HDLC_TYPE_FAILURE;
	} else if (packet.s.type == HDLC_TYPE_NOT_IMPLEMENTED) {
		LOG_WARN("Not implemented");
		return HDLC_TYPE_NOT_IMPLEMENTED;
	} else {
		return global_packet.s.type;
	}
}

int send_frame(packet_t *packet) {
	packet->s.id = msg_count;
	/*for (int i=0;i<PACKET_SIZE;i++) {
		LOG_INFO("packet[%d]=%d", i, packet->ui8[i]);
	}*/
	minihdlc_send_frame(packet->ui8, PACKET_SIZE);
	msg_count++;
	return 0;
}

void hdlc_frame_handler(const uint8_t *packet, uint16_t length) {
	if (length != PACKET_SIZE) {
		LOG_ERROR("HDLC frame dropped, bad length: %d.", length);
		exit(1);
	}
	memcpy(&global_packet, packet, PACKET_SIZE);
}

void hdlc_send_char(uint8_t data) {
	//LOG_DEBUG("Sending: %d", data);
	check(sp_blocking_write(port, &data, 1, 100));
}

void hdlc_read() {
	int timeout = 5 * 1000; //ms
	int count = 0;
	int delay = 1000; //ms
	check(sp_input_waiting(port));
	while(sp_input_waiting(port) == 0) {
		if (count*delay > timeout) {
			LOG_ERROR("Timeout reached.");
			return;
		}
		count++;
		sleep(delay/1000);
	}
	while (sp_input_waiting(port) > 0) {
		uint8_t rx;
		check(sp_blocking_read(port, &rx, 1, 100));
		//LOG_DEBUG("Received: %d", rx);
		minihdlc_char_receiver(rx);
	}
}

static void flush() {
	check(sp_drain(port));
	while (sp_input_waiting(port) > 0) {
		uint8_t rx;
		check(sp_blocking_read(port, &rx, 1, 100));
	}
}

static void reset() {
	LOG_DEBUG("Looking for port %s.", PORT);
	check(sp_get_port_by_name(PORT, &port));
	LOG_INFO("Opening port.");
	check(sp_open(port, SP_MODE_READ_WRITE));
	LOG_DEBUG("Setting port to 9600 8N1, no flow control.");
	check(sp_set_baudrate(port, 9600));
	check(sp_set_bits(port, 8));
	check(sp_set_parity(port, SP_PARITY_NONE));
	check(sp_set_stopbits(port, 1));
	check(sp_set_flowcontrol(port, SP_FLOWCONTROL_NONE));
	check(sp_set_dtr(port, false));
	sleep(1);
	check(sp_set_dtr(port, true));
	sleep(1);
}

void *mcuLogThread(void *arg) {
	const char *logfile = "/tmp/mcu.log";
  	remove(logfile);
	logger_initConsoleLogger(stderr);
	logger_initFileLogger(logfile, 10e6, 5);
	logger_setLevel(LogLevel_DEBUG);

	/* Open and configure each port. */
	check(sp_get_port_by_name(DEBUG_PORT, &debug_port));
	LOG_INFO("Opening debug port.");
	check(sp_open(debug_port, SP_MODE_READ_WRITE));
	check(sp_set_baudrate(debug_port, 9600));
	check(sp_set_bits(debug_port, 8));
	check(sp_set_parity(debug_port, SP_PARITY_NONE));
	check(sp_set_stopbits(debug_port, 1));
	check(sp_set_flowcontrol(debug_port, SP_FLOWCONTROL_NONE));
	LOG_DEBUG("Start logging MCU debug messages");
	
	while (true) {
		int i = 0;
		char *buffer= (char *) malloc(1);
		while (true) {
			char rx;
			check(sp_blocking_read(debug_port, &rx, 1, 0));
			if (rx == '\n') {
				LOG_INFO("MCU MSG: %s", buffer);
				break;
			} else {
				i++;
				// quick and dirty. See https://stackoverflow.com/questions/29070705/realloc-an-array-but-do-not-lose-the-elements-in-it
				char * new = (char *) realloc(buffer, i);
				buffer = new;
				buffer[i-1] = rx;
			}
		}
		free(buffer);
		sleep(0.5);
	}
}

int check(enum sp_return result) {
	int error_code;
	char *error_message;

	switch (result) {

		/* Handle each of the four negative error codes that can be returned.
		 *
		 * In this example, we will end the program on any error, using
		 * a different return code for each possible class of error. */

	case SP_ERR_ARG:
		/* When SP_ERR_ARG is returned, there was a problem with one
		 * or more of the arguments passed to the function, e.g. a null
		 * pointer or an invalid value. This generally implies a bug in
		 * the calling code. */
		LOG_FATAL("Error: Invalid argument.");
		exit(1);

	case SP_ERR_FAIL:
		/* When SP_ERR_FAIL is returned, there was an error from the OS,
		 * which we can obtain the error code and message for. These
		 * calls must be made in the same thread as the call that
		 * returned SP_ERR_FAIL, and before any other system functions
		 * are called in that thread, or they may not return the
		 * correct results. */
		error_code = sp_last_error_code();
		error_message = sp_last_error_message();
		LOG_ERROR("Error: Failed: OS error code: %d, message: '%s'",
			error_code, error_message);
		/* The error message should be freed after use. */
		sp_free_error_message(error_message);
		exit(2);

	case SP_ERR_SUPP:
		/* When SP_ERR_SUPP is returned, the function was asked to do
		 * something that isn't supported by the current OS or device,
		 * or that libserialport doesn't know how to do in the current
		 * version. */
		LOG_FATAL("Error: Not supported.");
		exit(3);

	case SP_ERR_MEM:
		/* When SP_ERR_MEM is returned, libserialport wasn't able to
		 * allocate some memory it needed. Since the library doesn't
		 * normally use any large data structures, this probably means
		 * the system is critically low on memory and recovery will
		 * require very careful handling. The library itself will
		 * always try to handle any allocation failure safely.
		 *
		 * In this example, we'll just try to exit gracefully without
		 * calling printf, which might need to allocate further memory. */
		exit(4);

	case SP_OK:
	default:
		/* A return value of SP_OK, defined as zero, means that the
		 * operation succeeded. */
		//LOG_INFO("Operation succeeded.");

		/* Some fuctions can also return a value greater than zero to
		 * indicate a numeric result, such as the number of bytes read by
		 * sp_blocking_read(). So when writing an error handling wrapper
		 * function like this one, it's helpful to return the result so
		 * that it can be used. */
		return result;
	}
}