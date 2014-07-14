
import com.pi4j.io.gpio.*;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import java.util.Calendar;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

/**
 * Created with IntelliJ IDEA.
 * User: ga2salw
 * Date: 14/07/14
 * Time: 10:56
 * To ch
 * <p/>
 * * |D3 | D2 | D1 | D0 | Meaning
 * | 1 | 0  | 1  | 1  | All On
 * | 1 | 1  | 1  | 1  | S1 On
 * | 1 | 1  | 1  | 0  | S2 On
 * | 1 | 1  | 0  | 1  | S3 On
 * | 1 | 1  | 0  | 0  | S4 On
 * <p/>
 * | 0 | 0  | 1  | 1  | All Off
 * | 0 | 1  | 1  | 1  | S1 Off
 * | 0 | 1  | 1  | 0  | S2 Off
 * | 0 | 1  | 0  | 1  | S3 Off
 * | 0 | 1  | 0  | 0  | S4 Off
 */
public class HolidayLights {

    private static final Log LOG = LogFactory.getLog(HolidayLights.class);


    private Timer timer;

    GpioController gpioController;
    GpioPinDigitalOutput d0;
    GpioPinDigitalOutput d1;
    GpioPinDigitalOutput d2;
    GpioPinDigitalOutput d3;
    GpioPinDigitalOutput modulator;
    GpioPinDigitalOutput keyshiftMode;


    public static void main(String[] args) throws InterruptedException {
        HolidayLights holidaylights = new HolidayLights();
        holidaylights.init();
        holidaylights.start();
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

    public void init() {
        timer = new Timer();

        gpioController = GpioFactory.getInstance();
        //Default all output pins to off;
        d0 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_00, "d0 out", PinState.LOW);
        d1 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_03, "d1 out", PinState.LOW);
        d2 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_04, "d2 out", PinState.LOW);
        d3 = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_02, "d3 out", PinState.LOW);
        //Set modulator off so no commands being sent
        modulator = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_06, "modulator control", PinState.LOW);
        //Low here tells the modulator to use ON/OFF keying
        keyshiftMode = gpioController.provisionDigitalOutputPin(RaspiPin.GPIO_05, "key shift mode control", PinState.LOW);

        //Add shutdown hooks so all pins default to off on shutdown
        d0.setShutdownOptions(true, PinState.LOW);
        d1.setShutdownOptions(true, PinState.LOW);
        d2.setShutdownOptions(true, PinState.LOW);
        d3.setShutdownOptions(true, PinState.LOW);
        modulator.setShutdownOptions(true, PinState.LOW);
        keyshiftMode.setShutdownOptions(true, PinState.LOW);
    }

    public void start() throws InterruptedException {

        //Send off signal to ensure that lights are off when we startup
        turnLightsOff();

        //Lights are scheduled to turn on at a random time between 1830 and 1900
        Random randomGenerator = new Random();
        long fraction = (long) (1 * randomGenerator.nextDouble());
        int randomMinutes = (int) fraction;

        Calendar cal = Calendar.getInstance();
        LOG.info("Current time: " + cal.getTime());
        System.out.println("Current time: " + cal.getTime());

        cal.set(Calendar.HOUR_OF_DAY, 12);
        cal.set(Calendar.MINUTE, 3 + randomMinutes);
        cal.set(Calendar.SECOND, 20);
        cal.set(Calendar.MILLISECOND, 0);

        LOG.info("Setting 'lightsup' time to: " + cal.getTime());
        System.out.println("Setting 'lightsup' time to: " + cal.getTime());
        timer.schedule(new TurnOnTask(), cal.getTime());

        //Keep lights on for two hours. Schedule a shutdown task for 2 hours from lightsOn
        cal.roll(Calendar.MINUTE, 1);
        LOG.info("Setting 'lightsdown' time to: " + cal.getTime());
        System.out.println("Setting 'lightsdown' time to: " + cal.getTime());
        timer.schedule(new TurnOffTask(true), cal.getTime());
    }

    public void turnLightsOff() throws InterruptedException{
        System.out.println("turning lights off");
        d0.setState(PinState.HIGH);
        d1.setState(PinState.HIGH);
        d2.setState(PinState.LOW);
        d3.setState(PinState.HIGH);
        sendSignalToSocket();
    }

    public void sendSignalToSocket() throws InterruptedException {
        Thread.sleep(100);
        modulator.setState(PinState.HIGH);
        //sleep for 250ms
        Thread.sleep(250);
        //disable modulator
        modulator.setState(PinState.LOW);
    }


    private class TurnOffTask extends TimerTask {

        boolean shutdownAfterRun = false;

        TurnOffTask(boolean shutdown){
            shutdownAfterRun = shutdown;
        }

        @Override
        public void run() {
            LOG.info("TURNING LIGHTS OFF");
            System.out.println("TURNING LIGHTS OFF");
            d0.setState(PinState.HIGH);
            d1.setState(PinState.HIGH);
            d2.setState(PinState.LOW);
            d3.setState(PinState.LOW);
            try {
                sendSignalToSocket();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("Socket 1 & 2 State = OFF");
            if(shutdownAfterRun){
                System.exit(0);
            }
        }
    }

    private class TurnOnTask extends TimerTask {

        @Override
        public void run() {
            LOG.info("TURNING LIGHTS ON");
            System.out.println("TURNING LIGHTS ON");
            d0.setState(PinState.HIGH);
            d1.setState(PinState.HIGH);
            d2.setState(PinState.LOW);
            d3.setState(PinState.HIGH);
            try {
                sendSignalToSocket();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("Socket 1 & 2 State = ON");

        }
    }


}
