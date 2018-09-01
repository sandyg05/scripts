#### This is a multithreaded Slowloris DoS attack implementation for educational purposes. ####

* Slowloris works by opening multiple connections to the targeted web server and keeping them open as long as possible. It does this by continuously sending partial HTTP requests, none of which are ever completed. The attacked servers open more and connections open, waiting for each of the attack requests to be completed.
* Periodically, the Slowloris sends subsequent HTTP headers for each request, but never actually completes the request. Ultimately, the targeted server’s maximum concurrent connection pool is filled, and additional (legitimate) connection attempts are denied.
* By sending partial, as opposed to malformed, packets, Slowloris can easily slip by traditional Intrusion Detection systems.
  





