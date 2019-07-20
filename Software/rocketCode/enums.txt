enum launchStatus { PREBURN, BURN, POSTBURN, APOGEE, DESCENT, 
LANDED};

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

#define FLAG_DATA_AVAILABLE (flags),(0)
#define FLAG_TRANSMIT_DATA (flags),(1)
#define FLAG_MESSAGE_RECIVED (flags),(2)
#define FLAG_ERROR (flags),(3)
