/* ***
 *  Used to  generate sudo random numbers
 *  sequence length: 65535
 *  test case
 *  uint16_t start_state = 0xAEE35;
 *  
 */
unsigned lsrl_fun(uint16_t lfsr){
  uint16_t bit;
  bit = ((lfsr >>0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) );
  lfsr = (lfsr >> 1) | (bit << 15 );
  return lfsr;
}

/* Bit Operation macros*/
#define sbi(b,n)( (b) |= (1<<(n)) )
#define cbi(b,n)( (b) &= (~(1<<(n))) )
#define fbi(b,n)( (b) ^= (1<<(n)) )
#define rbi(b,n)( (b) & (1<<(n)) )

#define set_flag(combo) sbi(combo)
#define clear_flag(combo) cbi(combo)
#define flag_is_set(combo)    rbi(combo)
#define flag_is_clear(combo)  (!rbi(combo))

volatile uint16_t flags;
volatile uint16_t commands;
volatile uint16_t state;
/* Bottom half are activity flags
 *  top half are command flags
 */

#define FLAG_DATA_AVAILABLE (flags),(0)
#define FLAG_TRANSMIT_DATA (flags),(1)
#define FLAG_MESSAGE_RECIVED (flags),(2)
#define FLAG_ERROR (flags),(3)

#define CMD_SEND_DATA (commands),(0)
#define CMD_RESET (commands),(1)
#define CMD_READY_LAUNCH (commands),(2)
#define CMD_STATUS (commands),(3)
#define CMD_STAND_DOWN (commands),(4)

#define STATE_STAND_DOWN (state),(0)
#define STATE_PRELAUNCH (state),(1)
#define STATE_BURN (state),(2)
#define STATE_POST_BURN (state),(3)
#define STATE_APOGEE (state),(4)
#define STATE_DRAG (state),(5)
#define STATE_MAIN_CUTE (state),(6)
#define STATE_LAND (state),(7)
