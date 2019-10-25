public class Philosophers {
    private static int NUM_PHIL = 5;
    private static int RunCnt[] = new int[NUM_PHIL]; // Counter for eating (Task 4)
    private static Object[] forks = new Object[NUM_PHIL];

    public static void main(String[] args) throws InterruptedException {

        Philosopher[] phils = new Philosopher[NUM_PHIL];
        // Create forks
        for(int i=0; i<NUM_PHIL; i++) forks[i]=new Object();
        for(int i=0; i<NUM_PHIL; i++){
            // Fix for deadlock
            if(i == NUM_PHIL - 1){
                phils[i]=new Philosopher(i, forks[i], forks[(i+1) % NUM_PHIL]);
            }else{
                phils[i]=new Philosopher(i, forks[(i+1)% NUM_PHIL]], forks[i]);
            }       
        }
        // Start all Philosopher threads
        for(Philosopher i : phils){
            i.start();
        }
        Thread.sleep(10000); // Idle here
        // Request termination
        for(Philosopher i : phils){
            i.requestStop();
            i.join();
        }
        // Wait for all to finish

        // Print stats
        for(int i = 0; i < NUM_PHIL; i++){ 
            System.out.print("ID: " + i + " Count: " + RunCnt[i] + "\n");
        }
        
        /** Fun for infinitum and tell for each 100 run
        if(RunCnt[1] % 100 == 0){
            System.out.print("ID: " + 1 + " Count: " + RunCnt[1] + "\n");
        }**/
        
    }
    static class Philosopher extends Thread {
        private final Object leftFork, rightFork;
        private final int id;

        private volatile boolean stop = false;
        public synchronized void requestStop(){ stop = true; }


        public Philosopher(int id, Object leftFork, Object rightFork) {
            this.id = id;
            this.leftFork = leftFork;
            this.rightFork = rightFork;
        }
        
        private void eat() {
            System.out.println("Philosopher "+id+" is eating.");
            RunCnt[id]++;
            // delay
            //try{Thread.sleep(100);}catch(InterruptedException ie){}
        }

        private void think() {
            System.out.println("Philosopher "+id+" is thinking.");
            // delay
            //try{Thread.sleep(100);}catch(InterruptedException ie){}
        }

        private void waiting() {
            System.out.println("Philosopher "+id+" is waiting.");
            // delay
            //try{Thread.sleep(100);}catch(InterruptedException ie){}
        }

        public void run( ) {
            while(!stop) {
                think();
                waiting();
                synchronized(leftFork){
                    // pick up forks
                    synchronized(rightFork){
                        eat();
                    }
                    // put down forks
                }
            }
        }
    }


}
