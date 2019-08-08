

uint16_t start_state = 0xD295;
uint16_t randomNum = start_state;
uint16_t count = 0;
uint16_t bottom_mask = 0x00FF;
bool flag_LED = false;
#define LED 13

unsigned lsrl_fun(uint16_t lfsr){
  uint16_t bit;
  uint16_t count = lfsr & 0x00F0;
  bit = ((lfsr >>0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) );
  lfsr = (lfsr >> 1) | (bit << 15 );
  count = count >> 4;
 // Serial.println(count);
 // for(int i =count; i> 0; i--){
  //  bit = ((lfsr >>0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) );
  //  lfsr = (lfsr >> 1) | (bit << 15 );
 // }
  return lfsr;
}

const int arraySize= 100;
float refArray[arraySize];
int distrabution[arraySize];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED,OUTPUT);
  while(!Serial){
    for(int i = 0; i < 3; i++){
      digitalWrite(LED,HIGH);
      delay(150);
      digitalWrite(LED,LOW);
      delay(150);
    }
    delay(1000);
  }

}

uint16_t firstNum = 0;
char received[30];


void loop() {
  // put your main code here, to run repeatedly:
  float temp1 = 1.0/arraySize;
  for(int i = 0; i <arraySize; i++){
    refArray[i] = temp1;
    distrabution[i] = 0;
    temp1 = temp1 + 1.0/arraySize;
    
  }
  
  randomNum = lsrl_fun(randomNum);
  uint16_t temp = randomNum;// & bottom_mask;
  
  for(int i=0;i<100000;i++){
    randomNum = lsrl_fun(randomNum);
    temp = randomNum;// & bottom_mask;
    float ranNum = temp /65535.0;
    
    for(int j=0; j<arraySize;j++){
      if( ranNum <= refArray[j]){
        distrabution[j] = distrabution[j]+1;
        break;
      }
    }
      
  }
 /* Serial.print("DATA");Serial.print(',');
  Serial.print(temp/255.0);Serial.print(",");
  Serial.print(randomNum%12,DEC); Serial.print(",");
  Serial.print(randomNum%11,DEC); Serial.print(",");
  Serial.print(count,DEC); Serial.print(',');
  Serial.println(millis(),DEC);
*/

  Serial.println("distrabution follows:");
  for(int i=0; i<arraySize; i++){
    Serial.print(refArray[i],5);
    Serial.print(',');
  }
  Serial.println('.');
  for(int i=0; i<arraySize; i++){
    Serial.print(distrabution[i]);
    Serial.print(',');
  }
  Serial.println('.');
  delay(10000);

  
  if( count == 0){
    //Serial.println("Begin sequence.");
    firstNum = randomNum;
    count = count +1;
  }else if(randomNum == firstNum){
    //Serial.print("End sequence. Length: ");
    //Serial.println( count, DEC);
    while(1){}
    count == 0;
  }else{
    count = count + 1;
  }

  delay(250);
  if( flag_LED){
    digitalWrite(LED,LOW);
    flag_LED = true;
  }else {
    digitalWrite(LED,HIGH);
    flag_LED = false;
  }
  if( Serial.available() >0){
    int lngth = Serial.readBytesUntil('\n', received,30);
    received[lngth]=NULL;
    delay(50);
    Serial.print("ECHO");Serial.print(',');
    Serial.println(received);
    received[0]=NULL;
  }
}
