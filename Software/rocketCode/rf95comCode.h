/**
Header file for communication protocals for the RF95
module for rocket telemertry system
**/

/* messageType used to identify a message*/
enum messageType {  STATE, DATA, COMMAND, TEST, ERROR, ACKNOWLEDGE };
enum commandType {SENDDATA, RESETSYSTEM,READY_FOR_LAUNCH,STATUS,STANDDOWN};
/* Creates a array of uint8_t that combines the destination
   and senders address with the data. it also appends a CRC value
   to confirm message integraty. 
   message form
   		selfId
		receiverId
		MessageType
		Data
		CRC
 */
void sendData(RH_RF95 &rf95, uint8_t selfId, uint8_t reciverId, uint8_t *data, uint8_t bufLen, 
              messageType type){
  uint8_t package[bufLen + 5];
  byte crc = 0;
  package[0] = reciverId;
  crc ^= selfId;
  package[1] = selfId;
  crc ^= reciverId;
  package[2] = (uint8_t)type;
  crc ^= package[2];
  package[3] = bufLen;
  crc ^= package[3];
  for(int i = 0; i < bufLen;i++){
    package[4+i] = data[i];
    crc ^= data[i];
  }
  package[4+bufLen] = crc;

  rf95.send(package,5+bufLen);
  //  Serial.print("CRC: 0x"); // used for debugging
  // Serial.println(crc,HEX);  // used for debugging
}

void sendAcknoledge(RH_RF95 &rf95, uint8_t selfId, uint8_t receiverId ){
  uint8_t package[4];
  byte crc = 0;
  package[0] = receiverId;
  crc ^= package[0];
  package[0] = selfId;
  crc ^= package[1];
  package[2] = (uint8_t)ACKNOWLEDGE;
  crc ^= package[2];
  package[3] = crc;
  rf95.send(package,4);

}

void sendError(RH_RF95 &rf95, uint8_t selfId, uint8_t receiverId){
  uint8_t package[4];
  byte crc = 0;
  package[0] = receiverId;
  crc ^= package[0];
  package[0] = selfId;
  crc ^= package[1];
  package[2] = (uint8_t)ERROR;
  crc ^= package[2];
  package[3] = crc;
  rf95.send(package,4);
}

void processRecivedMessage(RH_RF95 &rf95, uint8_t selfId){
    if (rf95.available()){
      Serial.println("Message Recived");
      // Should be a message for us now
      uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
      uint8_t len = sizeof(buf);
      
      if (rf95.recv(buf, &len)){
        digitalWrite(LED, HIGH);
        //check to see if it is for self
        if( buf[0] == selfId){ // if for me
          //check CRC
          byte crc = 0;
          for( int i = 0; i<len-1; i++){
            crc ^= buf[i];
          }
          // check the crc
          if( buf[len-1] == crc){
            
            // if tree to determine message type and how to handle it
            if(buf[2]==(unit8_t)DATA){
              sendAcknoledge(&rf95,myAddress, buf[1]);
              for( int i = 0; i < buf[3]; i++){
                dataSetRecived[i] = buf[4+i];
              }
              set_flag(FLAG_DATA_RECIVED);
            }else if( buf[2] == (unit8_t)COMMAND{
              uint8_t command = buf[3];
              if(command == SENDDATA){
                set_flag(CMD_SEND_DATA);
              }else if( command == RESETSYSTEM ){
                set_flag(CMD_RESET); 
              }else if( command == READY_FOR_LAUNCH){
                set_flag(CMD_READY_LAUNCH);
              }else if( command == STATUS){
                set_flag( CMD_STATUS );
              }else if( command == ,STANDDOWN){
                set_flag( CMD_STAND_DOWN );
              }else{
                Serial.println("Invalid message recived");
              }
              
            }else if( buf[2] == (unit8_t)STATE{
              if( buf[3] == -1){
                set_flag(
              }
            }else if( buf[2] == (unit8_t)TEST{
              
            }else if( buf[2] == (uint8_t)ERROR{
              
            }else if( buf[2] == (uint8_t)ACKNOWLEDGE{
              
            }
           
            Serial.println("Aknowledgement Sent");
          }else{
            sendError(rf95, myAddress, reciverAddress);
            Serial.println("Error Sent");
          }
          digitalWrite(LED, LOW);
        }
      }else{
        Serial.println("No message.");
      }  
  }// Message Recived --end protocal
}
