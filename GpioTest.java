import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalOutput;
import com.pi4j.io.gpio.PinPullResistance;
import com.pi4j.io.gpio.PinState;
import com.pi4j.io.gpio.RaspiPin;


/**
 * Created with IntelliJ IDEA.
 * User: ga2salw
 * Date: 11/07/14
 * Time: 16:04
 * To change this template use File | Settings | File Templates.
 */
public class GpioTest {

    GpioController gpio;
    GpioPinDigitalOutput red;
    GpioPinDigitalOutput green;

    public GpioTest() {
        init();

        while(true){
            green.toggle();
            System.out.println("Green toggle");
            red.toggle();
            System.out.println("red toggle");
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void init() {
        //Create factory controller
        gpio = GpioFactory.getInstance();
        //provision two pins for output
        red = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_02,"red led",PinState.LOW);
        red.setShutdownOptions(true, PinState.LOW, PinPullResistance.OFF);
        green = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_04,"green led",PinState.LOW);
        green.setShutdownOptions(true, PinState.LOW, PinPullResistance.OFF);

    }
}
