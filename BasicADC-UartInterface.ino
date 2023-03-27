String message = "";
String testchar= "*";
int x=0;

int bufferlength = 10; 
int analogPin = A0;
int val = 0;
int long runningtotal=0;
float average=0;
int data[500];
int maxbits=1024;
int maxvoltage=5;
int sampletime=10;

// This function is critical to the way the program works. 
// The python interface will send over something like
// c100* which for this program means "change the buffer length that
// will be used to 100 samples. The "c" tells the arduino which function
// to execute. The 100 tells it how many samples, and the * is an
// "end of message character"
//It also removes any newline characters that might have been sent

void removeextrachars(){
   while(message.indexOf("\n")!=-1) //if the message has a newline key hit multiple times this will remove them
   {
   x=message.indexOf("\n");
   message.remove(x,1);
   }
   x=message.indexOf("*");//Now I will remove the *
   message.remove(x,1);
   return;
}

// This function reads the ADC values and fills the samples in an array
 
void fillarray()
{
  for(int i=0; i<bufferlength;i++)   
  {
   data[i] = analogRead(analogPin);
   delay(sampletime);
  }
}

//gets the average of the data in the sample buffer
float getaverage()
  {
    runningtotal=0;
    for(int i=0; i<bufferlength;i++)
    {
      runningtotal+=data[i];
      }
    average=runningtotal/bufferlength;
    return(average);
  }

//This is the "controller" for the interface to the python script.
//The python gui will send things over in the form of:
//<a letter that represents a command to execute><a parameter if there is one(like number of samples)><an asterisk>
//The removeextrachars function cleans that message and just gives <letter><parameter>
//This function evaluates that format and calls the appropriate function

void evaluatemessage(String mymessage){
   
   if(mymessage.charAt(0)=='h'){
    Serial.println("Hello!");
   }
 
  if(mymessage.charAt(0)=='g'){
    Serial.println(average);
  }

  if(mymessage.charAt(0)=='r')
  {
    fillarray();
    average=getaverage();
    Serial.println(average);
    for(int i=0; i<bufferlength;i++ )
    {
    Serial.println(data[i]);
    }
    Serial.println("Capture Done!");
  }

   if(mymessage.charAt(0)=='a')
  {
    fillarray();
    getaverage();
    for(int i=0; i<bufferlength;i++ )
    {
    Serial.println(data[i]);
    }
    Serial.println(average);
    
  }
  if(mymessage.charAt(0)=='c'){
     String tempstring=mymessage.substring(1);//get the parameter entered after the c
     String outmessage="The buffer Length is now: ";
     outmessage.concat(tempstring) ;
     bufferlength=tempstring.toInt();
     Serial.println(outmessage);
     return;
   }
  if(mymessage.charAt(0)=='t'){
     String tempstring=mymessage.substring(1);//get the parameter entered after the t
     String outmessage="The sample rate is now: ";
     outmessage.concat(tempstring);
     sampletime=tempstring.toInt();
     Serial.println(outmessage);
     return;
   }
}

void setup()
{
  Serial.begin(9600); // Initialize Serial Monitor. Make sure the port speed is set correctly in the device manager
  while (!Serial) ; // Wait for Serial monitor to open
  // Send a welcome message to the serial monitor:
  Serial.println("Serial Port is open for business!");
  analogReadResolution(12);//Change ADC read resolution to 12bits
}

void loop()
{
  //fillarray();
  //getaverage();
  
  if (Serial.available()) // If data is sent to the monitor
  {
    while (Serial.available()) // While data is available
    {
      // Read from serial and add to the string:
      message += (char)Serial.read();
    }
    if(message.endsWith(testchar))
    {
      removeextrachars();
      evaluatemessage(message);
      message="";
    }
  }
}
