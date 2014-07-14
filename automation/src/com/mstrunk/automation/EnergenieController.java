import com.pi4j.io.gpio.*;

/**
 * Created with IntelliJ IDEA.
 * User: ga2salw
 * Date: 14/07/14
 * Time: 09:04
 *
 * **********************************************************************
 * ORGANIZATION : mstrunkdevelopment
 * PROJECT : home automation
 * FILENAME : EnergenieController.java
 *
 * %%
 * Copyright (C) 2014 Matthew Salt
 * %%
 * Licensed under the Apache License, Version 2.0 (the "License"); you
 * may not use this file except in compliance with the License. You may obtain a copy of the License
 * at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 *
 * Allows manual control of the energenie pi breakout board from the command line. The board can send up to four pairs of
 * on/off signals. This class currently only allows for two. This makes use of the pi4j library and therefore the wiringPi
 * pin numbering scheme.
 *
 * The energenie board uses 4 digial bits to make up the control message. The available options are shown below. The
 * first three rows of each table are implemented in this class.
 *
 * |D3 | D2 | D1 | D0 | Meaning
 * | 1 | 0  | 1  | 1  | All On
 * | 1 | 1  | 1  | 1  | S1 On
 * | 1 | 1  | 1  | 0  | S2 On
 * | 1 | 1  | 0  | 1  | S3 On
 * | 1 | 1  | 0  | 0  | S4 On
 *
 * | 0 | 0  | 1  | 1  | All Off
 * | 0 | 1  | 1  | 1  | S1 Off
 * | 0 | 1  | 1  | 0  | S2 Off
 * | 0 | 1  | 0  | 1  | S3 Off
 * | 0 | 1  | 0  | 0  | S4 Off
 *
 */
public class EnergenieController {

    GpioController gpioController;
    GpioPinDigitalOutput d0;
    GpioPinDigitalOutput d1;
    GpioPinDigitalOutput d2;
    GpioPinDigitalOutput d3;
    GpioPinDigitalOutput modulator;
    GpioPinDigitalOutput keyshiftMode;


    public static void main(String[] args){
        EnergenieController energenie = new EnergenieController();
        energenie.init();
        try {
            energenie.start();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    /**
     * Pin Headers
     * Pi pin 11 = GPIO_0 = d0
     * Pi pin 13 = GPIO_2 = d3
     * Pi pin 15 = GPIO_3 = d1
     * Pi pin 16 = GPIO_4 = d2
     * Pi pin 18 = GPIO_5 = keyShiftMode
     * Pi pin 22 = GPIO_6 = modulator
     */

    public void init(){
         gpioController = GpioFactory.getInstance();
         //Default all output pins to off;
         d0 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_00, "d0 out",PinState.LOW);
         d1 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_03, "d1 out",PinState.LOW);
         d2 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_04, "d2 out",PinState.LOW);
         d3 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_02, "d3 out",PinState.LOW);
         //Set modulator off so no commands being sent
         modulator = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_06,"modulator control",PinState.LOW);
         //Low here tells the modulator to use ON/OFF keying
         keyshiftMode = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_05,"key shift mode control",PinState.LOW);

         //Add shutdown hooks so all pins default to off on shutdown
        d0.setShutdownOptions(true,PinState.LOW);
        d1.setShutdownOptions(true,PinState.LOW);
        d2.setShutdownOptions(true,PinState.LOW);
        d3.setShutdownOptions(true,PinState.LOW);
        modulator.setShutdownOptions(true,PinState.LOW);
        keyshiftMode.setShutdownOptions(true,PinState.LOW);
    }

    public void start() throws InterruptedException{

        printBoilerPlate();
        for(;;){
            String command = System.console().readLine();
            if(command.equalsIgnoreCase("one on")){
                d0.setState(PinState.HIGH);
                d1.setState(PinState.HIGH);
                d2.setState(PinState.HIGH);
                d3.setState(PinState.HIGH);
                sendSignalToSocket();
                System.out.println("Socket 1 State = ON");
            }else if(command.equalsIgnoreCase("one off")){
                d0.setState(PinState.HIGH);
                d1.setState(PinState.HIGH);
                d2.setState(PinState.HIGH);
                d3.setState(PinState.LOW);
                sendSignalToSocket();
                System.out.println("Socket 1 State = OFF");
            }else if(command.equalsIgnoreCase("two on")){
                d0.setState(PinState.LOW);
                d1.setState(PinState.HIGH);
                d2.setState(PinState.HIGH);
                d3.setState(PinState.HIGH);
                sendSignalToSocket();
                System.out.println("Socket 2 State = ON");
            }else if(command.equalsIgnoreCase("two off")){
                d0.setState(PinState.LOW);
                d1.setState(PinState.HIGH);
                d2.setState(PinState.HIGH);
                d3.setState(PinState.LOW);
                sendSignalToSocket();
                System.out.println("Socket 2 State = OFF");
            }else if(command.equalsIgnoreCase("both on")){
                d0.setState(PinState.HIGH);
                d1.setState(PinState.HIGH);
                d2.setState(PinState.LOW);
                d3.setState(PinState.HIGH);
                sendSignalToSocket();
                System.out.println("Socket 1 & 2 State = ON");
            }else if(command.equalsIgnoreCase("both off")){
                d0.setState(PinState.HIGH);
                d1.setState(PinState.HIGH);
                d2.setState(PinState.LOW);
                d3.setState(PinState.LOW);
                sendSignalToSocket();
                System.out.println("Socket 1 & 2 State = OFF");
            }else if(command.equalsIgnoreCase("clear")){
                d0.setState(PinState.LOW);
                d1.setState(PinState.LOW);
                d2.setState(PinState.LOW);
                d3.setState(PinState.LOW);
            } else {
                System.out.println("COMMAND NOT RECOGNISED");
            }
        }
    }

    public void sendSignalToSocket() throws InterruptedException{
        Thread.sleep(100);
        modulator.setState(PinState.HIGH);
        //sleep for 250ms
        Thread.sleep(250);
        //disable modulator
        modulator.setState(PinState.LOW);
    }

    private void printBoilerPlate() {
        // display user options menu
        System.out.println("");
        System.out.println("");
        System.out.println("");
        System.out.println("");
        System.out.println("----------------------------------------------------");
        System.out.println(" Welcome to energenie light controller ");
        System.out.println(" Author: Matthew Salt - July 2014 ");
        System.out.println("----------------------------------------------------");
        System.out.println("");

    }


}
