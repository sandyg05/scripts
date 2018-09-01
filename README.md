#### This is a multithreaded Slowloris DoS attack implementation for educational purposes. ####

* Slowloris works by opening multiple connections to the targeted web server and keeping them open as long as possible. It does this by continuously sending partial HTTP requests, none of which are ever completed. The attacked servers open more and connections open, waiting for each of the attack requests to be completed.

  





