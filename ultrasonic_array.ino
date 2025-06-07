/*
 * HC-SR04 example sketch
 *
 * https://create.arduino.cc/projecthub/Isaac100/getting-started-with-the-hc-sr04-ultrasonic-sensor-036380
 *
 * by Isaac100
 */

const int trigPins[] = {11,10,9,8,7,6};
const int echoPin = 12;

const int distLimit = 6050;

const int sensorCount = 6;

float dist_array[] = {0,0,0,0,0,0};

void setup() {
  for (int i=0;i<sensorCount;i++)
    pinMode(trigPins[i], OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

float getUltraDist(int pin)
{
  float duration, distance;
  digitalWrite(pin, LOW);
  delayMicroseconds(2);
  digitalWrite(pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pin, LOW);

  duration = pulseIn(echoPin, HIGH, distLimit);
  //if (duration == 0)
  //{
  //  return 0.0;
  //}
  //else
  {
    distance = (duration*.0343)/2;
    return distance;
  }
}

void loop() {
  for (int i=0;i<sensorCount;i++)
  {
    dist_array[i] = getUltraDist(trigPins[i]);
    Serial.print(dist_array[i]);
    Serial.print(",");
    delay(20);
  }
  Serial.print("\n");
}
