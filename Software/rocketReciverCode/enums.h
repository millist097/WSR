enum launchStatus { PREBURN, BURN, POSTBURN, APOGEE, DESCENT, 
LANDED};


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

#define FLAG_DATA_RECIVED (flags),(0)
