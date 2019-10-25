package ticker;

import java.util.concurrent.TimeUnit;

public class Ticker2 extends Thread {

	public final static int TOTAL_WORKERS = 25;
	private Thread[] workers = new Thread[TOTAL_WORKERS];
	
	/* Depending on the # of workers, this is how often we need to send 
	 * signals to them. */
	private final long period = 100 / TOTAL_WORKERS; 
	
	private static boolean burn(long millis) {
		long deadline = System.nanoTime() +
				TimeUnit.MILLISECONDS.toNanos(millis);
		try { Thread.sleep(millis - 2); } catch(InterruptedException ie) { return false; }
		while(System.nanoTime() < deadline) {}
		return true;
	}
		
	/* This shall be our control thread signaling the worker threads */
	public void run() {
		//for(Thread t : workers) t.start();
		int currentWorker = 0;
		while(!interrupted()) {
		  synchronized(this) {
			  if(!burn(period)) break;
//			  try { Thread.sleep(period); } catch(InterruptedException ie) {break;}
			  Thread worker = workers[currentWorker];
			  if(worker != null) {
				  synchronized(worker) { worker.notify(); }
			  }
			  currentWorker = (currentWorker + 1) % TOTAL_WORKERS;
		  }
		}
		//for(Thread t: workers) t.interrupt();
	}
	
	static class Worker extends Thread {
		private final int workerId;
		private long lastCall = 0;
		
		public Worker(int id, Ticker2 scheduler) { 
			workerId = id;
			scheduler.workers[id] = this;
		}

		public void task() {
			long myPeriod = (lastCall == 0) ? 0 : System.nanoTime() - lastCall;
			lastCall = System.nanoTime();
			System.out.printf("Task from worker %d with period %.3f\n", workerId, myPeriod/1000000.0);
		}
		
		public void run() {
			while(!interrupted()) {
				synchronized(this) {
					try {
						this.wait();
						task();
					}catch(InterruptedException ie) {
						break;
					}
				}
			}
		}
	}
	
	public static void main(String[] args) throws InterruptedException {
		// Create the scheduler
		Ticker2 t = new Ticker2();
		// Create the workers
		Worker[] ws = new Worker[TOTAL_WORKERS];
		for(int i = 0; i<TOTAL_WORKERS; i++)
			ws[i] = new Worker(i, t);
		// Start the scheduler
		t.start();
		// Give time to execute some worker tasks
		sleep(10000);
		// Terminate the scheduler
		t.interrupt(); t.join();
	}

}
