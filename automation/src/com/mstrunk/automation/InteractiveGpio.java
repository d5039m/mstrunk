package com.mstrunk.automation;

import com.pi4j.io.gpio.*;

/**
 * Created by matthewsalt on 13/07/2014.
 */
public class InteractiveGpio {

    private GpioController controller;
    private GpioPinDigitalOutput red;
    private GpioPinDigitalOutput green;


    public static void main(String[] args){
        InteractiveGpio gpio = new InteractiveGpio();
        gpio.printBoilerPlate();
        gpio.start();
    }

    public InteractiveGpio(){
       controller = GpioFactory.getInstance();
       red = controller.provisionDigitalOutputPin(RaspiPin.GPIO_00, "Red LED", PinState.LOW);
       red.setShutdownOptions(true,PinState.LOW,PinPullResistance.OFF);
       green = controller.provisionDigitalOutputPin(RaspiPin.GPIO_04,"Green LED", PinState.LOW);
       green.setShutdownOptions(true, PinState.LOW, PinPullResistance.OFF);
    }

    public void start(){
        System.out.println("READY FOR COMMANDS");
        for(;;){
            String command =  System.console().readLine();
            if(command.equalsIgnoreCase("red on")){
                red.setState(PinState.HIGH);
                System.out.println("RED ON");
            }
            if(command.equalsIgnoreCase("red off")){
                red.setState(PinState.LOW);
                System.out.println("RED OFF");

            }
            if(command.equalsIgnoreCase("green on")){
                green.setState(PinState.HIGH);
                System.out.println("GREEN ON");

            }
            if(command.equalsIgnoreCase("green off")){
                green.setState(PinState.LOW);
                System.out.println("GREEN OFF");

            }
            if(command.equalsIgnoreCase("both on")){
                green.setState(PinState.HIGH);
                red.setState(PinState.HIGH);
                System.out.println("BOTH ON");

            }
            if(command.equalsIgnoreCase("both off")){
                green.setState(PinState.LOW);
                red.setState(PinState.LOW);
                System.out.println("BOTH OFF");

            }
            if(command.equalsIgnoreCase("help")){
                printHelpText();
            }


        }
    }
}
