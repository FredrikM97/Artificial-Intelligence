import java.util.concurrent.TimeUnit;

public class Philosophers2 extends Thread {
    private static int NUM_PHIL = 5;
    private static int RunCnt[] = new int[NUM_PHIL]; // Counter for eating (Task 4)
    private final long period = 100 / NUM_PHIL; 
    
    private static Object[] forks = new Object[NUM_PHIL];
    private Thread[] phils = new Thread[NUM_PHIL];
	
    
    public static void main(String[] args) throws InterruptedException {
        // Create scheduler
        Philosophers2 scheduler = new Philosophers2();
        Philosopher[] ph = new Philosopher[NUM_PHIL];
        // Create forks
        for(int i=0; i<NUM_PHIL; i++) forks[i]=new Object();
        for(int i=0; i<NUM_PHIL; i++){

            ph[i]=new Philosopher(i, scheduler, forks[i], forks[(i+1) % NUM_PHIL]);
        }
        // Start Scheduler
        scheduler.start();
        sleep(10000); // Idle here

        // Request termination
        scheduler.interrupt(); scheduler.join();

        // Print stats
        for(int i = 0; i < NUM_PHIL; i++){ 
            System.out.print("ID: " + i + " Count: " + RunCnt[i] + "\n");
        }
    }
    /** Waiter thread  control (scheduler) **/
	public void run() {
		for(Thread p : phils) p.start();
		int currentPhils = 0;
		while(!interrupted()) {
		    synchronized(this) {
			  
                try { Thread.sleep(period); } catch(InterruptedException ie) { break; }
                Thread phil = phils[currentPhils];
                if(phil != null) { synchronized(phil) { phil.notify(); }}
                
                currentPhils = (currentPhils + 1) % NUM_PHIL;
            }
        }   
		for(Thread p: phils) p.interrupt();
	}

    static class Philosopher extends Thread {
        private final Object leftFork, rightFork;
        private final int id;
        private long lastCall = 0;

        public Philosopher(int id, Philosophers2 scheduler, Object leftFork, Object rightFork) {
            this.id = id;
            //Tell scheduler that this object exist and add it to the waiter
            scheduler.phils[id] = this;
            this.leftFork = leftFork;
            this.rightFork = rightFork;
        }
        
        private void eat() throws InterruptedException {
            long myPeriod = (lastCall == 0) ? 0 : System.nanoTime() - lastCall;
			lastCall = System.nanoTime();
			System.out.printf("Period from Philosopher %d: %.3f\n", id, myPeriod/1000000.0); 
            //System.out.println("Philosopher "+id+" is eating.");
            RunCnt[id]++;
            // delay
            synchronized(this){
                this.wait(1000);
            }
        }

        private void think() throws InterruptedException {
            //System.out.println("Philosopher "+id+" is thinking.");
            // delay

            Thread.sleep(10);
        }

        private void waiting() throws InterruptedException {
            //System.out.println("Philosopher "+id+" is waiting.");
            // delay
            Thread.sleep(10);
        }

        public void run() {
            while(!interrupted()) {
                try{
                    think();
                    waiting();
                    synchronized(leftFork){
                        // pick up forks
                        synchronized(rightFork){
                                eat();
                        }
                        // put down forks
                    }
                }catch(InterruptedException ie) {
                    break;
                }
            }
        }

    }
}
